import streamlit as st
import streamlit.components.v1 as components

from services.gmail_service import GmailService
from utils.session import get


def render():

    email = get()

    disabled = email["result"] is None

    if st.button(
        "📨 Generate Gmail Draft",
        type="primary",
        use_container_width=True,
        disabled=disabled
    ):

        try:

            credentials = st.session_state.get(
                "google_credentials"
            )

            if credentials is None:
                st.error("Please sign in with Google first.")
                return

            gmail = GmailService(credentials)

            gmail.create_draft(
                to=email["to"],
                cc=email["cc"],
                subject=email["subject"],
                html=email["result"]["html"],
                attachments=email["attachments"]
            )

            st.success(
                "✅ Gmail Draft Created Successfully!"
            )

            components.html(
                """
                <script>
                window.open(
                    "https://mail.google.com/mail/u/0/#drafts",
                    "_blank"
                );
                </script>
                """,
                height=0,
            )

        except Exception as e:

            st.exception(e)