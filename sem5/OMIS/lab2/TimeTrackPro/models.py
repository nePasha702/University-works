import calendar
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import StrEnum
from io import BytesIO
from math import isfinite

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from database import check_password, connect, hash_password, notify, now


class ScheduleType(StrEnum):
    FIVE_DAY = "FIVE_DAY"
    SHIFT_WORK = "SHIFT_WORK"
    FLEXIBLE = "FLEXIBLE"


class AbsenceType(StrEnum):
    VACATION = "VACATION"
    SICK_LEAVE = "SICK_LEAVE"
    DAY_OFF = "DAY_OFF"
    BUSINESS_TRIP = "BUSINESS_TRIP"


class LeaveRequestStatus(StrEnum):
    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


def days_between(start, end):
    for index in range((end - start).days + 1):
        yield start + timedelta(days=index)


@dataclass
class Department:
    id: int
    name: str


@dataclass
class WorkSchedule:
    id: int
    type: ScheduleType
    startTime: time
    endTime: time
    standardDailyHours: float
    breakMinutes: int

    @classmethod
    def from_row(cls, row):
        return cls(row["id"], ScheduleType(row["type"]), time.fromisoformat(row["start"]),
                   time.fromisoformat(row["end"]), row["hours"], row["break_minutes"])

    def is_workday(self, day):
        return day.weekday() in (range(1, 6) if self.type == ScheduleType.SHIFT_WORK else range(5))


def schedule_for(db, employee_id, day=None):
    row = db.execute("""SELECT s.* FROM users u LEFT JOIN planned_days p
                     ON p.employee_id=u.id AND p.day=? JOIN schedules s
                     ON s.id=COALESCE(p.schedule_id,u.schedule_id) WHERE u.id=?""",
                     (day, employee_id)).fetchone()
    return WorkSchedule.from_row(row)


@dataclass
class TimeEntry:
    id: int
    date: date
    clockInTime: datetime
    clockOutTime: datetime | None
    breakMinutes: int
    isLate: bool
    workedHours: float
    employee_id: int | None = None

    @classmethod
    def from_row(cls, row):
        end = row["clock_out"]
        return cls(row["id"], date.fromisoformat(row["day"]), datetime.fromisoformat(row["clock_in"]),
                   datetime.fromisoformat(end) if end else None, row["break_minutes"],
                   bool(row["late"]), row["hours"], row["employee_id"])

    def calculateDuration(self):
        if self.clockOutTime is None:
            return 0.0
        minutes = (self.clockOutTime - self.clockInTime).total_seconds() / 60
        return round(max(0, minutes - self.breakMinutes) / 60, 4)


@dataclass
class LeaveBalance:
    id: int
    year: int
    totalDays: int
    usedDays: int

    def getAvailableDays(self):
        return self.totalDays - self.usedDays

    def deductDays(self, days):
        if not 0 <= days <= self.getAvailableDays():
            return False
        self.usedDays += days
        return True


def get_balance(db, employee_id, year):
    row = db.execute("SELECT * FROM balances WHERE employee_id=? AND year=?",
                     (employee_id, year)).fetchone()
    return LeaveBalance(row["id"], year, row["total"], row["used"]) if row else LeaveBalance(0, year, 24, 0)


@dataclass
class LeaveRequest:
    id: int
    type: AbsenceType
    startDate: date
    endDate: date
    status: LeaveRequestStatus
    comment: str
    employee_id: int
    manager_id: int
    reason: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(row["id"], AbsenceType(row["type"]), date.fromisoformat(row["start"]),
                   date.fromisoformat(row["end"]), LeaveRequestStatus(row["status"]),
                   row["comment"], row["employee_id"], row["manager_id"], row["reason"])

    def updateStatus(self, newStatus):
        allowed = {
            LeaveRequestStatus.DRAFT: {LeaveRequestStatus.UNDER_REVIEW},
            LeaveRequestStatus.UNDER_REVIEW: {LeaveRequestStatus.APPROVED, LeaveRequestStatus.REJECTED},
        }
        if newStatus not in allowed.get(self.status, set()):
            raise ValueError("Решение по заявке уже принято или переход недопустим.")
        self.status = newStatus


