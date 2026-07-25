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

            gmail = GmailService()

            attachments = email["attachments"]

            gmail.create_draft(
                to=email["to"],
                cc=email["cc"],
                subject=email["subject"],
                html=email["result"]["html"],
                attachments=attachments
            )

            st.success("✅ Gmail Draft Created Successfully!")

            st.info("Opening Gmail Drafts...")

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

            st.error(str(e))