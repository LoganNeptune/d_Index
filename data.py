# data.py

import yfinance as yf
from datetime import datetime, timedelta

def fetch_data(symbols, end_date):
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    # Adjust for weekends
    if end_date_dt.weekday() == 0:  # If it's Monday
        start_date_dt = end_date_dt - timedelta(days=3)  # Use Friday as the start date
    elif end_date_dt.weekday() == 6:  # If it's Sunday
        start_date_dt = end_date_dt - timedelta(days=2)  # Use Friday as the start date
    else:  # Other weekdays
        start_date_dt = end_date_dt - timedelta(days=1)  # Use the previous day

    start_date = start_date_dt.strftime("%Y-%m-%d")
    end_date = end_date_dt.strftime("%Y-%m-%d")

    # Data container
    stock_data = []

    # Fetch data for each symbol
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        
        # Historical market data
        hist = stock.history(start=start_date, end=end_date)
        closing_price = hist['Close'].iloc[-1] if not hist.empty else "No price data found"
        
        # Current market data
        current_data = stock.info
        stock_data.append({
            "Ticker": symbol,
            "Closing Price": closing_price,
            "Current Price": current_data.get('currentPrice', "N/A"),
            "Market Cap": current_data.get('marketCap', "N/A"),
            "PE Ratio": current_data.get('trailingPE', "N/A"),
            "EPS": current_data.get('trailingEps', "N/A"),
            "Dividend Yield": current_data.get('dividendYield', "N/A"),
            "Beta": current_data.get('beta', "N/A"),
            "52 Week High": current_data.get('fiftyTwoWeekHigh', "N/A"),
            "52 Week Low": current_data.get('fiftyTwoWeekLow', "N/A"),
            "Volume": current_data.get('volume', "N/A"),
            "Average Volume": current_data.get('averageVolume', "N/A"),
            "Sector": current_data.get('sector', "N/A"),
            "Industry": current_data.get('industry', "N/A"),
            "Website": current_data.get('website', "N/A"),
        })

    return stock_data
