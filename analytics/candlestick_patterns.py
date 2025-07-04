# analytics/candlestick_patterns.py

import pandas as pd
import talib
print(talib.get_functions())

class CandlestickPatternDetector:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.pattern_funcs = {
            'CDLDOJI': talib.CDLDOJI,
            'CDLHAMMER': talib.CDLHAMMER,
            'CDLINVERTEDHAMMER': talib.CDLINVERTEDHAMMER,
            'CDLENGULFING': talib.CDLENGULFING,
            'CDLSHOOTINGSTAR': talib.CDLSHOOTINGSTAR,
            'CDLDRAGONFLYDOJI': talib.CDLDRAGONFLYDOJI,
            'CDLMORNINGSTAR': talib.CDLMORNINGSTAR,
            'CDLEVENINGSTAR': talib.CDLEVENINGSTAR,
            'CDLPIERCING': talib.CDLPIERCING,
            'CDLHARAMI': talib.CDLHARAMI
        }

        self.pattern_signals = {
            'CDLHAMMER': 'long',
            'CDLINVERTEDHAMMER': 'long',
            'CDLENGULFING': 'long',
            'CDLDRAGONFLYDOJI': 'long',
            'CDLMORNINGSTAR': 'long',
            'CDLPIERCING': 'long',
            'CDLHARAMI': 'long',
            'CDLSHOOTINGSTAR': 'short',
            'CDLEVENINGSTAR': 'short',
            'CDLDOJI': 'neutral'
        }

    def detect(self) -> pd.DataFrame:
        """
        Aplica los patrones de velas japonesas y retorna el DataFrame con columnas:
        - pattern: nombre del patrón detectado
        - signal: interpretación ('long', 'short', 'neutral')
        """
        df = self.df.copy()
        df['pattern'] = None
        df['signal'] = None

        for name, func in self.pattern_funcs.items():
            result = func(df['open'], df['high'], df['low'], df['close'])
            df.loc[result != 0, 'pattern'] = name
            df.loc[result != 0, 'signal'] = self.pattern_signals.get(name)

        self.df = df
        return df

    def get_latest_pattern(self) -> str:
        """
        Devuelve el último patrón detectado, si existe.
        """
        patterns = self.df['pattern'].dropna()
        return patterns.iloc[-1] if not patterns.empty else None

    def get_latest_signal(self) -> str:
        """
        Devuelve la última señal ('long', 'short', 'neutral') según el patrón más reciente.
        """
        signals = self.df['signal'].dropna()
        return signals.iloc[-1] if not signals.empty else None