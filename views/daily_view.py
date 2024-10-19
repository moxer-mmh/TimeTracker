import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar


class DailyView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True)

        self.cal = Calendar(
            left_frame, selectmode="day", firstweekday="sunday", showweeknumbers=True
        )
        self.cal.pack(pady=10, padx=10)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill="both", expand=True)

        entries_frame = ttk.LabelFrame(right_frame, text="Time Entries")
        entries_frame.pack(pady=10, padx=10, fill="x")

        self.time_entries = {}
        for label in ["Arrival Time:", "Lunch Start:", "Lunch End:", "Departure Time:"]:
            frame = ttk.Frame(entries_frame)
            frame.pack(pady=5, fill="x")
            ttk.Label(frame, text=label).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, padx=5)
            self.time_entries[label] = entry

        self.save_button = ttk.Button(right_frame, text="Save Entry")
        self.save_button.pack(pady=10)

        summary_frame = ttk.LabelFrame(right_frame, text="Balance Summary")
        summary_frame.pack(pady=10, padx=10, fill="x")

        self.daily_balance_label = ttk.Label(summary_frame, text="Daily Balance: 0:00")
        self.daily_balance_label.pack(pady=5)

        self.weekly_balance_label = ttk.Label(
            summary_frame, text="Weekly Balance: 0:00"
        )
        self.weekly_balance_label.pack(pady=5)

        self.monthly_balance_label = ttk.Label(
            summary_frame, text="Monthly Balance: 0:00"
        )
        self.monthly_balance_label.pack(pady=5)
