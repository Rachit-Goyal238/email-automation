import os
import requests
import streamlit as st

from google.oauth2.credentials import Credentials


CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
OAUTH_URL = os.getenv("OAUTH_URL", "http://localhost:5000")

class GmailAuthenticator:

    def authenticate(self):

        if "google_credentials" in st.session_state:
            return st.session_state["google_credentials"]

        params = st.query_params

        token_id = params.get("token")

        if not token_id:
            return None

        try:
            response = requests.get(
                f"{OAUTH_URL}/token/{token_id}",
                timeout=10
            )

            response.raise_for_status()

        except requests.exceptions.Timeout:
            st.error(
                "Authentication server timed out. Please try again."
            )
            st.stop()

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot reach the authentication server."
            )
            st.stop()

        except requests.exceptions.RequestException:
            st.error(
                "Authentication failed."
            )
            st.stop()

        if response.status_code != 200:
            return None

        token = response.json()

        credentials = Credentials(
            token=token["access_token"],
            refresh_token=token.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scopes=token["scope"].split()
        )

        st.session_state["google_credentials"] = credentials

        st.query_params.clear()

        return credentials