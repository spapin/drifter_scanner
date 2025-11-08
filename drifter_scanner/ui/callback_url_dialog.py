"""
Dialog for setting the API callback URL.
"""
import json
import tkinter as tk
from pathlib import Path

CONFIG_PATH = Path.home() / ".drifter_scanner" / "config.json"


class CallbackUrlDialog:
    """Dialog window for viewing and setting the API callback URL."""

    def __init__(self):
        self.window = None

    def _load_config(self):
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH) as f:
                return json.load(f)
        return {}

    def _save_config(self, config):
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)

    def show(self):
        """Show the callback URL dialog."""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            self.window.focus_force()
            return

        config = self._load_config()
        current_url = config.get("api_url", "")

        self.window = tk.Tk()
        self.window.title("Set Callback URL")
        self.window.geometry("500x150")
        self.window.resizable(False, False)

        tk.Label(self.window, text="Callback URL:").pack(anchor="w", padx=10, pady=(10, 0))

        url_var = tk.StringVar(value=current_url)
        entry = tk.Entry(self.window, textvariable=url_var, width=70)
        entry.pack(padx=10, pady=5)
        entry.select_range(0, tk.END)
        entry.focus()

        status_label = tk.Label(self.window, text="", fg="green")
        status_label.pack(pady=(0, 5))

        def save():
            url = url_var.get().strip()
            config = self._load_config()
            if url:
                config["api_url"] = url
            else:
                config.pop("api_url", None)
            self._save_config(config)
            status_label.config(text="Saved! Restart to apply.")

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Save", command=save, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Close", command=self.window.destroy, width=10).pack(side="left", padx=5)

        self.window.mainloop()
