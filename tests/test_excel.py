from services.excel_reader import ExcelReader

reader = ExcelReader("SY3001_Prime_Stockyard.xlsx")

reader.load()

reader.validate()

print(reader.get_sheet_names())

print(reader.get_checklist_sheet().title)

print(reader.get_score_sheet().title)