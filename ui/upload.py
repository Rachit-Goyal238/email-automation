import streamlit as st

from services.email_builder import EmailBuilder
from utils.session import get


def render():

    email = get()

    st.subheader("Upload Workbook")

    st.selectbox(
        "Client",
        [
            "TATA Capital"
        ],
        disabled=True
    )

    uploaded = st.file_uploader(
        "Upload Audit Workbook",
        type=["xlsx"]
    )

    additional_files = st.file_uploader(
        "Additional Attachments",
        accept_multiple_files=True
    )

    if uploaded is None:
        return

    # Prevent rebuilding every rerun
    if (
        email["result"] is None
        or email["filename"] != uploaded.name
    ):

        with st.spinner("Generating Email Preview..."):

            builder = EmailBuilder(uploaded)

            result = builder.build()

        email["result"] = result
        email["subject"] = result["subject"]

        email["filename"] = uploaded.name
        email["file_bytes"] = uploaded.getvalue()

    # Store additional attachments
    attachments = []

    if additional_files:

        for file in additional_files:

            attachments.append(
                {
                    "filename": file.name,
                    "content": file.read()
                }
            )

    email["attachments"] = attachments

    st.divider()

    st.subheader("Email Details")

    email["subject"] = st.text_input(
        "Subject",
        value=email["subject"]
    )

    col1, col2 = st.columns(2)

    with col1:

        email["to"] = st.text_input(
            "To",
            value=email["to"],
            placeholder="recipient@example.com"
        )

    with col2:

        email["cc"] = st.text_input(
            "CC",
            value=email["cc"],
            placeholder="manager@example.com"
        )

    if additional_files:

        st.divider()

        st.markdown("### Attached Files")

        for file in additional_files:

            size = file.size / (1024 * 1024)

            st.success(
                f"📎 {file.name} ({size:.2f} MB)"
            )