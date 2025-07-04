# utils/client_loader.py

import os
from binance.client import Client

# SOLO cargamos dotenv si estamos en desarrollo local
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Detectar entorno testnet/mainnet
USE_TESTNET = os.getenv("USE_TESTNET", "false").lower() == "true"
BINANCE_TESTNET_SPOT_BASE_URL = "https://testnet.binance.vision/api"

# Seleccionar claves
if USE_TESTNET:
    API_KEY = os.getenv("BINANCE_API_KEY_TESTNET")
    API_SECRET = os.getenv("BINANCE_SECRET_KEY_TESTNET")
else:
    API_KEY = os.getenv("BINANCE_API_KEY_MAINNET")
    API_SECRET = os.getenv("BINANCE_SECRET_KEY_MAINNET")

# Validar claves
if not API_KEY or not API_SECRET:
    raise RuntimeError("❌ Faltan claves de Binance en las variables de entorno")

# Crear cliente
client = Client(api_key=API_KEY, api_secret=API_SECRET, testnet=USE_TESTNET)

# Cambiar URL para Testnet si aplica
if USE_TESTNET:
    client.API_URL = BINANCE_TESTNET_SPOT_BASE_URL

# Función auxiliar
def get_price(symbol: str) -> float:
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])