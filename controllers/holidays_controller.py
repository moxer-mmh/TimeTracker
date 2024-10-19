from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from models.holiday import Holiday


class HolidaysController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        self.setup_handlers()
        self.load_holidays()

    def setup_handlers(self):
        self.view.add_button.config(command=self.add_holiday)
        self.view.delete_button.config(command=self.delete_holiday)

    def add_holiday(self):
        date = self.view.holiday_cal.get_date()
        desc = self.view.holiday_desc_entry.get()

        if not desc:
            messagebox.showerror("Error", "Please enter a description for the holiday")
            return

        try:
            date_obj = datetime.strptime(date, "%m/%d/%y").date()
            date_str = date_obj.strftime("%Y-%m-%d")

            holiday = Holiday(date_str, desc)
            if self.db.save_holiday(holiday):
                self.view.holiday_desc_entry.delete(0, tk.END)
                self.load_holidays()
                messagebox.showinfo("Success", "Holiday added successfully!")
            else:
                messagebox.showerror("Error", "Failed to add holiday")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding holiday: {str(e)}")

    def delete_holiday(self):
        selected = self.view.holiday_tree.selection()
        if not selected:
            return

        try:
            for item in selected:
                date = self.view.holiday_tree.item(item)["values"][0]
                if self.db.delete_holiday(date):
                    self.load_holidays()
                else:
                    messagebox.showerror("Error", f"Failed to delete holiday on {date}")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting holiday: {str(e)}")

    def load_holidays(self):
        for item in self.view.holiday_tree.get_children():
            self.view.holiday_tree.delete(item)

        holidays = self.db.get_holidays()
        for holiday in holidays:
            self.view.holiday_tree.insert(
                "", "end", values=(holiday.date, holiday.description)
            )
