import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import database
from models import User


class MonthlyTimesheetTests(unittest.TestCase):
    def test_period_without_employees_does_not_save_empty_timesheet(self):
        with TemporaryDirectory() as tmp, patch.object(database, "DB_PATH", Path(tmp) / "test.sqlite3"):
            database.seed()
            admin = User.login("hradmin", "Demo1234")

            with self.assertRaisesRegex(ValueError, "нет сотрудников"):
                admin.generateMonthlyTimesheet(1, 2000)

            with database.connect() as db:
                self.assertIsNone(db.execute("SELECT id FROM timesheets").fetchone())

            sheet = admin.generateMonthlyTimesheet(1, 2026)
            with database.connect() as db:
                record_count = db.execute(
                    "SELECT COUNT(*) FROM timesheet_records WHERE sheet_id=?", (sheet.id,)
                ).fetchone()[0]
            self.assertGreater(record_count, 0)
            self.assertEqual(len(sheet.records), record_count)
