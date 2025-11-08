"""
Drifter Scanner - Main Daemon
"""
import sys
import threading
from drifter_scanner.state import AppState
from drifter_scanner.system_tray import SystemTray
from drifter_scanner.monitor import ChatMonitor


class DrifterScanner:
    """Main daemon class for Drifter Scanner."""

    def __init__(self):
        self.state = AppState()
        self.monitor = ChatMonitor()

    def run(self):
        """Run the daemon with system tray."""
        print("Starting Drifter Scanner daemon...")
        self.state.start()

        # Start system tray in a daemon thread
        tray = SystemTray(self.state)
        tray_thread = threading.Thread(
            target=tray.run,
            daemon=True,
            name="SystemTray"
        )
        tray_thread.start()

        # Run the chat monitor
        try:
            self.monitor.run(self.state)
        except KeyboardInterrupt:
            print("\nReceived interrupt signal...")
            self.state.shutdown()

        print("Drifter Scanner stopped.")


def main():
    """Main entry point for the daemon."""
    daemon = DrifterScanner()
    daemon.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