@dataclass
class Notification:
    id: int
    message: str
    isRead: bool
    createdAt: datetime
    recipient_id: int

    def markAsRead(self):
        with connect() as db:
            db.execute("UPDATE notifications SET is_read=1 WHERE id=? AND user_id=?",
                       (self.id, self.recipient_id))
        self.isRead = True


@dataclass
class TimesheetRecord:
    id: int
    plannedHours: float
    actualHours: float
    absenceDays: int
    overtimeHours: float
    manualAdjustmentHours: float
    employee_id: int
    full_name: str
    employee_label: str = ""

    @property
    def corrected_hours(self):
        return round(self.actualHours + self.manualAdjustmentHours, 4)

    def recalculate(self):
        self.overtimeHours = round(max(0, self.corrected_hours - self.plannedHours), 4)


@dataclass
class Timesheet:
    id: int
    month: int
    year: int
    isClosed: bool
    records: list[TimesheetRecord] = field(default_factory=list)
    planned_total: float = 0
    actual_total: float = 0
    overtime_enabled: bool = True

    def calculateTotals(self):
        for record in self.records:
            record.recalculate()
            if not self.overtime_enabled:
                record.overtimeHours = 0
        self.planned_total = sum(r.plannedHours for r in self.records)
        self.actual_total = sum(r.corrected_hours for r in self.records)

    def exportToExcel(self):
        book = Workbook()
        sheet = book.active
        sheet.title = f"Табель {self.month:02d}.{self.year}"
        sheet.append(["№", "ФИО", "Норма, ч", "Факт, ч", "Отсутствия, дн.",
                      "Корректировка, ч", "Итого, ч", "Переработка, ч"])
        for index, record in enumerate(self.records, start=1):
            sheet.append([index, record.full_name, record.plannedHours, record.actualHours,
                          record.absenceDays, record.manualAdjustmentHours,
                          record.corrected_hours, record.overtimeHours])
            sheet.cell(sheet.max_row, 2).data_type = "s"
        sheet.append(["", "Итого", self.planned_total, sum(r.actualHours for r in self.records),
                      sum(r.absenceDays for r in self.records),
                      sum(r.manualAdjustmentHours for r in self.records),
                      self.actual_total, sum(r.overtimeHours for r in self.records)])
        for cell in sheet[1]:
            cell.fill = PatternFill("solid", fgColor="604388")
            cell.font = Font(color="FFFFFF", bold=True)
        for col, width in zip("ABCDEFGH", (7, 34, 13, 13, 19, 22, 13, 20)):
            sheet.column_dimensions[col].width = width
        sheet.freeze_panes = "C2"
        output = BytesIO()
        book.save(output)
        return output.getvalue()


@dataclass
class User(ABC):
    id: int
    firstName: str
    lastName: str
    username: str
    passwordHash: str
    email: str
    department: Department
    position: str

    @property
    def full_name(self):
        return f"{self.lastName} {self.firstName}"

    @property
    @abstractmethod
    def role(self):
        raise NotImplementedError

    @classmethod
    def load(cls, user_id):
        with connect() as db:
            row = db.execute("""SELECT u.*, d.name AS department FROM users u
                             JOIN departments d ON d.id=u.department_id WHERE u.id=?""",
                             (user_id,)).fetchone()
        if row is None:
            raise ValueError("Учётная запись не найдена.")
        subtype = {"employee": Employee, "manager": DepartmentManager, "hradmin": HRAdmin}[row["role"]]
        return subtype(row["id"], row["first_name"], row["last_name"], row["login"],
                       row["password_hash"], row["email"],
                       Department(row["department_id"], row["department"]), row["position"])

    @classmethod
    def login(cls, username, password):
        with connect() as db:
            row = db.execute("SELECT id,password_hash FROM users WHERE login=?",
                             (username.strip().casefold(),)).fetchone()
        if row is None or not check_password(password, row["password_hash"]):
            raise ValueError("Неверный логин или пароль.")
        return cls.load(row["id"])

    def logout(self, session):
        session.clear()

    def notifications(self):
        with connect() as db:
            rows = db.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY id DESC",
                              (self.id,)).fetchall()
        return [Notification(r["id"], r["message"], bool(r["is_read"]),
                             datetime.fromisoformat(r["created_at"]), self.id) for r in rows]


