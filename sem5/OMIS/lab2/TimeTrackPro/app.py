from abc import ABC, abstractmethod
from base64 import b64encode
from calendar import monthrange
from datetime import date, datetime, time, timedelta
from json import dumps

import streamlit as st

from database import FIXED_NOW, SETTINGS, connect, now, seed
from models import (
    AbsenceType, DepartmentManager, Employee, LeaveRequest, ScheduleType, User,
    WorkSchedule, days_between, get_balance, save_employee, schedule_for,
)
from ui.view import action, buttons, card, date_field, details, esc, field, form, heading, icon, panel, render


ABSENCE = dict(zip(AbsenceType, ("Отпуск", "Больничный", "Отгул", "Командировка")))
ABSENCE_ICONS = dict(zip(AbsenceType, ("vacation", "sick", "clipboard", "plane")))
STATUS = {
    "DRAFT": "Черновик", "UNDER_REVIEW": "На согласовании",
    "APPROVED": "Утверждена", "REJECTED": "Отклонена",
}
ROLE = {"employee": "Сотрудник", "manager": "Руководитель", "hradmin": "Администратор"}
ROLE_ICON = {"employee": "person", "manager": "tie", "hradmin": "tools"}
HOME = {"employee": "EmployeeDash", "manager": "ManagerDash", "hradmin": "HRDash"}
MENU = {
    "employee": (("TimeTracking", "clock", "Отметить время"), ("MySchedule", "calendar", "Мой график"),
                 ("LeaveRequest", "plane", "Заявка на отпуск")),
    "manager": (("TeamAttendance", "people", "Посещаемость отдела"), ("Approvals", "check", "Согласовать заявки"),
                ("TeamSchedule", "chart", "Сформировать график")),
    "hradmin": (("EmployeeDirectory", "people", "Справочник сотрудников"), ("Reports", "report", "Формирование табеля"),
                ("SystemSettings", None, "⚙ Системные настройки")),
}
SCREENS = {
    "Login": ("login", "Вход в систему", "login"),
    "Register": ("register", "Регистрация", "register"),
    "EmployeeDash": ("employee-dash", "Дашборд сотрудника", "showDashboard"),
    "ManagerDash": ("manager-dash", "Дашборд руководителя", "showDashboard"),
    "HRDash": ("hr-dash", "Дашборд HR-администратора", "showDashboard"),
    "TimeTracking": ("time-tracking", "Отметка времени", "time_tracking"),
    "MySchedule": ("my-schedule", "Мой график", "my_schedule"),
    "LeaveRequest": ("leave-request", "Заявка на отсутствие", "leave_request"),
    "TeamAttendance": ("team-attendance", "Посещаемость отдела", "team_attendance"),
    "TeamSchedule": ("team-schedule", "График отдела", "team_schedule"),
    "Approvals": ("approvals", "Согласование заявок", "approvals"),
    "EmployeeDirectory": ("directory", "Справочник сотрудников", "directory"),
    "Reports": ("reports", "Формирование табеля", "reports"),
    "SystemSettings": ("settings", "Системные настройки", "settings"),
}
ACTIONS = {
    "Login": {"login"}, "Register": {"register"},
    "EmployeeDash": {"read"}, "ManagerDash": {"read", "start", "finish", "week"},
    "HRDash": {"read", "schedule_config", "configure_schedule"},
    "TimeTracking": {"start", "finish"}, "MySchedule": {"week"},
    "LeaveRequest": {"leave"}, "TeamAttendance": {"history"},
    "TeamSchedule": {"team_period", "save_plan"},
    "Approvals": {"approve", "reject_panel", "reject", "cancel_reject"},
    "EmployeeDirectory": {"profile", "edit", "add", "save_employee", "cancel_employee"},
    "Reports": {"report_period", "adjust_panel", "adjust"}, "SystemSettings": {"save_settings"},
}
MONTHS = "январь февраль март апрель май июнь июль август сентябрь октябрь ноябрь декабрь".split()
WEEKDAYS = "Понедельник Вторник Среда Четверг Пятница Суббота Воскресенье".split()
SETTINGS_TEXT = {
    "email": ("bell", "Отправлять уведомления на почту"),
    "reminders": ("alarm", "Напоминать за 15 мин до начала смены"),
    "overtime": ("chart", "Учитывать часы сверх нормы"),
    "two_factor": ("lock", "Требовать код при входе"),
    "turnstiles": ("globe", "Синхронизация с физическими пропусками"),
}


def full_name(row):
    return f"{row['last_name']} {row['first_name']}"


def initials(last, first):
    return f"{last} {''.join(word[0] + '.' for word in first.split())}"


def short_name(row):
    return initials(row["last_name"], row["first_name"])


def span(start, end):
    return f"{start:%d.%m.%Y} — {end:%d.%m.%Y}"


