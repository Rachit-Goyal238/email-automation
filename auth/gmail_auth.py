import os
import requests
import streamlit as st

from google.oauth2.credentials import Credentials

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
OAUTH_URL = os.getenv("OAUTH_URL", "http://localhost:5000")


class GmailAuthenticator:

    def _create_credentials(self, token):

        credentials = Credentials(
            token=token["access_token"],
            refresh_token=token.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scopes=token["scope"].split(),
        )

        st.session_state["google_credentials"] = credentials

        return credentials

    def _exchange_token(self, token_id):

        response = requests.get(
            f"{OAUTH_URL}/token/{token_id}",
            timeout=10
        )

        if response.status_code != 200:
            return None

        token = response.json()

        return self._create_credentials(token)

    def authenticate(self):

        # Already authenticated in Streamlit
        if "google_credentials" in st.session_state:
            return st.session_state["google_credentials"]

        # ---------------------------------------------------
        # FIRST LOGIN (Google redirected back)
        # ---------------------------------------------------

        params = st.query_params

        token_id = params.get("token")

        if token_id:

            credentials = self._exchange_token(token_id)

            st.query_params.clear()

            return credentials

        # ---------------------------------------------------
        # RETURNING USER
        # ---------------------------------------------------

        try:

            status = requests.get(
                f"{OAUTH_URL}/status",
                timeout=5
            )

            if status.status_code != 200:
                return None

            authenticated = status.json()["authenticated"]

            if not authenticated:
                return None

            session_token = requests.get(
                f"{OAUTH_URL}/session-token",
                timeout=5
            )

            if session_token.status_code != 200:
                return None

            token_id = session_token.json()["token"]

            return self._exchange_token(token_id)

        except requests.exceptions.RequestException:

            st.error(
                "Unable to contact the authentication server."
            )

            return None