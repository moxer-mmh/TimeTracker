from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from utils.helpers import format_minutes


class ReportsController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        self.setup_handlers()

    def setup_handlers(self):
        self.view.generate_button.config(command=self.generate_report)
        self.view.month_entry.insert(0, datetime.now().strftime("%Y-%m"))

    def generate_report(self):
        try:
            month = self.view.month_entry.get()
            entries = self.db.get_monthly_entries(month)

            self.view.report_text.delete(1.0, tk.END)

            total_balance = 0
            report = f"Monthly Report for {month}\n\n"

            for entry in entries:
                report += f"Date: {entry.date}\n"
                report += (
                    f"Times: {entry.arrival_time} - {entry.lunch_start}, "
                    f"{entry.lunch_end} - {entry.departure_time}\n"
                )
                report += f"Daily Balance: {format_minutes(entry.balance)}\n\n"
                total_balance += entry.balance

            report += f"\nTotal Monthly Balance: {format_minutes(total_balance)}"
            self.view.report_text.insert(1.0, report)
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
