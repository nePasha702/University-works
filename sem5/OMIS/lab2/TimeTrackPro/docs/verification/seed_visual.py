"""Create one fresh SQLite database for a Lab 1 wireframe scenario."""

import argparse
import os
from datetime import date, datetime, time, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

FIXED_NOW = "2026-11-18T20:52:00"
TODAY = date.fromisoformat(FIXED_NOW[:10])


def seed(path, scenario):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb"):
        pass
    os.environ["TIMETRACKPRO_DB"] = str(path)
    os.environ["TIMETRACKPRO_FIXED_NOW"] = FIXED_NOW
    from database import SCHEMA, TZ, connect, hash_password

    with connect() as db:
        db.executescript(SCHEMA)
        db.executemany("INSERT INTO departments VALUES(?,?)",
                       [(1, "Отдел продаж"), (2, "Отдел разработки"), (3, "HR-отдел")])
        db.executemany("INSERT INTO schedules VALUES(?,?,?,?,?,?)", [
            (1, "FIVE_DAY", "09:00", "18:00", 8, 60),
            (2, "SHIFT_WORK", "10:00", "19:00", 8, 60),
            (3, "FLEXIBLE", "08:30", "17:30", 8, 60),
            (4, "FIVE_DAY", "09:00", "17:00", 7, 60),
        ])
        sales = scenario in {"manager", "schedule", "dashboard"}
        people = [
            (1, "Иван Иванович", "Иванов", "employee", "ivanov", 1 if sales else 2,
             "employee", "Разработчик", 1, "+7 (900) 123-45-67"),
            (2, "Петр Петрович", "Петров", "manager", "petrov", 1,
             "manager", "Руководитель отдела", 1, ""),
            (3, "Анна Андреевна", "Смирнова", "hradmin", "smirnova", 3,
             "hradmin", "Администратор", 1, ""),
        ]
        if sales or scenario == "reports":
            people.append((4, "Сергей Сергеевич", "Сидоров", "sidorov", "sidorov", 1,
                           "employee", "Менеджер по продажам", 1, ""))
        if sales:
            people.append((5, "Кирилл Кириллович", "Козлов", "kozlov", "kozlov", 1,
                           "employee", "Специалист", 2, ""))
        if scenario in {"manager", "dashboard"}:
            people.append((6, "Николай Николаевич", "Новиков", "novikov", "novikov", 1,
                           "employee", "Специалист", 1, ""))
        for ident, first, last, login, mail, dep, role, position, schedule, phone in people:
            db.execute("""INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                       (ident, first, last, login, hash_password("Demo1234"), f"{mail}@company.ru",
                        dep, role, position, schedule, phone, "2023-03-15"))
        if scenario == "dashboard":
            db.execute("INSERT INTO schedules VALUES(5,'FLEXIBLE','09:30','18:30',8,60)")
            password = hash_password("Demo1234")
            db.executemany("""INSERT INTO users VALUES(?,?,?, ?,?,?, ?,?,?,?,?,'2023-03-15')""", [
                (ident, "Сотрудник", f"Учебный {ident}", f"sample{ident}", password, f"sample{ident}@company.ru",
                 1 if ident <= 10 else 2, "employee", "Специалист", 1, "") for ident in range(7, 147)
            ])
        db.execute("INSERT INTO balances(employee_id,year,total,used) VALUES(1,2026,24,10)")
        db.executemany("INSERT INTO settings VALUES(?,?)", [
            ("email", 1), ("reminders", 1), ("overtime", 0), ("two_factor", 0), ("turnstiles", 1),
        ])

        def entry(employee, day, start, end=None, hours=0, late=False):
            def stamp(value):
                return datetime.combine(day, time.fromisoformat(value), TZ).isoformat() if value else None

            db.execute("""INSERT INTO time_entries(employee_id,day,clock_in,clock_out,break_minutes,late,hours)
                       VALUES(?,?,?,?,60,?,?)""", (employee, day, stamp(start), stamp(end), late, hours))

        if scenario in {"employee", "time"}:
            db.execute("INSERT INTO planned_days VALUES(?,?,?)", (1, "2026-11-20", 4))
        if scenario == "employee":
            entry(1, TODAY, "09:00", "16:30", 6.5)
        if scenario == "time":
            entry(1, TODAY, "09:15", late=True)
        if scenario in {"manager", "dashboard"}:
            for day, start, end, hours in [
                (8, "09:00", "18:00", 8), (9, "09:00", "18:00", 8), (10, "09:20", "18:00", 7 + 2 / 3),
                (11, "08:55", "18:10", 8.25), (12, "09:00", "18:00", 8),
            ]:
                entry(1, date(2026, 11, day), start, end, hours, day == 10)
            entry(1, TODAY, "09:00")
            entry(4, TODAY, "08:45")
            db.execute("INSERT INTO planned_days VALUES(?,?,1)", (5, TODAY))
            entry(5, TODAY, "09:30", late=True)
            db.executemany("""INSERT INTO requests(employee_id,manager_id,type,start,end,status,comment)
                           VALUES(?,2,?,?,?,?, '')""", [
                (4, "VACATION", "2026-11-10", "2026-11-20", "UNDER_REVIEW"),
                (5, "DAY_OFF", "2026-11-05", "2026-11-05", "UNDER_REVIEW"),
                (6, "SICK_LEAVE", "2026-11-03", "2026-11-03", "UNDER_REVIEW"),
                (6, "SICK_LEAVE", "2026-11-16", "2026-11-20", "APPROVED"),
            ])
        if scenario == "dashboard":
            for ident in (7, 8, 9):
                entry(ident, TODAY, "09:00")
        if scenario == "reports":
            first = date(2026, 11, 1)
            working_days = [first + timedelta(days=i) for i in range(30) if (first + timedelta(days=i)).weekday() < 5]
            for employee, daily_hours in ((1, [8] * 19 + [6]), (4, [8] * 21), (2, [8] * 20)):
                db.execute("INSERT INTO planned_days VALUES(?,?,2)", (employee, working_days[0]))
                for day, total in zip(working_days, daily_hours):
                    entry(employee, day, "09:00", f"{10 + total:02d}:00", total)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("scenario", choices=["employee", "time", "manager", "schedule", "reports", "dashboard"])
    args = parser.parse_args()
    seed(args.path, args.scenario)
    print(f"TIMETRACKPRO_DB={args.path.resolve()}")
    print(f"TIMETRACKPRO_FIXED_NOW={FIXED_NOW}")
