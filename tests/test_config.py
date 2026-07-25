from services.config_loader import ConfigLoader

loader = ConfigLoader()

print(loader.available_clients())

config = loader.load("tata_capital")

print(config["client"])