def hours(value, compact=False):
    h, m = divmod(round(value * 60), 60)
    return (f"{h}ч" + (f" {m}м" if m else "")) if compact else f"{h} ч {m:02d} мин"


def vacation_days(value):
    form = "дней"
    if not 11 <= value % 100 <= 14:
        form = {1: "день", 2: "дня", 3: "дня", 4: "дня"}.get(value % 10, form)
    return f"{value} {form}"


def read_date(value):
    try:
        return datetime.strptime(value, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Введите действительную дату в формате ДД.ММ.ГГГГ.") from None


def lookup():
    with connect() as db:
        departments = {r["id"]: r["name"] for r in db.execute("SELECT * FROM departments ORDER BY id")}
        schedules = {r["id"]: WorkSchedule.from_row(r) for r in db.execute("SELECT * FROM schedules ORDER BY id")}
    return departments, schedules


def shift_label(schedule):
    prefix = {ScheduleType.FIVE_DAY: "Пн-Пт", ScheduleType.SHIFT_WORK: "Вт-Сб",
              ScheduleType.FLEXIBLE: "Пн-Пт (гибкий)"}[schedule.type]
    return f"{prefix}: {schedule.startTime:%H:%M}-{schedule.endTime:%H:%M}"


def description_rows(values):
    return "<dl>" + "".join(
        f'<div><dt>{esc(label)}</dt><dd>{value}</dd></div>' for label, value in values
    ) + "</dl>"


class UI(ABC):
    @abstractmethod
    def showDashboard(self):
        raise NotImplementedError

    @abstractmethod
    def showNotifications(self):
        raise NotImplementedError

    @abstractmethod
    def openForm(self, formName):
        raise NotImplementedError

    @abstractmethod
    def submitAction(self, action):
        raise NotImplementedError


class WebUI(UI):
    def __init__(self):
        self.session = st.session_state
        try:
            self.user = User.load(self.session.user_id) if "user_id" in self.session else None
        except ValueError:
            self.session.clear()
            self.user = None
        self.page = self.current_page()
        self.inputs = {}

    def current_page(self):
        if self.user is None:
            return "Register" if self.session.get("page") == "Register" else "Login"
        home = HOME[self.user.role]
        page = self.session.get("page", home)
        return page if page == home or page in {row[0] for row in MENU[self.user.role]} else home

    def openForm(self, formName):
        self.session.page = formName
        for key in ("directory_panel", "attendance_id", "reject_id", "schedule_id", "adjust_open"):
            self.session.pop(key, None)

    def submitAction(self, event):
        name, target = event.get("name"), event.get("target")
        values = event.get("values", {})
        if name == "open":
            pages = {row[0] for row in MENU[self.user.role]} if self.user else {"Login", "Register"}
            if target in pages:
                self.openForm(target)
            return
        if self.user and name == "back":
            self.openForm(HOME[self.user.role])
            return
        if self.user and name == "logout" and self.page == HOME[self.user.role]:
            self.user.logout(self.session)
            self.user = None
            return
        if name not in ACTIONS[self.page]:
            return
        try:
            message = self.apply_action(name, target, values)
        except ValueError as exc:
            self.inputs = {key: value for key, value in values.items() if "password" not in key}
            self.session.notice = ("error", str(exc))
        else:
            if message:
                self.session.notice = ("success", message)

    def apply_action(self, name, target, values):
        if name == "login":
            self.user = User.login(values["login"], values["password"])
            self.session.user_id = self.user.id
            self.openForm(HOME[self.user.role])
        elif name == "register":
            departments, _ = lookup()
            department = next((key for key, label in departments.items() if label == "Отдел продаж"), next(iter(departments)))
            save_employee(values["name"], values["login"], values["new_password"], values["email"],
                          department, "Сотрудник")
            self.openForm("Login")
            return "Учётная запись создана. Войдите в систему."
        elif name == "read":
            item = next((item for item in self.user.notifications() if str(item.id) == target), None)
            if item:
                item.markAsRead()
        elif name == "start":
            self.user.clockIn()
        elif name == "finish":
            self.user.clockOut()
        elif name == "week":
            self.session.week_day = read_date(values["week_day"])
        elif name == "leave":
            self.user.createLeaveRequest(AbsenceType(values["kind"]), read_date(values["start"]),
                                         read_date(values["end"]), values.get("comment", ""))
            self.openForm(HOME[self.user.role])
            return "Заявка отправлена руководителю."
        elif name == "history":
            member = next((row for row in self.team_members() if str(row["id"]) == target), None)
            if member:
                self.toggle("attendance_id", member["id"])
        elif name == "team_period":
            start, end = read_date(values["plan_start"]), read_date(values["plan_end"])
            if not 0 <= (end - start).days <= 92:
                raise ValueError("Укажите период до 93 дней включительно.")
            self.session.team_period = (start, end)
        elif name == "save_plan":
            _, schedules = lookup()
            assignments = {row["id"]: int(values[f"shift_{row['id']}"]) for row in self.team_members()
                           if f"shift_{row['id']}" in values}
            if not assignments or any(value not in schedules for value in assignments.values()):
                raise ValueError("Укажите действующие графики сотрудников.")
            self.user.planShiftSchedule(*self.team_period(), assignments)
            return "График отдела сохранён."
        elif name in {"approve", "reject_panel", "reject", "cancel_reject"}:
            return self.decide(name, target, values)
        elif name in {"profile", "edit", "add", "save_employee", "cancel_employee"}:
            return self.directory_action(name, target, values)
        elif name == "report_period":
            year, month = map(int, values["month"].split("-"))
            if not 2000 <= year <= 2100 or not 1 <= month <= 12:
                raise ValueError("Укажите месяц в диапазоне 2000–2100 годов.")
            self.session.report_period = (year, month)
            self.session.pop("adjust_open", None)
        elif name == "adjust_panel":
            self.toggle("adjust_open", True)
        elif name == "adjust":
            sheet = self.report()
            record = next((r for r in sheet.records if str(r.id) == values["record"]), None)
            if record is None:
                raise ValueError("Строка табеля недоступна для корректировки.")
            self.user.adjustTimesheet(record, float(values["hours"].replace(",", ".")))
            self.session.pop("adjust_open", None)
            return "Корректировка сохранена."
        elif name == "schedule_config":
            _, schedules = lookup()
            schedule_id = int(target) if target else next(iter(schedules))
            if schedule_id in schedules:
                self.session.schedule_id = schedule_id
        elif name == "configure_schedule":
            _, schedules = lookup()
            schedule = schedules.get(int(target))
            if schedule is None:
                raise ValueError("График не найден.")
            configured = WorkSchedule(schedule.id, schedule.type, time.fromisoformat(values["schedule_start"]),
                                      time.fromisoformat(values["schedule_end"]), schedule.standardDailyHours,
                                      int(values["pause"]))
            self.user.configureSchedule(configured)
            self.session.pop("schedule_id", None)
            return "Типовой график сохранён."
        elif name == "save_settings":
            with connect() as db:
                db.executemany("UPDATE settings SET enabled=? WHERE key=?",
                               [(key in values, key) for key in SETTINGS])
            return "Настройки сохранены."

    def toggle(self, key, value):
        if self.session.get(key) == value:
            self.session.pop(key, None)
        else:
            self.session[key] = value

    def run(self):
        event = self.session.get("screen", {}).get("event")
        revision = self.session.get("revision", 0)
        if event and event.get("revision") == revision:
            self.session.pop("notice", None)
            self.submitAction(event)
            revision += 1
            self.session.revision = revision
            self.page = self.current_page()
        css, title, handler = SCREENS[self.page]
        notice = ""
        if self.session.get("notice"):
            kind, message = self.session.notice
            notice = f'<p class="notice {kind}" role="status">{esc(message)}</p>'
        inner = getattr(self, handler)()
        back = action("← Назад", "back", "back") if self.user and self.page != HOME[self.user.role] else ""
        render(f"""
          <section class="screen {css}" data-page="{self.page}" lang="ru">
            <header class="screen-header">{self.page} — {title}</header>
            <main class="screen-body">{back}{notice}{inner}</main>
          </section>""", revision)

    def auth_intro(self, symbol, title, subtitle):
        return f'<div class="auth-intro">{icon(symbol, 52)}<h1>{title}</h1><p>{subtitle}</p></div>'

    def login(self):
        intro = self.auth_intro("clock", "TimeTrackPro", "Введите ваши учетные данные")
        fields = field("Логин", "login", value=self.inputs.get("login", ""), placeholder="Введите логин")
        fields += field("Пароль", "password", kind="password", placeholder="Введите пароль")
        login = form("login", fields, action("▶ Войти", "login", submit=True))
        register = action("Зарегистрироваться", "open", "link", target="Register")
        return f'{intro}{login}<p class="auth-footer">Нет аккаунта? {register}</p>'

    def register(self):
        intro = self.auth_intro("register", "Регистрация", "Создайте новый аккаунт")
        fields = "".join(field(label, name, value=self.inputs.get(name, ""), kind=kind, placeholder=prompt)
                         for label, name, kind, prompt in (
            ("ФИО", "name", "text", "Иванов Иван Иванович"),
            ("Логин", "login", "text", "Придумайте логин"),
            ("Пароль", "new_password", "password", "Придумайте пароль (мин. 6 символов)"),
            ("Email", "email", "email", "example@mail.ru"),
        ))
        fields += field("Роль", "role", value=self.inputs.get("role", ""), options={"employee": ROLE["employee"]},
                        placeholder="Выберите роль" if not self.inputs.get("role") else "")
        register = form("register", fields, action("✓ Зарегистрироваться", "register", "teal", submit=True))
        enter = action("Войти", "open", "link", target="Login")
        return f'{intro}{register}<p class="auth-footer">Уже есть аккаунт? {enter}</p>'

    def showDashboard(self):
        user = self.user
        subtitle = ("Администратор HR-отдела" if user.role == "hradmin"
                    else f"{ROLE[user.role]} · {user.department.name}")
        user_line = f'<h2>{icon(ROLE_ICON[user.role], 22)} {esc(user.full_name)}</h2><p>{esc(subtitle)}</p>'
        logout = action("Выход", "logout", "red small logout")
        identity = f'<div class="identity"><div>{user_line}</div>{logout}</div>'
        account = (f'<details class="account" data-keep="account"><summary>Вы вошли как: '
                   f'<strong>{esc(user.username)}</strong></summary><div>{self.showNotifications()}</div></details>')
        today = now().date()
        with connect() as db:
            if isinstance(user, DepartmentManager):
                team = self.team_members()
                at_work = {entry.employee_id for entry in user.viewTeamAttendance() if entry.clockOutTime is None}
                stats = [("На рабочем месте", f"{len(at_work)} / {len(team)}"),
                         ("Заявок на согласование", len(self.pending_requests()))]
            elif isinstance(user, Employee):
                work = sum(r.workedHours for r in user.viewHistory() if r.date == today)
                balance = get_balance(db, user.id, today.year).getAvailableDays()
                stats = [("Отработано сегодня", hours(work)), ("Остаток отпуска", vacation_days(balance))]
            else:
                count = db.execute("SELECT COUNT(*) FROM users WHERE role!='hradmin'").fetchone()[0]
                stats = [("Всего сотрудников", count), ("Активных графиков", len(lookup()[1]))]
        metrics = []
        for label, value in stats:
            text = f"<span>{label}</span><strong>{value}</strong>"
            if label == "Активных графиков":
                metrics.append(action(text, "schedule_config", "metric", title="Настроить типовой график"))
            else:
                metrics.append(f'<div class="metric">{text}</div>')
        navigation = "".join(action(f"{icon(symbol, 18)} {label}" if symbol else label, "open", target=target)
                             for target, symbol, label in MENU[user.role])
        config = self.schedule_settings() if user.role == "hradmin" and self.session.get("schedule_id") else ""
        return (f'{identity}{account}<div class="metrics">{"".join(metrics)}</div>'
                f'<nav class="nav" aria-label="Разделы кабинета">{navigation}</nav>{config}')

    def showNotifications(self):
        notices = self.user.notifications()
        content = "<strong>Уведомления</strong>"
        if notices:
            entries = []
            for item in notices:
                mark = action("Отметить прочитанным", "read", "link", target=item.id) if not item.isRead else ""
                entries.append(f'<li>{esc(item.message)} <small>{item.createdAt:%d.%m.%Y %H:%M}</small> {mark}</li>')
            content += f'<ul>{"".join(entries)}</ul>'
        else:
            content += "<p>Уведомлений пока нет.</p>"
        if isinstance(self.user, DepartmentManager):
            start = details("Мой учёт времени", self.time_tracking(), "utility", keep="personal-time")
            week = details("Мой график", self.my_schedule(), "utility", keep="personal-schedule")
            content += f'<div class="manager-tools">{start}{week}</div>'
        elif isinstance(self.user, Employee):
            with connect() as db:
                requests = db.execute("SELECT * FROM requests WHERE employee_id=? ORDER BY id DESC",
                                      (self.user.id,)).fetchall()
            if requests:
                values = [(f"{ABSENCE[row['type']]} · {span(date.fromisoformat(row['start']), date.fromisoformat(row['end']))}",
                           esc(STATUS[row["status"]] + (f" ({row['reason']})" if row["reason"] else ""))) for row in requests]
                content += details("Мои заявки", description_rows(values), "utility")
        return content

    def time_tracking(self):
        stamp = now()
        history = self.user.viewHistory()
        active = next((r for r in history if r.clockOutTime is None), None)
        schedule = self.user.viewSchedule(active.date if active else stamp.date())
        today_entries = [r for r in history if r.date == stamp.date()]
        latest = active or (today_entries[0] if today_entries else None)
        clock_live = "" if FIXED_NOW else "data-live-clock"
        clock = (f'<div class="clock-face"><strong {clock_live}>{stamp:%H:%M}</strong>'
                 f'<span>Плановое начало: {schedule.startTime:%H:%M}</span></div>')
        status = ""
        if latest and latest.isLate:
            expected = self.user.viewSchedule(latest.date).startTime
            shift_start = datetime.combine(latest.date, expected, latest.clockInTime.tzinfo)
            minutes = max(0, int((latest.clockInTime - shift_start).total_seconds() // 60))
            if minutes:
                status = f'<p class="clock-status late">⚠ Опоздание: {minutes} минут</p>'
        elif active:
            status = f'<p class="clock-status">Смена открыта с {active.clockInTime:%H:%M}</p>'
        controls = buttons(action("▶ Начать", "start", "green", disabled=active is not None),
                           action("▪ Завершить", "finish", "red", disabled=active is None))
        day_lines = []
        for row in reversed(today_entries):
            day_lines.append(f'<p>• {row.clockInTime:%H:%M} — Вход</p>')
            if row.clockOutTime:
                day_lines.append(f'<p>• {row.clockOutTime:%H:%M} — Выход · {hours(row.workedHours)}</p>')
        if not day_lines:
            day_lines.append("<p>Сегодня отметок нет.</p>")
        previous = [row for row in history if row.date < stamp.date()]
        summary = details("История за сегодня:", self.history_rows(previous), "previous-days") if previous else "<strong>История за сегодня:</strong>"
        return (f'{heading("Отметка рабочего времени")}{clock}{status}<div class="time-actions">{controls}</div>'
                f'<div class="daily-history">{summary}{"".join(day_lines)}</div>')

    def my_schedule(self):
        start = self.session.get("week_day", now().date())
        monday = start - timedelta(days=start.weekday())
        select_week = form("week", date_field("Дата в нужной неделе", "week_day", start),
                           action("Показать неделю", "week", submit=True))
        title = details(heading(f"График работы на {MONTHS[start.month - 1]} {start.year}"),
                        select_week, "schedule-heading")
        rows = []
        with connect() as db:
            for day in days_between(monday, monday + timedelta(days=6)):
                schedule = schedule_for(db, self.user.id, day)
                request = db.execute("""SELECT type FROM requests WHERE employee_id=? AND status='APPROVED'
                                     AND start<=? AND end>=?""", (self.user.id, day, day)).fetchone()
                if not schedule.is_workday(day) and not request:
                    continue
                if request:
                    shift = ABSENCE[request["type"]]
                else:
                    shift = f"{schedule.startTime:%H:%M} — {schedule.endTime:%H:%M}"
                    if schedule.breakMinutes:
                        begin = datetime.combine(day, schedule.startTime) + timedelta(hours=4)
                        end = min(begin + timedelta(minutes=schedule.breakMinutes), datetime.combine(day, schedule.endTime))
                        shift += (f" (перерыв {begin:%H:%M}-{end:%H:%M})" if begin < end
                                  else f" (перерыв {schedule.breakMinutes} мин)")
                rows.append(f'<p>{icon("calendar", 24)} {WEEKDAYS[day.weekday()]}, {day:%d.%m.%Y}<br>{shift}</p>')
        return f'<div class="week">{title}<div class="week-list">{"".join(rows)}</div></div>'

    def leave_request(self):
        choices = []
        selected = self.inputs.get("kind", AbsenceType.VACATION)
        for kind, label in ABSENCE.items():
            checked = " checked" if kind == selected else ""
            choices.append(f'<label><input type="radio" name="kind" value="{kind}"{checked}>'
                           f'<span class="choice">{icon(ABSENCE_ICONS[kind], 38)}{label}</span></label>')
        controls = f'<fieldset class="absence-types" aria-label="Тип отсутствия">{"".join(choices)}</fieldset>'
        for key, label in (("start", "Дата начала"), ("end", "Дата окончания")):
            try:
                value = read_date(self.inputs.get(key, ""))
            except ValueError:
                value = None
            controls += date_field(label, key, value)
        controls += field("Комментарий (необязательно)", "comment", value=self.inputs.get("comment", ""),
                          placeholder="Укажите причину или детали", required=False)
        return heading("Подача заявки на отсутствие") + form(
            "leave", controls, action(f'{icon("send", 21)} Отправить заявку', "leave", "green", submit=True)
        )

    def team_members(self):
        with connect() as db:
            return db.execute("""SELECT * FROM users WHERE department_id=? AND role!='hradmin' AND id!=?
                              ORDER BY id""", (self.user.department.id, self.user.id)).fetchall()

    def team_attendance(self):
        members = self.team_members()
        entries = self.user.viewTeamAttendance()
        today = now().date()
        with connect() as db:
            absences = {r["employee_id"]: r["type"] for r in db.execute(
                "SELECT employee_id,type FROM requests WHERE status='APPROVED' AND start<=? AND end>=?",
                (today, today))}
        cards, history = [], ""
        for member in members:
            rows = [row for row in entries if row.employee_id == member["id"]]
            last = next((r for r in rows if r.clockOutTime is None or r.date == today), None)
            color = "grey"
            if last and (last.clockOutTime is None or member["id"] not in absences):
                color = "red" if last.isLate else "green"
                label = ("Смена закрыта" if last.clockOutTime else
                         "⚠ Опоздание" if last.isLate else "На рабочем месте")
                status = f"{label} · Пришел в {last.clockInTime:%H:%M}"
            elif kind := absences.get(member["id"]):
                reason = {"VACATION": "В отпуске", "SICK_LEAVE": "На больничном", "DAY_OFF": "Отгул",
                          "BUSINESS_TRIP": "В командировке"}[kind]
                status = f'{icon(ABSENCE_ICONS[kind], 18)} {reason}'
            else:
                status = "Сегодня отметок нет"
            name = short_name(member)
            button = action(f'{icon("chart", 18)} История', "history", "blue small", target=member["id"])
            cards.append(card(name, f'<span class="attendance-status">{status}</span>', button, color=color))
            if member["id"] == self.session.get("attendance_id"):
                history = panel(f'{icon("history", 22)} История посещений — {esc(name)}',
                                self.history_rows([row for row in rows if row.clockOutTime]), "history-panel")
        department = self.user.department.name
        if department.startswith("Отдел "):
            department = "отдела " + department.removeprefix("Отдел ")
        contents = "".join(cards) or "<p>В отделе пока нет сотрудников.</p>"
        return f'{heading(f"Сотрудники {department}")}<div class="cards">{contents}</div>{history}'

    def history_rows(self, rows):
        if not rows:
            return "<p>Отметок пока нет.</p>"
        values = []
        for row in rows:
            end = row.clockOutTime
            if end:
                end_text = end.strftime("%H:%M" if end.date() == row.date else "%d.%m %H:%M")
                total = hours(row.workedHours, compact=True)
            else:
                end_text, total = "…", "В работе"
            css, late = (' class="late"', " ⚠") if row.isLate else ("", "")
            values.append((f"{row.date:%d.%m.%Y}", f'<span{css}>{row.clockInTime:%H:%M} — {end_text} · {total}{late}</span>'))
        return description_rows(values)

    def pending_requests(self):
        with connect() as db:
            return db.execute("""SELECT r.*, u.first_name, u.last_name FROM requests r
                              JOIN users u ON u.id=r.employee_id WHERE r.manager_id=?
                              AND u.department_id=? AND r.status='UNDER_REVIEW' ORDER BY r.id""",
                              (self.user.id, self.user.department.id)).fetchall()

    def decide(self, name, target, values):
        row = next((row for row in self.pending_requests() if str(row["id"]) == target), None)
        if name == "cancel_reject":
            self.session.pop("reject_id", None)
        elif row is None:
            raise ValueError("Заявка уже обработана или недоступна.")
        elif name == "reject_panel":
            self.toggle("reject_id", row["id"])
        else:
            request = LeaveRequest.from_row(row)
            if name == "approve":
                self.user.approveRequest(request)
                message = "Заявка утверждена."
            else:
                self.user.rejectRequest(request, values["reason"])
                message = "Заявка отклонена."
            self.session.pop("reject_id", None)
            return message

    def approvals(self):
        cards = []
        for row in self.pending_requests():
            req = LeaveRequest.from_row(row)
            if req.startDate == req.endDate:
                period = f"{req.startDate:%d.%m.%Y}"
                if req.type == AbsenceType.SICK_LEAVE:
                    period = f"с {period}"
            else:
                start = f"{req.startDate:%d.%m}"
                period = f"{start} — {req.endDate:%d.%m.%Y}"
            description = f"{ABSENCE[req.type]} · {period}"
            if req.comment:
                description = details(description, f'<p>{esc(req.comment)}</p>')
            controls = buttons(action("✓ Утвердить", "approve", "green small", target=req.id),
                               action("✕ Отклонить", "reject_panel", "red small", target=req.id))
            if self.session.get("reject_id") == req.id:
                rejection = field("Причина отклонения", "reason", value=self.inputs.get("reason", ""))
                controls += form("reject", rejection, buttons(action("Отклонить заявку", "reject", "red small", submit=True),
                                 action("Отмена", "cancel_reject", "grey small")), target=req.id)
            cards.append(card(short_name(row), description, controls, color="orange", symbol="register"))
        return heading("Заявки на согласование") + (
            f'<div class="cards">{"".join(cards)}</div>' if cards else "<p>Нет заявок на согласование.</p>"
        )

    def team_period(self):
        today = now().date()
        monday = today - timedelta(days=today.weekday())
        return self.session.get("team_period", (monday, monday + timedelta(days=6)))

    def team_schedule(self):
        _, schedules = lookup()
        start, end = self.team_period()
        fields = date_field("Начало периода", "plan_start", start) + date_field("Конец периода", "plan_end", end)
        chosen_period = details(f'<span class="period-control">{span(start, end)}</span>',
                                form("team_period", fields, action("Применить период", "team_period", submit=True)),
                                "period")
        cards = []
        with connect() as db:
            for member in self.team_members():
                name, member_id = short_name(member), member["id"]
                current = schedule_for(db, member_id, start)
                options = "".join(f'<option value="{sid}"{" selected" if sid == current.id else ""}>'
                                  f'{shift_label(schedule)}</option>' for sid, schedule in schedules.items())
                select = f'<select class="shift-select" name="shift_{member_id}" aria-label="График — {esc(name)}">{options}</select>'
                cards.append(card(name, select))
        content = form("save_plan", f'<div class="cards">{"".join(cards)}</div>',
                       action(f'{icon("save", 20)} Сохранить график', "save_plan", submit=True), css="") if cards else (
                           "<p>В отделе пока нет сотрудников.</p>")
        return f'{heading("Формирование графика смен")}<span class="period-label">Период</span>{chosen_period}{content}'

    def directory_action(self, name, target, values):
        if name == "cancel_employee":
            self.session.pop("directory_panel", None)
            return
        if name == "add":
            self.toggle("directory_panel", ("add", None))
            return
        row = next((r for r in self.user.manageEmployees() if str(r["id"]) == target), None)
        if name in {"profile", "edit"}:
            if row:
                self.toggle("directory_panel", (name, row["id"]))
            return
        if target and row is None:
            raise ValueError("Сотрудник не найден.")
        departments, _ = lookup()
        department_id = int(values["department"])
        role = row["role"] if row else values["role"]
        if department_id not in departments or role not in ROLE:
            raise ValueError("Выберите действующие отдел и роль.")
        save_employee(values["name"], row["login"] if row else values["login"], values.get("new_password", ""),
                      values["email"], department_id, values["position"], values.get("phone", ""),
                      role, row["id"] if row else None)
        self.session.pop("directory_panel", None)
        return "Данные сотрудника сохранены."

    def directory(self):
        search = (f'<div class="search">{icon("search", 22)}'
                  '<input data-search type="search" placeholder="Поиск по ФИО или отделу…" '
                  'aria-label="Поиск по ФИО или отделу"></div>')
        staff = self.user.manageEmployees()
        cards, drawer = [], ""
        opened, selected = self.session.get("directory_panel", ("", None))
        for row in staff:
            name = full_name(row)
            description = esc(f"{row['department']} · {ROLE[row['role']]} · {row['email']}")
            controls = buttons(action(f'{icon("eye", 14)} Профиль', "profile", "blue small", target=row["id"]),
                               action("✏︎ Редактировать", "edit", "amber small", target=row["id"]))
            cards.append(card(name, description, controls, symbol=ROLE_ICON[row["role"]],
                              attrs=f'data-employee="{esc(name + " " + row["department"])}"'))
            if row["id"] == selected:
                drawer = self.employee_profile(row) if opened == "profile" else self.employee_form(row)
        if opened == "add":
            drawer = self.employee_form(None)
        add = action(f'{icon("add", 23)} Добавить сотрудника', "add", "green add-employee")
        return (f'{heading("Все сотрудники компании")}{search}<p data-search-empty{" hidden" if cards else ""}>'
                f'Сотрудники не найдены.</p><div class="cards">{"".join(cards)}</div>{add}{drawer}')

    def employee_profile(self, row):
        with connect() as db:
            balance = get_balance(db, row["id"], now().year).getAvailableDays()
        values = [("ФИО:", full_name(row)), ("Должность:", row["position"]), ("Отдел:", row["department"]),
                  ("Email:", row["email"]), ("Телефон:", row["phone"] or "—"),
                  ("Дата найма:", date.fromisoformat(row["hired_on"]).strftime("%d.%m.%Y"))]
        if row["role"] != "hradmin":
            values.append(("Остаток отпуска:", vacation_days(balance)))
        return panel(f'{icon("profile", 22)} Профиль сотрудника — {esc(short_name(row))}',
                     description_rows((label, esc(value)) for label, value in values), "profile-panel")

    def employee_form(self, row):
        departments, _ = lookup()
        values = {"name": full_name(row), "position": row["position"], "department": row["department_id"],
                  "email": row["email"], "phone": row["phone"]} if row else {"department": next(iter(departments))}
        values.update(self.inputs)
        fields = field("ФИО", "name", value=values.get("name", ""))
        fields += field("Должность", "position", value=values.get("position", ""))
        fields += field("Отдел", "department", options=departments, value=int(values["department"]))
        fields += field("Email", "email", value=values.get("email", ""), kind="email")
        fields += field("Телефон", "phone", value=values.get("phone", ""), kind="tel", required=False)
        if row is None:
            fields += field("Логин", "login", value=values.get("login", ""))
            fields += field("Начальный пароль", "new_password", kind="password")
            fields += field("Роль", "role", value=values.get("role", "employee"), options=ROLE)
        controls = buttons(action(f'{icon("save-edit", 20)} Сохранить', "save_employee", "green", submit=True),
                           action("Отмена", "cancel_employee", "grey"))
        title = f"✏︎ Редактирование — {esc(short_name(row))}" if row else "Добавление сотрудника"
        return panel(title, form("save_employee", fields, controls, target=row["id"] if row else None), "edit-panel")

    def report_period(self):
        today = now().date()
        return self.session.get("report_period", (today.year, today.month))

    def report(self):
        year, month = self.report_period()
        return self.user.generateMonthlyTimesheet(month, year)

    def reports(self):
        year, month = self.report_period()
        period = span(date(year, month, 1), date(year, month, monthrange(year, month)[1]))
        picker = form("report_period", field("Месяц табеля", "month", value=f"{year}-{month:02}", kind="month"),
                      action("Сформировать табель", "report_period", submit=True))
        select_period = details(f'{icon("calendar", 19)} <span>Период: <b>{period}</b></span>', picker, "report-period")
        top = heading("Табель учёта рабочего времени") + select_period
        try:
            sheet = self.report()
        except ValueError as exc:
            return f'{top}<p class="notice error">{esc(exc)}</p>'
        if not sheet.records:
            return f'{top}<p>За выбранный период нет сотрудников для табеля.</p>'
        rows = "".join(f"<tr><td>{index}</td><td>{esc(record.employee_label)}</td>"
                       f"<td>{record.plannedHours:.2f}".rstrip("0").rstrip(".") + "</td>"
                       f"<td>{record.corrected_hours:.2f}".rstrip("0").rstrip(".") + "</td></tr>"
                       for index, record in enumerate(sheet.records, start=1))
        table = ('<table class="report-table"><thead><tr><th scope="col">№</th><th scope="col">ФИО</th>'
                 '<th scope="col">Норма</th><th scope="col">Факт</th></tr></thead>'
                 f'<tbody>{rows}</tbody></table>')
        workbook = b64encode(sheet.exportToExcel()).decode("ascii")
        download = (f'<a class="button teal" download="timesheet_{year}_{month:02}.xlsx" '
                    f'href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{workbook}">'
                    f'{icon("send", 21)} Excel</a>')
        bar = buttons(action("✏︎ Корректировка", "adjust_panel", "amber"), download)
        adjust = ""
        if self.session.get("adjust_open"):
            options = {r.id: r.full_name for r in sheet.records}
            record = next((r for r in sheet.records if str(r.id) == self.inputs.get("record")), sheet.records[0])
            fields = field("Сотрудник", "record", options=options, value=record.id)
            values = esc(dumps({r.id: r.corrected_hours for r in sheet.records}))
            fields = fields.replace('<select ', f'<select data-hours="{values}" ', 1)
            fields += field("Итоговые часы", "hours", value=self.inputs.get("hours", str(record.corrected_hours)))
            adjust = panel("Корректировка", form("adjust", fields,
                           action("Сохранить корректировку", "adjust", "green", submit=True)))
        return f'{top}{table}<div class="report-actions">{bar}</div>{adjust}'

    def schedule_settings(self):
        _, schedules = lookup()
        selected = self.session.schedule_id
        schedule = schedules[selected]
        choices = buttons(*(action(shift_label(s), "schedule_config", "blue small", target=sid)
                            for sid, s in schedules.items()))
        fields = field("Начало смены", "schedule_start", value=schedule.startTime.strftime("%H:%M"), kind="time")
        fields += field("Окончание смены", "schedule_end", value=schedule.endTime.strftime("%H:%M"), kind="time")
        fields += field("Перерыв, мин", "pause", value=schedule.breakMinutes, kind="number")
        return panel("Настроить типовой график", choices + form(
            "configure_schedule", fields, action("Сохранить график", "configure_schedule", submit=True),
            target=selected
        ))

    def settings(self):
        with connect() as db:
            current = {r["key"]: bool(r["enabled"]) for r in db.execute("SELECT * FROM settings")}
        toggles = []
        for key, (label, default) in SETTINGS.items():
            symbol, explanation = SETTINGS_TEXT[key]
            checked = " checked" if current.get(key, default) else ""
            toggles.append(f'<label class="setting"><span><strong>{icon(symbol, 19)} {label}</strong>'
                           f'<small>{explanation}</small></span><input type="checkbox" role="switch" '
                           f'name="{key}"{checked}></label>')
        return heading("Настройки системы") + form(
            "save_settings", "".join(toggles), action(f'{icon("save", 20)} Сохранить настройки', "save_settings", submit=True)
        )


def main():
    st.set_page_config(page_title="TimeTrackPro", layout="wide", initial_sidebar_state="collapsed")
    if "_seeded" not in st.session_state:
        seed()
        st.session_state._seeded = True
    WebUI().run()


if __name__ == "__main__":
    main()
