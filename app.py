import streamlit as st

from utils.session import initialize

from ui import upload
from ui import preview
from ui import draft


st.set_page_config(
    page_title="TATA Capital Audit Email Automation",
    page_icon="📧",
    layout="wide"
)

initialize()

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