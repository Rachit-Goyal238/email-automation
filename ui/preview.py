import streamlit as st

from utils.session import get


def render():

    email = get()

    if email["result"] is None:

        st.info("Upload an audit workbook to generate the email preview.")

        return

    st.components.v1.html(
        email["result"]["html"],
        height=1400,
        scrolling=True
    )