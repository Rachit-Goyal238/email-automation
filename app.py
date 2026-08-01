import os
from dotenv import load_dotenv

load_dotenv()
import streamlit as st

from auth.gmail_auth import GmailAuthenticator

from utils.session import initialize

from ui import upload
from ui import preview
from ui import draft

OAUTH_URL = os.getenv("OAUTH_URL", "http://localhost:5000")
st.set_page_config(
    page_title="TATA Capital Audit Email Automation",
    page_icon="📧",
    layout="wide"
)

initialize()
auth = GmailAuthenticator()

credentials = auth.authenticate()

if credentials is None:

    st.title("Authentication Required")

    st.warning(
        "Please access the application using the company login URL."
    )

    st.link_button(
        "Login",
        f"{OAUTH_URL}/login"
    )

    st.stop()

st.title("📧 TATA Capital Audit Email Automation")

upload.render()

st.divider()

with st.expander(
    "👀 Preview Generated Email",
    expanded=False
):
    preview.render()

st.divider()

draft.render()