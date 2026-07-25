from services.excel_reader import ExcelReader

from extractors.score_table import ScoreTableExtractor

reader = ExcelReader("SY3001_Prime_Stockyard.xlsx")

reader.load()

sheet = reader.get_score_sheet()

extractor = ScoreTableExtractor(sheet)

scores = extractor.extract()

print()

print(f"Found {len(scores)} rows\n")

for row in scores:

    print(row)