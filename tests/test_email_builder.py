from services.email_builder import EmailBuilder

builder = EmailBuilder("SY3001_Prime_Stockyard.xlsx")

result = builder.build()

print(result["subject"])

print(result["score_summary"])

print(f"Observations: {len(result['observations'])}")

print(f"Score Rows: {len(result['score_table'])}")

with open("preview.html", "w", encoding="utf-8") as f:
    f.write(result["html"])

print("preview.html generated successfully.")