# utils/client_loader.py

import os
from dotenv import load_dotenv
from binance.client import Client

# Cargar variables de entorno
load_dotenv()

USE_TESTNET = os.getenv("USE_TESTNET", "false").lower() == "true"
BINANCE_TESTNET_SPOT_BASE_URL = "https://testnet.binance.vision/api"

# Seleccionar claves según entorno
if USE_TESTNET:
    API_KEY = os.getenv("BINANCE_API_KEY_TESTNET")
    API_SECRET = os.getenv("BINANCE_SECRET_KEY_TESTNET")
else:
    API_KEY = os.getenv("BINANCE_API_KEY_MAINNET")
    API_SECRET = os.getenv("BINANCE_SECRET_KEY_MAINNET")

if not API_KEY or not API_SECRET:
    raise RuntimeError("❌ Faltan claves de Binance en .env")

# Crear cliente Binance
client = Client(api_key=API_KEY, api_secret=API_SECRET, testnet=USE_TESTNET)

if USE_TESTNET:
    client.API_URL = BINANCE_TESTNET_SPOT_BASE_URL

# Utilidad para obtener precio actual
def get_price(symbol: str) -> float:
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])