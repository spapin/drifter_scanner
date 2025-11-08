"""
Simple state management for Drifter Scanner.
"""
import threading


class AppState:
    """Holds application state and provides control functions."""

    def __init__(self):
        self.running = False
        self.shutdown_event = threading.Event()

    def start(self):
        """Start the application."""
        self.running = True

    def shutdown(self):
        """Signal shutdown."""
        print("Shutting down...")
        self.running = False
        self.shutdown_event.set()
