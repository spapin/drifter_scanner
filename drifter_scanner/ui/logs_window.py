"""
Logs window UI component.
"""
import tkinter as tk
from tkinter import scrolledtext


class LogsWindow:
    """Window for displaying application logs."""

    def __init__(self, log_buffer):
        self.log_buffer = log_buffer
        self.window = None
        self.text_area = None
        self.last_length = 0

    def refresh_logs(self):
        """Refresh the logs display."""
        if not self.window or not self.window.winfo_exists():
            return

        logs = self.log_buffer.get_logs()
        if len(logs) != self.last_length:
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, logs)
            self.text_area.see(tk.END)
            self.text_area.config(state=tk.DISABLED)
            self.last_length = len(logs)

        self.window.after(500, self.refresh_logs)

    def show(self):
        """Show the logs window."""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            self.window.focus_force()
            return

        self.window = tk.Tk()
        self.window.title("Drifter Scanner - Logs")
        self.window.geometry("800x600")

        self.text_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            width=100,
            height=30,
            font=("Consolas", 9)
        )
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)

        logs = self.log_buffer.get_logs()
        self.text_area.insert(tk.INSERT, logs)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.last_length = len(logs)

        self.window.after(500, self.refresh_logs)
        self.window.mainloop()
