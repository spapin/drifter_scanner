"""
EVE Online chat log monitor.
"""
import re
import time
from pathlib import Path
from collections import defaultdict


class ChatMonitor:
    """Monitors EVE chat logs for system changes."""

    def __init__(self, log_dir=None):
        if log_dir is None:
            log_dir = Path.home() / "Documents" / "EVE" / "logs" / "Chatlogs"
        self.log_dir = Path(log_dir)
        self.file_positions = {}
        self.pattern = re.compile(r'Channel changed to Local\s*:\s*(.+)$')

    def get_latest_local_files(self):
        """Get the latest Local log file for each character."""
        files = defaultdict(list)
        for f in self.log_dir.glob("Local_*.txt"):
            parts = f.stem.split('_')
            if len(parts) >= 3:
                char_id = parts[-1]
                files[char_id].append(f)

        return {char_id: max(file_list, key=lambda f: f.stat().st_mtime)
                for char_id, file_list in files.items()}

    def read_new_lines(self, file_path):
        """Read new lines from file since last position."""
        pos = self.file_positions.get(file_path, 0)
        try:
            with open(file_path, 'r', encoding='utf-16-le') as f:
                f.seek(pos)
                lines = f.readlines()
                self.file_positions[file_path] = f.tell()
                return lines
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []

    def process_line(self, line):
        """Extract and log system name from line."""
        match = self.pattern.search(line)
        if match:
            system = match.group(1).strip()
            print(system)

    def run_once(self):
        """Run one iteration of monitoring."""
        current_files = self.get_latest_local_files()
        for char_id, file_path in current_files.items():
            lines = self.read_new_lines(file_path)
            for line in lines:
                self.process_line(line)

    def run(self, state):
        """Run monitor loop."""
        print(f"Monitoring: {self.log_dir}")
        while state.running:
            self.run_once()
            time.sleep(1)
        print("Chat monitor stopped.")
