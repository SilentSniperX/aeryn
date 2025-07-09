import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# === STRATEGY PARAMETERS ===
RSI_PERIOD = 14
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 25
SMA_PERIOD = 50
SYMBOL = "ES=F"  # E-mini S&P 500 Futures
INTERVAL = "1m"  # 1-minute data
CHECK_INTERVAL = 60  # seconds between checks

def fetch_data(symbol, interval="1m", period="1d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def calculate_indicators(df):
    df["RSI"] = compute_rsi(df["Close"], RSI_PERIOD)
    df["SMA"] = df["Close"].rolling(window=SMA_PERIOD).mean()
    return df

def compute_rsi(series, period):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def check_for_trade(df):
    latest = df.iloc[-1]
    previous = df.iloc[-2]

    signal = None
    confidence = 0

    if latest["RSI"] < RSI_OVERSOLD and latest["Close"] > latest["SMA"]:
        signal = "BUY"
        confidence = 80  # rough estimate

    elif latest["RSI"] > RSI_OVERBOUGHT and latest["Close"] < latest["SMA"]:
        signal = "SELL"
        confidence = 80

    return signal, confidence

def main_loop():
    while True:
        print(f"[{datetime.now()}] Checking for trade setup...")
        df = fetch_data(SYMBOL, INTERVAL)
        df = calculate_indicators(df)

        signal, confidence = check_for_trade(df)

        if signal:
            print(f">>> SIGNAL: {signal} ({confidence}% confidence)")
        else:
            print("No setup found.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop()
