"""
Drifter connection data model.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DrifterConnection:
    """Represents a connection to a drifter wormhole system."""

    # Mapping of drifter wormholes to short codes (class variable)
    WORMHOLE_CODES = {
        "Sentinel MZ": "S",
        "Liberated Barbican": "B",
        "Sanctified Vidette": "V",
        "Conflux Eyrie": "C",
        "Azdaja Redoubt": "R"
    }

    system: str
    drifter_wormhole: str
    seen_at: datetime

    def __repr__(self):
        wh_code = self.WORMHOLE_CODES.get(self.drifter_wormhole, "?")
        timestamp = self.seen_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.system} -> {wh_code} ({timestamp} UTC)"
