import tkinter as tk
from tkinter import ttk


class ReportsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        month_frame = ttk.Frame(self)
        month_frame.pack(pady=10)

        ttk.Label(month_frame, text="Month:").pack(side=tk.LEFT)
        self.month_entry = ttk.Entry(month_frame)
        self.month_entry.pack(side=tk.LEFT, padx=5)

        self.generate_button = ttk.Button(month_frame, text="Generate Report")
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.report_text = tk.Text(self, height=20, width=60)
        self.report_text.pack(pady=10, padx=10, fill="both", expand=True)
