"""
Log buffer for capturing application logs.
"""
import sys
from collections import deque
from threading import Lock


class LogBuffer:
    """Thread-safe buffer that captures stderr output."""

    def __init__(self, max_lines=1000):
        self.buffer = deque(maxlen=max_lines)
        self.lock = Lock()
        self.original_stderr = sys.stderr

    def write(self, text):
        """Write to buffer and original stderr."""
        self.original_stderr.write(text)
        self.original_stderr.flush()

        with self.lock:
            self.buffer.append(text)

    def flush(self):
        """Flush the original stderr."""
        self.original_stderr.flush()

    def get_logs(self):
        """Get all logs as a single string."""
        with self.lock:
            return ''.join(self.buffer)

    def install(self):
        """Redirect stderr to this buffer."""
        sys.stderr = self

    def uninstall(self):
        """Restore original stderr."""
        sys.stderr = self.original_stderr
