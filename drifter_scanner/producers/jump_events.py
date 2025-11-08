"""
EVE Online jump event producer.
"""
import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from reactivex.subject import ReplaySubject
from reactivex.scheduler import EventLoopScheduler

from drifter_scanner.models.jump_event import JumpEvent


class JumpEvents:
    """Produces JumpEvent from EVE log files."""

    def __init__(self, log_dir=None):
        if log_dir is None:
            log_dir = Path.home() / "Documents" / "EVE" / "logs" / "Chatlogs"
        self.log_dir = Path(log_dir)
        self.file_positions = {}
        self.pattern = re.compile(r'\[\s*(.+?)\s*\].*Channel changed to Local\s*:\s*(.+)$')
        self.subject = ReplaySubject(buffer_size=1000)

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

    def process_line(self, line, char_id):
        """Extract timestamp and system name from line and emit JumpEvent."""
        match = self.pattern.search(line)
        if match:
            timestamp_str = match.group(1)
            system = match.group(2).strip()

            try:
                visited_at = datetime.strptime(timestamp_str, "%Y.%m.%d %H:%M:%S")
            except ValueError:
                visited_at = datetime.now()

            self.subject.on_next(JumpEvent(
                system=system,
                character_id=char_id,
                visited_at=visited_at
            ))

    def run_once(self):
        """Run one iteration of monitoring."""
        current_files = self.get_latest_local_files()
        for char_id, file_path in current_files.items():
            lines = self.read_new_lines(file_path)
            for line in lines:
                self.process_line(line, char_id)

    def start_monitoring(self, state):
        """Start the monitoring loop on a scheduler."""
        scheduler = EventLoopScheduler()

        def monitor_action(state_arg):
            try:
                if state.running:
                    self.run_once()
                else:
                    self.subject.on_completed()
                    scheduler.dispose()
            except Exception as e:
                self.subject.on_error(e)
                scheduler.dispose()

        scheduler.schedule_periodic(1.0, monitor_action)
        return scheduler

    def get_observable(self):
        """Get the observable that emits JumpEvent."""
        return self.subject