class Employee(User):
    role = "employee"

    def clockIn(self):
        stamp = now()
        with connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM time_entries WHERE employee_id=? AND clock_out IS NULL",
                          (self.id,)).fetchone():
                raise ValueError("Смена уже открыта.")
            schedule = schedule_for(db, self.id, stamp.date())
            late = stamp.replace(second=0, microsecond=0).time() > schedule.startTime
            db.execute("""INSERT INTO time_entries(employee_id,day,clock_in,break_minutes,late)
                       VALUES(?,?,?,?,?)""",
                       (self.id, stamp.date(), stamp.isoformat(), schedule.breakMinutes, late))

    def clockOut(self):
        stamp = now()
        with connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM time_entries WHERE employee_id=? AND clock_out IS NULL",
                             (self.id,)).fetchone()
            if row is None:
                raise ValueError("Сначала начните смену.")
            entry = TimeEntry.from_row(row)
            entry.clockOutTime = max(stamp, entry.clockInTime)
            entry.workedHours = entry.calculateDuration()
            db.execute("UPDATE time_entries SET clock_out=?, hours=? WHERE id=?",
                       (entry.clockOutTime.isoformat(), entry.workedHours, entry.id))

    def viewHistory(self):
        with connect() as db:
            rows = db.execute("SELECT * FROM time_entries WHERE employee_id=? ORDER BY id DESC",
                              (self.id,)).fetchall()
        return [TimeEntry.from_row(row) for row in rows]

    def viewSchedule(self, day=None):
        with connect() as db:
            return schedule_for(db, self.id, day or now().date())

    def createLeaveRequest(self, type, startDate, endDate, comment=""):
        if endDate < startDate or startDate.year != endDate.year:
            raise ValueError("Укажите даты по порядку в пределах одного календарного года.")
        with connect() as db:
            db.execute("BEGIN IMMEDIATE")
            manager = db.execute("""SELECT id FROM users WHERE department_id=? AND role='manager'
                                 AND id!=? ORDER BY id LIMIT 1""",
                                 (self.department.id, self.id)).fetchone()
            if manager is None:
                raise ValueError("Для этого отдела не назначен согласующий руководитель.")
            if db.execute("""SELECT 1 FROM requests WHERE employee_id=? AND start<=? AND end>=?
                          AND status IN ('UNDER_REVIEW','APPROVED')""",
                          (self.id, endDate, startDate)).fetchone():
                raise ValueError("На эти даты уже есть действующая заявка.")
            if type == AbsenceType.VACATION:
                count = (endDate - startDate).days + 1
                if get_balance(db, self.id, startDate.year).getAvailableDays() < count:
                    raise ValueError("Недостаточно дней отпуска.")
            request = LeaveRequest(0, type, startDate, endDate, LeaveRequestStatus.DRAFT,
                                   comment, self.id, manager["id"])
            request.updateStatus(LeaveRequestStatus.UNDER_REVIEW)
            request.id = db.execute("""INSERT INTO requests(employee_id,manager_id,type,start,end,status,comment)
                                    VALUES(?,?,?,?,?,?,?)""",
                                    (self.id, request.manager_id, type, startDate, endDate,
                                     request.status, comment)).lastrowid
            notify(db, request.manager_id, f"{self.full_name} отправил(а) заявку на отсутствие.")
            return request


