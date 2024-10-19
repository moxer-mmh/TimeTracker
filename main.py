import tkinter as tk
from tkinter import ttk
from views.daily_view import DailyView
from views.holidays_view import HolidaysView
from views.reports_view import ReportsView
from controllers.daily_controller import DailyController
from controllers.holidays_controller import HolidaysController
from controllers.reports_controller import ReportsController
from models.database import Database
from utils.logger import setup_logging


class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Time Tracker By MoXeR")
        self.root.geometry("800x600")

        self.logger = setup_logging()

        self.db = Database()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        self.daily_view = DailyView(self.notebook)
        self.holidays_view = HolidaysView(self.notebook)
        self.reports_view = ReportsView(self.notebook)

        self.daily_controller = DailyController(self.daily_view, self.db)
        self.holidays_controller = HolidaysController(self.holidays_view, self.db)
        self.reports_controller = ReportsController(self.reports_view, self.db)

        self.notebook.add(self.daily_view, text="Daily Entry")
        self.notebook.add(self.holidays_view, text="Holidays")
        self.notebook.add(self.reports_view, text="Reports")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
