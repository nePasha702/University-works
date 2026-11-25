import hashlib
import hmac
import os
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


TZ = ZoneInfo("Europe/Minsk")
DEFAULT_DB_PATH = Path(__file__).with_name("timetrack.sqlite3")
DB_PATH = Path(os.environ.get("TIMETRACKPRO_DB", DEFAULT_DB_PATH))
FIXED_NOW = os.environ.get("TIMETRACKPRO_FIXED_NOW")
sqlite3.register_adapter(date, date.isoformat)


def now():
    if FIXED_NOW:
        if DB_PATH.resolve() == DEFAULT_DB_PATH.resolve():
            raise ValueError("Для фиксированного времени укажите отдельную базу TIMETRACKPRO_DB.")
        return datetime.fromisoformat(FIXED_NOW).replace(tzinfo=TZ)
    return datetime.now(TZ)


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 300_000)
    return f"{salt}:{hashed.hex()}"


def check_password(password, stored):
    return hmac.compare_digest(hash_password(password, stored.split(":")[0]), stored)


@contextmanager
def connect():
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        with db:
            yield db
    finally:
        db.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY, type TEXT NOT NULL, start TEXT NOT NULL,
    end TEXT NOT NULL, hours REAL NOT NULL, break_minutes INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, email TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(id), role TEXT NOT NULL,
    position TEXT NOT NULL, schedule_id INTEGER NOT NULL REFERENCES schedules(id),
    phone TEXT NOT NULL DEFAULT '', hired_on TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS balances (
    id INTEGER PRIMARY KEY, employee_id INTEGER NOT NULL REFERENCES users(id),
    year INTEGER NOT NULL, total INTEGER NOT NULL, used INTEGER NOT NULL DEFAULT 0,
    UNIQUE(employee_id, year)
);
CREATE TABLE IF NOT EXISTS time_entries (
    id INTEGER PRIMARY KEY, employee_id INTEGER NOT NULL REFERENCES users(id),
    day TEXT NOT NULL, clock_in TEXT NOT NULL, clock_out TEXT,
    break_minutes INTEGER NOT NULL, late INTEGER NOT NULL, hours REAL NOT NULL DEFAULT 0
);
CREATE UNIQUE INDEX IF NOT EXISTS one_open_shift
    ON time_entries(employee_id) WHERE clock_out IS NULL;
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY, employee_id INTEGER NOT NULL REFERENCES users(id),
    manager_id INTEGER NOT NULL REFERENCES users(id),
    type TEXT NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL,
    status TEXT NOT NULL, comment TEXT NOT NULL, reason TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id),
    message TEXT NOT NULL, is_read INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS planned_days (
    employee_id INTEGER NOT NULL REFERENCES users(id), day TEXT NOT NULL,
    schedule_id INTEGER NOT NULL REFERENCES schedules(id), PRIMARY KEY(employee_id, day)
);
CREATE TABLE IF NOT EXISTS timesheets (
    id INTEGER PRIMARY KEY, month INTEGER NOT NULL, year INTEGER NOT NULL,
    admin_id INTEGER NOT NULL REFERENCES users(id), is_closed INTEGER NOT NULL DEFAULT 0,
    UNIQUE(year, month)
);
CREATE TABLE IF NOT EXISTS timesheet_records (
    id INTEGER PRIMARY KEY, sheet_id INTEGER NOT NULL REFERENCES timesheets(id),
    employee_id INTEGER NOT NULL REFERENCES users(id), planned REAL NOT NULL,
    actual REAL NOT NULL, absence_days INTEGER NOT NULL, adjustment REAL NOT NULL DEFAULT 0,
    overtime REAL NOT NULL, UNIQUE(sheet_id, employee_id)
);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, enabled INTEGER NOT NULL);
"""

SETTINGS = {
    "email": ("Уведомления по email", False),
    "reminders": ("Напоминания об отметке", False),
    "overtime": ("Автоматический расчет переработок", True),
    "two_factor": ("Двухфакторная аутентификация", False),
    "turnstiles": ("Интеграция с турникетами", False),
}


def notify(db, user_id, message):
    db.execute("INSERT INTO notifications(user_id, message, created_at) VALUES(?,?,?)",
               (user_id, message, now().isoformat()))


def seed():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as db:
        db.executescript(SCHEMA)
        db.execute("BEGIN IMMEDIATE")
        db.executemany("INSERT OR IGNORE INTO settings VALUES(?,?)",
                       [(key, default) for key, (_, default) in SETTINGS.items()])
        if db.execute("SELECT 1 FROM departments LIMIT 1").fetchone():
            return
        db.executemany("INSERT INTO departments(name) VALUES(?)",
                       [(name,) for name in ("Отдел продаж", "Отдел разработки", "HR-отдел")])
        db.executemany("INSERT INTO schedules(type,start,end,hours,break_minutes) VALUES(?,?,?,?,?)", [
            ("FIVE_DAY", "09:00", "18:00", 8, 60),
            ("SHIFT_WORK", "10:00", "19:00", 8, 60),
            ("FLEXIBLE", "08:30", "17:30", 8, 60),
        ])
        accounts = [
            ("Иван Иванович", "Иванов", "employee", 1, "employee", "Специалист", 1),
            ("Пётр Петрович", "Петров", "manager", 1, "manager", "Руководитель отдела", 1),
            ("Анна Андреевна", "Смирнова", "hradmin", 3, "hradmin", "HR-администратор", 1),
            ("Сергей Сергеевич", "Сидоров", "sidorov", 1, "employee", "Менеджер по продажам", 1),
            ("Кирилл Кириллович", "Козлов", "kozlov", 1, "employee", "Специалист", 2),
            ("Наталья Николаевна", "Новикова", "novikova", 2, "employee", "Разработчик", 1),
            ("Ольга Олеговна", "Орлова", "devmanager", 2, "manager", "Руководитель отдела", 1),
        ]
        for first, last, login, dept, role, position, schedule in accounts:
            db.execute("""INSERT INTO users(first_name,last_name,login,password_hash,email,
                       department_id,role,position,schedule_id,hired_on) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                       (first, last, login, hash_password("Demo1234"), f"{login}@example.test",
                        dept, role, position, schedule, "2023-03-15"))
        today = now().date()
        db.executemany("INSERT INTO balances(employee_id,year,total,used) VALUES(?,?,?,?)",
                       [(i, today.year, 24, 10 if i == 1 else 0) for i in (1, 2, 4, 5, 6, 7)])
        for days_back in (1, 2, 3):
            day = today - timedelta(days=days_back)
            for employee_id, start, end in ((1, 9, 18), (4, 9, 18), (5, 10, 19)):
                stamp = datetime.combine(day, datetime.min.time(), TZ)
                db.execute("""INSERT INTO time_entries(employee_id,day,clock_in,clock_out,
                           break_minutes,late,hours) VALUES(?,?,?,?,60,0,8)""",
                           (employee_id, day.isoformat(), (stamp+timedelta(hours=start)).isoformat(),
                            (stamp+timedelta(hours=end)).isoformat()))
        start = today + timedelta(days=7)
        db.execute("""INSERT INTO requests(employee_id,manager_id,type,start,end,status,comment)
                   VALUES(4,2,'VACATION',?,?,'UNDER_REVIEW','Плановый отпуск')""",
                   (start.isoformat(), (start + timedelta(days=2)).isoformat()))
        notify(db, 2, "Сидоров Сергей Сергеевич подал заявку на отпуск.")
