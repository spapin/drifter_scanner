"""
Event consumer that posts drifter connections to the drifterbearAA API.
"""
import sys
import requests
from drifter_scanner.models.drifter_connection import DrifterConnection


class ApiWriter:
    """Subscriber that POSTs DrifterConnection events to the drifterbearAA API."""

    def __init__(self, api_url: str):
        """Initialize the API writer.

        Args:
            api_url: Full callback URL including ?token= query parameter.
        """
        self.api_url = api_url

    def on_next(self, event):
        """Handle incoming DrifterConnection events."""
        if isinstance(event, DrifterConnection):
            wh_code = DrifterConnection.WORMHOLE_CODES.get(event.drifter_wormhole, "?")
            try:
                resp = requests.post(self.api_url, json={
                    "system_name": event.system,
                    "drifter_hole": wh_code,
                }, allow_redirects=False)
                if resp.status_code == 201:
                    print(f"[API] {event.system} -> {wh_code} (created)", file=sys.stderr)
                else:
                    print(f"[API] {event.system} -> {wh_code} (HTTP {resp.status_code}: {resp.text[:200]})", file=sys.stderr)
            except Exception as e:
                print(f"[API] Error posting connection: {e}", file=sys.stderr)

    def on_error(self, error):
        """Handle errors."""
        print(f"API writer error: {error}", file=sys.stderr)

    def on_completed(self):
        """Handle completion."""
        print("API writer completed", file=sys.stderr)
