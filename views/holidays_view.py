import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar


class HolidaysView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        self.holiday_cal = Calendar(
            left_frame, selectmode="day", firstweekday="sunday", showweeknumbers=True
        )
        self.holiday_cal.pack(pady=10, padx=10, fill="both", expand=True)

        add_frame = ttk.LabelFrame(right_frame, text="Add Holiday")
        add_frame.pack(pady=10, fill="x")

        ttk.Label(add_frame, text="Description:").pack(pady=5)
        self.holiday_desc_entry = ttk.Entry(add_frame)
        self.holiday_desc_entry.pack(pady=5, fill="x")

        self.add_button = ttk.Button(add_frame, text="Add Holiday")
        self.add_button.pack(pady=10)

        list_frame = ttk.LabelFrame(right_frame, text="Holiday List")
        list_frame.pack(pady=10, fill="both", expand=True)

        self.holiday_tree = ttk.Treeview(
            list_frame, columns=("Date", "Description"), show="headings"
        )
        self.holiday_tree.heading("Date", text="Date")
        self.holiday_tree.heading("Description", text="Description")
        self.holiday_tree.pack(pady=5, fill="both", expand=True)

        self.delete_button = ttk.Button(list_frame, text="Delete Selected")
        self.delete_button.pack(pady=5)
