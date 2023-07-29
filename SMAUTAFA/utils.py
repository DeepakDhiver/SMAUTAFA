import yfinance as yf
import ta
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os



def calculate_indicators(ticker, interval):
    def get_signal(interpretation):
        if "Overbought" in interpretation or "Bearish" in interpretation:
            return "Sell"
        elif "Oversold" in interpretation or "Bullish" in interpretation:
            return "Buy"
        elif "Price Above SMA" in interpretation or "Positive OBV" in interpretation or "Volatility: High" in interpretation:
            return "Buy"
        elif "Price Below SMA" in interpretation or "Price Below EMA" in interpretation or "Non-Trending" in interpretation:
            return "Sell"
        else:
            return "Hold"

    def get_rsi(data):
        # Calculate the RSI
        rsi = ta.momentum.RSIIndicator(data['Close'], window=14).rsi().iloc[-1]

        # Interpretation of RSI
        if rsi > 70:
            interpretation = "Overbought (Strong)"
        elif rsi > 60:
            interpretation = "Overbought (Mild)"
        elif rsi > 40:
            interpretation = "Neutral"
        elif rsi > 30:
            interpretation = "Oversold (Mild)"
        else:
            interpretation = "Oversold (Strong)"

        return rsi, interpretation

    def get_macd(data):
        # Calculate the MACD
        macd = ta.trend.MACD(data['Close']).macd().iloc[-1]

        # Interpretation of MACD
        if macd > 0:
            interpretation = "Bullish"
        else:
            interpretation = "Bearish"

        return macd, interpretation

    def calculate_atr(data):
        # Calculate the ATR
        atr = ta.volatility.AverageTrueRange(data['High'], data['Low'], data['Close'], window=14).average_true_range().iloc[-1]

        # Interpretation of ATR
        interpretation = "Volatility: Low" if atr < 0.5 else "Volatility: High"

        return atr, interpretation

    def get_stoch(data):
        # Calculate the Stochastic Oscillator
        stoch = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close']).stoch().iloc[-1]

        # Interpretation of Stochastic Oscillator
        if stoch > 80:
            interpretation = "Overbought"
        elif stoch < 20:
            interpretation = "Oversold"
        else:
            interpretation = "Neutral"

        return stoch, interpretation

    def get_mfi(data):
        # Calculate the Money Flow Index (MFI)
        mfi = ta.volume.MFIIndicator(data['High'], data['Low'], data['Close'], data['Volume'], window=14).money_flow_index().iloc[-1]

        # Interpretation of MFI
        if mfi > 70:
            interpretation = "Overbought"
        elif mfi < 30:
            interpretation = "Oversold"
        else:
            interpretation = "Neutral"

        return mfi, interpretation

    def get_cci(data):
        # Calculate the Commodity Channel Index (CCI)
        cci = ta.trend.CCIIndicator(data['High'], data['Low'], data['Close'], window=20).cci().iloc[-1]

        # Interpretation of CCI
        if cci > 100:
            interpretation = "Overbought"
        elif cci < -100:
            interpretation = "Oversold"
        else:
            interpretation = "Neutral"

        return cci, interpretation

    def get_sma(data, window):
        # Calculate the Simple Moving Average (SMA)
        sma = ta.trend.SMAIndicator(data['Close'], window=window).sma_indicator().iloc[-1]

        # Interpretation of SMA
        if data['Close'].iloc[-1] > sma:
            interpretation = "Price Above SMA"
        else:
            interpretation = "Price Below SMA"

        return sma, interpretation

    def get_ema(data, window):
        # Calculate the Exponential Moving Average (EMA)
        ema = ta.trend.EMAIndicator(data['Close'], window=window).ema_indicator().iloc[-1]

        # Interpretation of EMA
        if data['Close'].iloc[-1] > ema:
            interpretation = "Price Above EMA"
        else:
            interpretation = "Price Below EMA"

        return ema, interpretation

    def get_adx(data):
        # Calculate Average Directional Index (ADX)
        adx = ta.trend.ADXIndicator(data['High'], data['Low'], data['Close'], window=14).adx().iloc[-1]

        # Interpretation of ADX
        if adx > 25:
            interpretation = "Trending"
        else:
            interpretation = "Non-Trending"

        return adx, interpretation

    def get_obv(data):
        # Calculate On-Balance Volume (OBV)
        obv = ta.volume.OnBalanceVolumeIndicator(data['Close'], data['Volume']).on_balance_volume().iloc[-1]

        # Interpretation of OBV
        if obv > 0:
            interpretation = "Positive OBV (Buyers Dominant)"
        else:
            interpretation = "Negative OBV (Sellers Dominant)"

        return obv, interpretation

    # Calculate the start and end dates
    end_date = datetime.now()
    if interval == "1d":
        start_date = end_date - timedelta(days=90)
    else:
        start_date = end_date - timedelta(days=30)

    # Get the data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

    # Calculate the indicators
    rsi, rsi_interpretation = get_rsi(data)
    macd, macd_interpretation = get_macd(data)
    atr, atr_interpretation = calculate_atr(data)
    stoch, stoch_interpretation = get_stoch(data)
    mfi, mfi_interpretation = get_mfi(data)
    cci, cci_interpretation = get_cci(data)
    sma_50, sma_50_interpretation = get_sma(data, window=50)
    sma_200, sma_200_interpretation = get_sma(data, window=200)
    ema_20, ema_20_interpretation = get_ema(data, window=20)
    ema_50, ema_50_interpretation = get_ema(data, window=50)
    adx, adx_interpretation = get_adx(data)
    obv, obv_interpretation = get_obv(data)

    # Prepare the indicator data with buy, sell, or hold signals
    indicators = [
        {"name": "RSI", "value": rsi, "interpretation": rsi_interpretation, "signal": get_signal(rsi_interpretation)},
        {"name": "MACD", "value": macd, "interpretation": macd_interpretation, "signal": get_signal(macd_interpretation)},
        {"name": "ATR", "value": atr, "interpretation": atr_interpretation, "signal": get_signal(atr_interpretation)},
        {"name": "Stochastic Oscillator", "value": stoch, "interpretation": stoch_interpretation, "signal": get_signal(stoch_interpretation)},
        {"name": "Money Flow Index (MFI)", "value": mfi, "interpretation": mfi_interpretation, "signal": get_signal(mfi_interpretation)},
        {"name": "Commodity Channel Index (CCI)", "value": cci, "interpretation": cci_interpretation, "signal": get_signal(cci_interpretation)},
        {"name": "50-day SMA", "value": sma_50, "interpretation": sma_50_interpretation, "signal": get_signal(sma_50_interpretation)},
        {"name": "200-day SMA", "value": sma_200, "interpretation": sma_200_interpretation, "signal": get_signal(sma_200_interpretation)},
        {"name": "20-day EMA", "value": ema_20, "interpretation": ema_20_interpretation, "signal": get_signal(ema_20_interpretation)},
        {"name": "50-day EMA", "value": ema_50, "interpretation": ema_50_interpretation, "signal": get_signal(ema_50_interpretation)},
        {"name": "ADX", "value": adx, "interpretation": adx_interpretation, "signal": get_signal(adx_interpretation)},
        {"name": "On-Balance Volume (OBV)", "value": obv, "interpretation": obv_interpretation, "signal": get_signal(obv_interpretation)},
        # Add more indicators as needed...
    ]

    return indicators


