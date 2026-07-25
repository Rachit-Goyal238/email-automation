from services.config_loader import ConfigLoader
from services.excel_reader import ExcelReader
from extractors.audit_details import AuditDetailsExtractor

loader = ConfigLoader()

config = loader.load("tata_capital")

reader = ExcelReader("SY3001_Prime_Stockyard.xlsx")

reader.load()

sheet = reader.get_checklist_sheet()

extractor = AuditDetailsExtractor(sheet, config)

details = extractor.extract()

print(details)