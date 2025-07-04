# analytics/indicator_engine.py

import pandas as pd
import numpy as np
import ta
import talib

MIN_REQUIRED_BARS = 50

class TechnicalIndicatorEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def compute_indicators(self):
        if len(self.df) < MIN_REQUIRED_BARS:
            return {"summary": "Insuficientes datos", "details": {}, "score": 0}
        df = self.df.copy()
        signals = {}
    

        # RSI
        rsi = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
        df['rsi'] = rsi
        signals['RSI'] = self._interpret_rsi(rsi.iloc[-1])

        # MACD
        macd = ta.trend.MACD(close=df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_hist'] = macd.macd_diff()
        signals['MACD'] = self._interpret_macd(df['macd_hist'].iloc[-1])

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(close=df['close'])
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_lower'] = bb.bollinger_lband()
        signals['Bollinger'] = self._interpret_bollinger(
            df['close'].iloc[-1],
            df['bb_upper'].iloc[-1],
            df['bb_lower'].iloc[-1]
        )

        # ADX
        adx = ta.trend.ADXIndicator(high=df['high'], low=df['low'], close=df['close'])
        df['adx'] = adx.adx()
        signals['ADX'] = f"{df['adx'].iloc[-1]:.2f}"

        # VWAP (manual)
        try:
            df['vwap'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
            signals['VWAP'] = "Above Price" if df['close'].iloc[-1] > df['vwap'].iloc[-1] else "Below Price"
        except:
            df['vwap'] = None
            signals['VWAP'] = "N/A"

        self.df = df  # Guardamos el DataFrame enriquecido
        return signals

    # Alias retrocompatible
    def calculate_indicators(self):
        return self.compute_indicators()

    def _interpret_rsi(self, value):
        if value > 70:
            return f"Overbought ({value:.2f})"
        elif value < 30:
            return f"Oversold ({value:.2f})"
        else:
            return f"Neutral ({value:.2f})"

    def _interpret_macd(self, value):
        if value > 0:
            return f"Bullish ({value:.2f})"
        elif value < 0:
            return f"Bearish ({value:.2f})"
        else:
            return "Neutral (0)"

    def _interpret_bollinger(self, close, upper, lower):
        if close > upper:
            return "Breakout Up"
        elif close < lower:
            return "Breakdown Down"
        else:
            return "Inside Bands"


# Alias para mantener compatibilidad con módulos antiguos
IndicatorEngine = TechnicalIndicatorEngine