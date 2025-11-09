"""
Drifter Scanner - Main Application

Entry point and orchestration for the Drifter Scanner.
Wires producers to consumers and manages application lifecycle.
"""
import sys
import threading
from pathlib import Path

from drifter_scanner.state import AppState
from drifter_scanner.producers.jump_events import JumpEvents
from drifter_scanner.consumers.logger import StderrLogger
from drifter_scanner.consumers.spreadsheet_writer import SpreadsheetWriter
from drifter_scanner.auth.google_auth import GoogleSheetsAuth
from drifter_scanner.ui.system_tray import SystemTray
from drifter_scanner.ui.log_buffer import LogBuffer
from drifter_scanner.operators.drifter_connections import detect_drifter_connections


class DrifterScanner:
    """Main application class for Drifter Scanner."""

    def __init__(self):
        self.state = AppState()
        self.jump_events = JumpEvents()
        self.scheduler = None
        self.tray = None
        self.log_buffer = LogBuffer()
        self.log_buffer.install()

    def _start_workers(self):
        """Start all background workers."""
        jump_stream = self.jump_events.get_observable()

        logger = StderrLogger()
        jump_stream.subscribe(logger)

        drifter_connections = jump_stream.pipe(detect_drifter_connections())

        def init_spreadsheet_writer():
            credentials_file = Path(__file__).parent / "auth" / "credentials.json"
            try:
                auth_handler = GoogleSheetsAuth(credentials_file)
                spreadsheet_writer = SpreadsheetWriter(auth_handler)
                drifter_connections.subscribe(spreadsheet_writer)
                print("Spreadsheet writer enabled", file=sys.stderr)
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"Spreadsheet writer error: {e}", file=sys.stderr)

        threading.Thread(target=init_spreadsheet_writer, daemon=True).start()
        self.scheduler = self.jump_events.start_monitoring(self.state)

    def _cleanup(self):
        """Clean up resources."""
        self.state.shutdown()
        if self.scheduler:
            self.scheduler.dispose()
        self.log_buffer.uninstall()

    def run(self):
        """Run the application."""
        self.state.start()
        self._start_workers()

        self.tray = SystemTray(self.state, self.log_buffer)
        tray_thread = threading.Thread(target=self.tray.run, daemon=False)
        tray_thread.start()

        try:
            while tray_thread.is_alive():
                tray_thread.join(timeout=1.0)
        except KeyboardInterrupt:
            print("\nCtrl+C detected", file=sys.stderr)
            self.tray.stop()
            tray_thread.join()

        self._cleanup()


def main():
    """Main entry point for the application."""
    app = DrifterScanner()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
