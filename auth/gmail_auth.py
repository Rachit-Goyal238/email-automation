from pathlib import Path

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose"
]


class GmailAuthenticator:

    def __init__(self):
        self.credentials_path = Path("credentials.json")
        self.token_path = Path("token.json")

    def authenticate(self):

        creds = None

        # Load saved token
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(
                str(self.token_path),
                SCOPES
            )

        # Refresh expired token
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())

            except RefreshError:
                # Refresh token has been revoked/expired.
                # Delete the invalid token so a new OAuth flow can begin.
                if self.token_path.exists():
                    self.token_path.unlink()

                creds = None

        # First login or token refresh failed
        if not creds or not creds.valid:

            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.credentials_path),
                SCOPES
            )

            creds = flow.run_local_server(port=0)

            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return creds