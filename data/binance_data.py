# data/binance_data.py

import os
import pandas as pd
from binance.client import Client
from dotenv import load_dotenv

# Cargar claves desde .env
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)

def get_ohlcv_data(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_15MINUTE, limit=100):
    """
    Descarga velas OHLCV desde Binance.
    """
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # Convertir a float
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df[["open", "high", "low", "close", "volume"]]