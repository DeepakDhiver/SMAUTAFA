import yfinance as yf
import ta
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


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

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    # Save the plot as a JPEG in memory
    output_path = r"C:\Users\deepa\OneDrive\Desktop\Final Integration\SMAUTAFA\SMAUTAFA\static\images\correlation_matrix.jpg"
    plt.savefig(output_path, format='jpeg')
    return correlation_matrix


def calculate_indicators(ticker, interval):
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

    # Prepare the indicator data
    indicators = [
        {"name": "RSI", "value": rsi, "interpretation": rsi_interpretation},
        {"name": "MACD", "value": macd, "interpretation": macd_interpretation},
        {"name": "ATR", "value": atr, "interpretation": atr_interpretation},
        {"name": "Stochastic Oscillator", "value": stoch, "interpretation": stoch_interpretation},
        {"name": "Money Flow Index (MFI)", "value": mfi, "interpretation": mfi_interpretation},
        {"name": "Commodity Channel Index (CCI)", "value": cci, "interpretation": cci_interpretation},
    ]

    return indicators


def calculate_pivot_points(ticker):
    # Calculate the start and end dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    tickerData = yf.download(ticker, start=start_date, end=end_date, interval='1m')
    tickerDf = tickerData.reset_index()

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
