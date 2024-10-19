import sqlite3
import logging
from pathlib import Path
import os
from .time_entry import TimeEntry
from .holiday import Holiday


class Database:
    def __init__(self):
        self.logger = logging.getLogger("TimeTracker.Database")
        self.conn = None
        self.cursor = None
        self.connect()
        self.init_tables()

    def get_db_path(self):
        app_data = Path(os.getenv("LOCALAPPDATA", str(Path.home())))
        db_dir = app_data / "TimeTracker" / "data"
        db_dir.mkdir(parents=True, exist_ok=True)
        return str(db_dir / "timetracker.db")

    def connect(self):
        try:
            db_path = self.get_db_path()
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.logger.info(f"Connected to database at: {db_path}")
        except Exception as e:
            self.logger.error(f"Database connection error: {str(e)}")
            raise

    def init_tables(self):
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS time_entries (
                    date TEXT,
                    arrival_time TEXT,
                    lunch_start TEXT,
                    lunch_end TEXT,
                    departure_time TEXT,
                    balance INTEGER,
                    PRIMARY KEY (date)
                )
            """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS holidays (
                    date TEXT PRIMARY KEY,
                    description TEXT
                )
            """
            )
            self.conn.commit()
            self.logger.info("Database tables initialized successfully")
        except Exception as e:
            self.logger.error(f"Database initialization error: {str(e)}")
            raise

    def save_time_entry(self, entry):
        try:
            self.cursor.execute(
                """
                INSERT OR REPLACE INTO time_entries 
                (date, arrival_time, lunch_start, lunch_end, departure_time, balance)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    entry.date,
                    entry.arrival_time,
                    entry.lunch_start,
                    entry.lunch_end,
                    entry.departure_time,
                    entry.balance,
                ),
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error saving time entry: {str(e)}")
            return False

    def get_time_entry(self, date):
        try:
            self.cursor.execute(
                """
                SELECT * FROM time_entries WHERE date = ?
            """,
                (date,),
            )
            entry = self.cursor.fetchone()
            if entry:
                return TimeEntry(*entry)
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving time entry: {str(e)}")
            return None

    def save_holiday(self, holiday):
        try:
            self.cursor.execute(
                """
                INSERT INTO holidays (date, description)
                VALUES (?, ?)
            """,
                (holiday.date, holiday.description),
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error saving holiday: {str(e)}")
            return False

    def delete_holiday(self, date):
        try:
            self.cursor.execute("DELETE FROM holidays WHERE date = ?", (date,))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting holiday: {str(e)}")
            return False

    def get_holidays(self):
        try:
            self.cursor.execute("SELECT date, description FROM holidays ORDER BY date")
            return [Holiday(*row) for row in self.cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Error retrieving holidays: {str(e)}")
            return []

    def is_holiday(self, date):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM holidays WHERE date = ?", (date,))
            return self.cursor.fetchone()[0] > 0
        except Exception as e:
            self.logger.error(f"Error checking holiday: {str(e)}")
            return False

    def get_monthly_entries(self, month):
        try:
            self.cursor.execute(
                """
                SELECT *
                FROM time_entries
                WHERE date LIKE ?
                AND strftime('%w', date) NOT IN ('5', '6')  -- Friday=5, Saturday=6 in SQLite
                AND date NOT IN (SELECT date FROM holidays)
                ORDER BY date
                """,
                (f"{month}%",),
            )
            return [TimeEntry(*entry) for entry in self.cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Error retrieving monthly entries: {str(e)}")
            return []