class DepartmentManager(Employee):
    role = "manager"

    def approveRequest(self, request):
        self._decide(request.id, LeaveRequestStatus.APPROVED, "")

    def rejectRequest(self, request, reason):
        reason = reason.strip()
        if not reason:
            raise ValueError("Укажите причину отклонения.")
        self._decide(request.id, LeaveRequestStatus.REJECTED, reason)

    def _decide(self, request_id, status, reason):
        with connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("""SELECT r.* FROM requests r JOIN users u ON u.id=r.employee_id
                             WHERE r.id=? AND r.manager_id=? AND u.department_id=?""",
                             (request_id, self.id, self.department.id)).fetchone()
            if row is None:
                raise ValueError("Заявка недоступна.")
            request = LeaveRequest.from_row(row)
            request.updateStatus(status)
            if status == LeaveRequestStatus.APPROVED and request.type == AbsenceType.VACATION:
                year = request.startDate.year
                balance = get_balance(db, request.employee_id, year)
                if not balance.deductDays((request.endDate - request.startDate).days + 1):
                    raise ValueError("Остаток дней изменился. Утвердить заявку невозможно.")
                db.execute("""INSERT INTO balances(employee_id,year,total,used) VALUES(?,?,?,?)
                           ON CONFLICT(employee_id,year) DO UPDATE SET used=excluded.used""",
                           (request.employee_id, year, balance.totalDays, balance.usedDays))
            db.execute("UPDATE requests SET status=?, reason=? WHERE id=?", (status, reason, request_id))
            decision = "утверждена" if status == LeaveRequestStatus.APPROVED else f"отклонена ({reason})"
            notify(db, request.employee_id, f"Заявка №{request_id} {decision}.")

    def viewTeamAttendance(self):
        with connect() as db:
            rows = db.execute("""SELECT t.* FROM time_entries t JOIN users u ON u.id=t.employee_id
                              WHERE u.department_id=? AND u.id!=? AND u.role!='hradmin' ORDER BY t.id DESC""",
                              (self.department.id, self.id)).fetchall()
        return [TimeEntry.from_row(row) for row in rows]

    def planShiftSchedule(self, start, end, assignments):
        if not 0 <= (end - start).days <= 92:
            raise ValueError("Укажите период до 93 дней включительно.")
        with connect() as db:
            db.execute("BEGIN IMMEDIATE")
            for employee_id, schedule in assignments.items():
                member = db.execute("""SELECT 1 FROM users WHERE id=? AND department_id=?
                                    AND role!='hradmin' AND id!=?""",
                                    (employee_id, self.department.id, self.id)).fetchone()
                if member is None:
                    raise ValueError("В график можно включать только сотрудников своего отдела.")
                db.executemany("""INSERT INTO planned_days VALUES(?,?,?)
                               ON CONFLICT(employee_id,day) DO UPDATE SET schedule_id=excluded.schedule_id""",
                               [(employee_id, day, schedule) for day in days_between(start, end)])


class HRAdmin(User):
    role = "hradmin"

    def manageEmployees(self, query=""):
        with connect() as db:
            rows = db.execute("""SELECT u.*, d.name AS department FROM users u
                              JOIN departments d ON d.id=u.department_id
                              ORDER BY last_name,first_name""").fetchall()
        needle = query.strip().casefold()
        return [r for r in rows if needle in f"{r['last_name']} {r['first_name']} {r['department']}".casefold()]

    def configureSchedule(self, schedule):
        minutes = (datetime.combine(date.min, schedule.endTime)
                   - datetime.combine(date.min, schedule.startTime)).total_seconds() / 60
        if not 0 <= schedule.breakMinutes < minutes:
            raise ValueError("Окончание должно быть позже начала, а перерыв — короче смены.")
        with connect() as db:
            db.execute("UPDATE schedules SET type=?, start=?, end=?, hours=?, break_minutes=? WHERE id=?",
                       (schedule.type, schedule.startTime.strftime("%H:%M"),
                        schedule.endTime.strftime("%H:%M"), (minutes-schedule.breakMinutes)/60,
                        schedule.breakMinutes, schedule.id))

    def generateMonthlyTimesheet(self, month, year):
        start = date(year, month, 1)
        end = date(year, month, calendar.monthrange(year, month)[1])
        with connect() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("""INSERT OR IGNORE INTO timesheets(month,year,admin_id) VALUES(?,?,?)""",
                       (month, year, self.id))
            sheet = db.execute("SELECT * FROM timesheets WHERE month=? AND year=?", (month, year)).fetchone()
            overtime = bool(db.execute("SELECT enabled FROM settings WHERE key='overtime'").fetchone()[0])
            result = Timesheet(sheet["id"], month, year, bool(sheet["is_closed"]), overtime_enabled=overtime)
            if result.isClosed:
                raise ValueError("Табель за этот период закрыт.")
            employees = db.execute("""SELECT * FROM users WHERE role!='hradmin' AND hired_on<=?
                                   ORDER BY role='manager', id""", (end,))
            for employee in employees:
                employee_id = employee["id"]
                approved = db.execute("""SELECT start,end FROM requests WHERE employee_id=?
                                      AND status='APPROVED' AND start<=? AND end>=?""",
                                      (employee_id, end, start)).fetchall()
                planned, absences = 0.0, 0
                for day in days_between(max(start, date.fromisoformat(employee["hired_on"])), end):
                    schedule = schedule_for(db, employee_id, day)
                    if not schedule.is_workday(day):
                        continue
                    if any(r["start"] <= day.isoformat() <= r["end"] for r in approved):
                        absences += 1
                    else:
                        planned += schedule.standardDailyHours
                actual = db.execute("""SELECT COALESCE(SUM(hours),0) FROM time_entries
                                    WHERE employee_id=? AND day BETWEEN ? AND ?""",
                                    (employee_id, start, end)).fetchone()[0]
                row = db.execute("""INSERT INTO timesheet_records(sheet_id,employee_id,planned,actual,absence_days,overtime)
                                 VALUES(?,?,?,?,?,0) ON CONFLICT(sheet_id,employee_id) DO UPDATE SET
                                 planned=excluded.planned, actual=excluded.actual, absence_days=excluded.absence_days
                                 RETURNING id,adjustment""",
                                 (result.id, employee_id, planned, actual, absences)).fetchone()
                name = f"{employee['last_name']} {employee['first_name']}"
                short_name = employee["last_name"] + " " + "".join(
                    word[0] + "." for word in employee["first_name"].split())
                result.records.append(TimesheetRecord(row["id"], planned, actual, absences, 0,
                                                     row["adjustment"], employee_id, name, short_name))
            result.calculateTotals()
            db.executemany("UPDATE timesheet_records SET overtime=? WHERE id=?",
                           [(r.overtimeHours, r.id) for r in result.records])
        return result

    def adjustTimesheet(self, record, correctedHours):
        if not isfinite(correctedHours) or correctedHours < 0:
            raise ValueError("Укажите неотрицательное количество часов.")
        with connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("""SELECT r.actual,r.planned,s.is_closed FROM timesheet_records r
                             JOIN timesheets s ON s.id=r.sheet_id WHERE r.id=?""", (record.id,)).fetchone()
            if row is None or row["is_closed"]:
                raise ValueError("Строка табеля недоступна для корректировки.")
            enabled = db.execute("SELECT enabled FROM settings WHERE key='overtime'").fetchone()[0]
            adjustment = round(correctedHours - row["actual"], 4)
            overtime = round(max(0, correctedHours - row["planned"]), 4) if enabled else 0
            db.execute("UPDATE timesheet_records SET adjustment=?,overtime=? WHERE id=?",
                       (adjustment, overtime, record.id))


