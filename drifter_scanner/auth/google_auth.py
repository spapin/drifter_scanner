"""
Google OAuth2 authentication for Google Sheets API.
"""
import sys
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleSheetsAuth:
    """Handles OAuth2 authentication for Google Sheets API."""

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, credentials_file: Path, token_file: Path = None):
        """Initialize the authentication handler.

        Args:
            credentials_file: Path to OAuth2 client credentials JSON file
            token_file: Path to store/load OAuth2 tokens (default: ~/.drifter_scanner/token.json)
        """
        self.credentials_file = credentials_file

        if token_file is None:
            self.token_file = Path.home() / ".drifter_scanner" / "token.json"
        else:
            self.token_file = token_file

        # Ensure token directory exists
        self.token_file.parent.mkdir(parents=True, exist_ok=True)

    def get_credentials(self):
        """Get or create OAuth2 credentials.

        Returns:
            Google OAuth2 credentials object

        Raises:
            FileNotFoundError: If credentials file doesn't exist
        """
        if not self.credentials_file.exists():
            raise FileNotFoundError(
                f"Credentials file not found: {self.credentials_file}\n"
                f"Download OAuth2 credentials from Google Cloud Console."
            )

        creds = None

        if self.token_file.exists():
            try:
                creds = Credentials.from_authorized_user_file(
                    str(self.token_file),
                    self.SCOPES
                )
            except Exception:
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    creds = self._run_oauth_flow()
            else:
                creds = self._run_oauth_flow()

            try:
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Could not save credentials: {e}", file=sys.stderr)

        return creds

    def _run_oauth_flow(self):
        """Run the OAuth2 flow in browser."""
        print("Opening browser for authentication...", file=sys.stderr)
        flow = InstalledAppFlow.from_client_secrets_file(
            str(self.credentials_file),
            self.SCOPES
        )
        return flow.run_local_server(port=0)
