"""
Jump event data model.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class JumpEvent:
    """Event emitted when a character jumps to a system."""
    system: str
    character_id: str
    visited_at: datetime

    def __repr__(self):
        timestamp = self.visited_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.system} ({timestamp} UTC)"