def save_employee(full_name, login, password, email, department_id, position, phone="",
                  role="employee", user_id=None):
    parts = full_name.strip().split(maxsplit=1)
    normalized_login = login.strip().casefold()
    if len(parts) < 2 or "@" not in email or email.startswith("@"):
        raise ValueError("Укажите фамилию, имя и действительный адрес email.")
    try:
        with connect() as db:
            if user_id is None:
                if len(normalized_login) < 3 or any(c.isspace() for c in normalized_login) or len(password) < 6:
                    raise ValueError("Логин должен содержать от 3 символов без пробелов, пароль — от 6 символов.")
                db.execute("""INSERT INTO users(first_name,last_name,login,password_hash,email,department_id,
                           role,position,schedule_id,phone,hired_on) VALUES(?,?,?,?,?,?,?,?,1,?,?)""",
                           (parts[1], parts[0], normalized_login, hash_password(password), email.strip(),
                            department_id, role, position.strip(), phone.strip(), now().date()))
            else:
                db.execute("BEGIN IMMEDIATE")
                previous = db.execute("SELECT department_id FROM users WHERE id=?", (user_id,)).fetchone()
                if previous["department_id"] != department_id:
                    pending = db.execute("""SELECT 1 FROM requests WHERE status='UNDER_REVIEW'
                                         AND (employee_id=? OR manager_id=?) LIMIT 1""", (user_id, user_id)).fetchone()
                    if pending:
                        raise ValueError("Сначала завершите согласование заявок сотрудника, затем измените отдел.")
                db.execute("""UPDATE users SET first_name=?,last_name=?,email=?,department_id=?,
                           position=?,phone=? WHERE id=?""",
                           (parts[1], parts[0], email.strip(), department_id,
                            position.strip(), phone.strip(), user_id))
    except sqlite3.IntegrityError as exc:
        if "users.login" in str(exc):
            raise ValueError("Такой логин уже существует.") from exc
        raise
