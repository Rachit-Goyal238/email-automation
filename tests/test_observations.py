from services.config_loader import ConfigLoader
from services.excel_reader import ExcelReader
from extractors.observations import ObservationsExtractor

loader = ConfigLoader()
config = loader.load("tata_capital")

reader = ExcelReader("SY3001_Prime_Stockyard.xlsx")
reader.load()

sheet = reader.get_checklist_sheet()

extractor = ObservationsExtractor(sheet, config)

observations = extractor.extract()

print("=" * 120)
print(f"Total NO observations found: {len(observations)}")
print("=" * 120)

for i, obs in enumerate(observations, start=1):

    print(f"\nObservation #{i}")

    print(f"Rating Category     : {obs.rating_category}")
    print(f"Short Segmentation  : {obs.short_segmentation}")
    print(f"Observation         : {obs.observation}")
    print(f"Pending Status      : {obs.pending_status}")

    print("-" * 120)