def calculate_pivot_points(ticker):
    # Calculate the start and end dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    tickerData = yf.download(ticker, start=start_date, end=end_date, interval='1m')
    tickerDf = tickerData.reset_index()

    if tickerDf.empty:
        return []

    # Calculate pivot points
    high = tickerDf['High'].max()
    low = tickerDf['Low'].min()
    close = tickerDf['Close'].iloc[-1]

    pivot = (high + low + close) / 3
    s1 = (2 * pivot) - high
    r1 = (2 * pivot) - low
    s2 = pivot - (high - low)
    r2 = pivot + (high - low)
    s3 = low - 2 * (high - pivot)
    r3 = high + 2 * (pivot - low)

    # Create a list to store the pivot point values
    pivot_values = [
        r3,
        r2,
        r1,
        pivot,
        s1,
        s2,
        s3
    ]

    return pivot_values

def calculate_correlation(indices):
    # Calculate start and end dates
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=2 * 20)).strftime("%Y-%m-%d")

    # Fetch historical data for the given indices using yfinance
    data = yf.download(indices, start=start_date, end=end_date, interval="1d")["Close"]

    # Update index names for better readability
    index_names = {
        "^NSEI": "Nifty India",
        "^IXIC": "NASDAQ USA",
        "^FTSE": "FTSE UK",
        "^FCHI": "CAC 40 France",
        "^STI": "STI Singapore",
        "^HSI": "Hang Seng Hong Kong"
    }
    data.rename(columns=index_names, inplace=True)

    # Calculate correlation matrix
    correlation_matrix = data.corr()

    return correlation_matrix