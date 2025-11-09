"""
System tray menu management.
"""
import sys
import threading
from pathlib import Path
from PIL import Image
import pystray

from drifter_scanner.ui.logs_window import LogsWindow


class SystemTray:
    """Manages the system tray icon and menu."""

    def __init__(self, app_state, log_buffer=None):
        self.app_state = app_state
        self.log_buffer = log_buffer
        self.icon = None
        self.logs_window = None
        if log_buffer:
            self.logs_window = LogsWindow(log_buffer)

    def get_icon_path(self):
        """Get the path to the icon file."""
        module_dir = Path(__file__).parent.parent
        icon_path = module_dir / "resources" / "WCBR_logo.png"

        if not icon_path.exists():
            raise FileNotFoundError(f"Icon file not found: {icon_path}")

        return icon_path

    def load_icon_image(self):
        """Load the icon image."""
        icon_path = self.get_icon_path()
        return Image.open(icon_path)

    def on_logs(self, icon, item):
        """Handle logs action."""
        if self.logs_window:
            threading.Thread(target=self.logs_window.show, daemon=True).start()

    def on_quit(self, icon, item):
        """Handle quit action."""
        self.app_state.shutdown()
        icon.stop()

    def create_menu(self):
        """Create the system tray menu."""
        menu_items = []
        if self.log_buffer:
            menu_items.append(pystray.MenuItem("Logs", self.on_logs))
        menu_items.append(pystray.MenuItem("Quit", self.on_quit))
        return pystray.Menu(*menu_items)

    def stop(self):
        """Stop the system tray."""
        if self.icon:
            self.icon.stop()

    def run(self):
        """Run the system tray."""
        icon_image = self.load_icon_image()
        self.icon = pystray.Icon(
            "drifter_scanner",
            icon_image,
            "Drifter Scanner",
            menu=self.create_menu()
        )
        self.icon.run()
