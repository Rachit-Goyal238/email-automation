from services.email_builder import EmailBuilder
from services.gmail_service import GmailService

EXCEL_FILE = "SY3001_Prime_Stockyard.xlsx"

builder = EmailBuilder(EXCEL_FILE)

result = builder.build()

gmail = GmailService()

with open(EXCEL_FILE, "rb") as f:

    excel_bytes = f.read()

draft = gmail.create_draft(

    to="rachitgoyal238@gmail.com",

    subject=result["subject"],

    html=result["html"],

    attachments=[

        {

            "filename": "SY3001_Prime_Stockyard.xlsx",

            "content": excel_bytes

        }

    ]

)

print()

print("Draft Created!")

print()

print(draft["id"])