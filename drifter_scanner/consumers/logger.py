"""
Event consumers that log to stderr.
"""
import sys


class StderrLogger:
    """Subscriber that logs events to stderr."""

    def on_next(self, event):
        print(event, file=sys.stderr)

    def on_error(self, error):
        print(f"Error: {error}", file=sys.stderr)

    def on_completed(self):
        pass
