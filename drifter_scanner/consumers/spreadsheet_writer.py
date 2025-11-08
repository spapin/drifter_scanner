"""
Event consumer that writes connections to Google Spreadsheet.
"""
import sys
import gspread
from drifter_scanner.models.drifter_connection import DrifterConnection
from drifter_scanner.auth.google_auth import GoogleSheetsAuth


class SpreadsheetWriter:
    """Subscriber that writes DrifterConnection events to Google Spreadsheet."""

    # SPREADSHEET_ID = "1P8pZO1aQGs0rkspS0Jo9gYo3H76dkv1biS4AdrlFARM"
    SPREADSHEET_ID = "169U0m2UGUjspxuSOTN8gqsJ1fMQ8Yi_q3UVw7aFqPng"
    WORKSHEET_NAME = "Drifter_Update"

    def __init__(self, auth_handler: GoogleSheetsAuth):
        """Initialize the spreadsheet writer using OAuth2.

        Args:
            auth_handler: GoogleSheetsAuth instance for authentication
        """
        self.auth_handler = auth_handler

        # Get credentials from auth handler
        credentials = self.auth_handler.get_credentials()

        # Connect to spreadsheet
        self.gc = gspread.authorize(credentials)
        self.spreadsheet = self.gc.open_by_key(self.SPREADSHEET_ID)
        self.worksheet = self.spreadsheet.worksheet(self.WORKSHEET_NAME)
        print(f"Connected to spreadsheet: {self.SPREADSHEET_ID}", file=sys.stderr)

    def on_next(self, event):
        """Handle incoming DrifterConnection events."""
        if isinstance(event, DrifterConnection):
            try:
                self._write_connection(event)
            except Exception as e:
                print(f"Error writing to spreadsheet: {e}", file=sys.stderr)

    def _write_connection(self, connection: DrifterConnection):
        """Write a connection to the spreadsheet."""
        # Get all values to find the row
        all_values = self.worksheet.get_all_values()

        # Find the row where column C matches the system name
        row_index = None
        for i, row in enumerate(all_values[1:], start=2):  # Start from row 2 (skip header)
            if len(row) >= 3 and row[2].strip() == connection.system:
                row_index = i
                break

        if row_index is None:
            print(f"System '{connection.system}' not found in spreadsheet", file=sys.stderr)
            return

        # Get the wormhole code (single letter)
        wh_code = connection.WORMHOLE_CODES.get(connection.drifter_wormhole, "?")

        # Format timestamp
        timestamp_str = connection.seen_at.strftime("%Y-%m-%d %H:%M:%S")

        # Update column D (wormhole code) and column E (timestamp)
        # Column D is index 4 (1-indexed), Column E is index 5
        self.worksheet.update_cell(row_index, 4, wh_code)
        self.worksheet.update_cell(row_index, 5, timestamp_str)

        print(f"[SPREADSHEET] Updated {connection.system} -> {wh_code} at {timestamp_str}", file=sys.stderr)

    def on_error(self, error):
        """Handle errors."""
        print(f"Spreadsheet error: {error}", file=sys.stderr)

    def on_completed(self):
        """Handle completion."""
        print("Spreadsheet writer completed", file=sys.stderr)
