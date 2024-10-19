from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from models.time_entry import TimeEntry
from utils.helpers import format_minutes


class DailyController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        self.setup_handlers()

    def setup_handlers(self):
        self.view.cal.bind("<<CalendarSelected>>", self.on_date_select)
        self.view.save_button.config(command=self.save_daily_entry)

        today = datetime.now().date()
        self.view.cal.selection_set(today)
        self.check_weekend_and_holiday_and_update_entries(today)

    def on_date_select(self, event=None):
        selected_date = datetime.strptime(self.view.cal.get_date(), "%m/%d/%y").date()
        self.check_weekend_and_holiday_and_update_entries(selected_date)
        self.update_balance_summaries(selected_date)

    def check_weekend_and_holiday_and_update_entries(self, date_obj):
        is_weekend = date_obj.weekday() in [4, 5]
        is_holiday = self.db.is_holiday(date_obj.strftime("%Y-%m-%d"))
        should_disable = is_weekend or is_holiday

        for entry in self.view.time_entries.values():
            entry.delete(0, tk.END)
            entry.configure(state="disabled" if should_disable else "normal")

        if should_disable:
            reason = "holiday" if is_holiday else "weekend"
            self.view.daily_balance_label.config(text=f"Daily Balance: 0:00 ({reason})")
        else:
            self.load_entry(date_obj.strftime("%Y-%m-%d"))

    def load_entry(self, date_str):
        entry = self.db.get_time_entry(date_str)
        if entry:
            fields = ["Arrival Time:", "Lunch Start:", "Lunch End:", "Departure Time:"]
            values = [
                entry.arrival_time,
                entry.lunch_start,
                entry.lunch_end,
                entry.departure_time,
            ]
            for field, value in zip(fields, values):
                self.view.time_entries[field].delete(0, tk.END)
                if value:
                    self.view.time_entries[field].insert(0, value)

    def save_daily_entry(self):
        date = self.view.cal.get_date()
        date_obj = datetime.strptime(date, "%m/%d/%y").date()
        date_str = date_obj.strftime("%Y-%m-%d")

        if date_obj.weekday() in [4, 5]:
            messagebox.showerror("Error", "Cannot save entries for weekends!")
            return

        if self.db.is_holiday(date_str):
            messagebox.showerror("Error", "Cannot save entries for holidays!")
            return

        values = {
            "arrival_time": self.view.time_entries["Arrival Time:"].get(),
            "lunch_start": self.view.time_entries["Lunch Start:"].get(),
            "lunch_end": self.view.time_entries["Lunch End:"].get(),
            "departure_time": self.view.time_entries["Departure Time:"].get(),
        }

        if not all(values.values()):
            messagebox.showerror("Error", "All time fields must be filled!")
            return

        try:
            entry = TimeEntry(
                date=date_str,
                arrival_time=values["arrival_time"],
                lunch_start=values["lunch_start"],
                lunch_end=values["lunch_end"],
                departure_time=values["departure_time"],
            )
            entry.update_balance()

            if self.db.save_time_entry(entry):
                self.update_balance_summaries(date_obj)
                messagebox.showinfo("Success", "Entry saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save entry")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving entry: {str(e)}")

    def update_balance_summaries(self, current_date):
        try:
            entry = self.db.get_time_entry(current_date.strftime("%Y-%m-%d"))
            daily_balance = entry.balance if entry else 0

            current_weekday = current_date.weekday()
            days_from_sunday = (
                current_weekday - 6 if current_weekday >= 6 else current_weekday + 1
            )
            week_start = current_date - timedelta(days=days_from_sunday)
            week_end = week_start + timedelta(days=4)  # 5 days: Sunday through Thursday

            weekly_entries = self.db.get_monthly_entries(week_start.strftime("%Y-%m"))
            if week_start.month != week_end.month:
                weekly_entries.extend(
                    self.db.get_monthly_entries(week_end.strftime("%Y-%m"))
                )

            weekly_balance = sum(
                e.balance
                for e in weekly_entries
                if week_start
                <= datetime.strptime(e.date, "%Y-%m-%d").date()
                <= week_end
            )

            month_start = current_date.replace(day=1)
            if month_start.weekday() in [4, 5]:
                days_to_sunday = 7 - month_start.weekday()
                month_start += timedelta(days=days_to_sunday)

            month_entries = self.db.get_monthly_entries(current_date.strftime("%Y-%m"))
            monthly_balance = sum(
                e.balance
                for e in month_entries
                if datetime.strptime(e.date, "%Y-%m-%d").date() >= month_start
            )

            self.view.daily_balance_label.config(
                text=f"Daily Balance: {format_minutes(daily_balance)}"
            )
            self.view.weekly_balance_label.config(
                text=f"Weekly Balance: {format_minutes(weekly_balance)}"
            )
            self.view.monthly_balance_label.config(
                text=f"Monthly Balance: {format_minutes(monthly_balance)}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error updating balances: {str(e)}")
