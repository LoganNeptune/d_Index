import yfinance as yf
from datetime import datetime, timedelta

def fetch_data(symbols, end_date):
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    if end_date_dt.weekday() == 0:  # If it's Monday
        start_date_dt = end_date_dt - timedelta(days=3)  # Use Friday as the start date
    elif end_date_dt.weekday() == 6:  # If it's Sunday
        start_date_dt = end_date_dt - timedelta(days=2)  # Use Friday as the start date
    else:  # Other weekdays
        start_date_dt = end_date_dt - timedelta(days=1)  # Use the previous day

    start_date = start_date_dt.strftime("%Y-%m-%d")
    end_date = end_date_dt.strftime("%Y-%m-%d")

    stock_data = []

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        
        hist = stock.history(start=start_date, end=end_date)
        closing_price = hist['Close'].iloc[-1] if not hist.empty else "No price data found"
        
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

def compare_data(symbols, date1, date2):
    data1 = fetch_data(symbols, date1)
    data2 = fetch_data(symbols, date2)

    comparison = []

    for d1, d2 in zip(data1, data2):
        if d1["Ticker"] == d2["Ticker"]:
            comparison.append({
                "Ticker": d1["Ticker"],
                "Closing Price Date1": d1["Closing Price"],
                "Closing Price Date2": d2["Closing Price"],
                "Price Change": d2["Closing Price"] - d1["Closing Price"] if isinstance(d1["Closing Price"], (int, float)) and isinstance(d2["Closing Price"], (int, float)) else "N/A",
                "Current Price Date1": d1["Current Price"],
                "Current Price Date2": d2["Current Price"],
                "Market Cap Date1": d1["Market Cap"],
                "Market Cap Date2": d2["Market Cap"],
                "PE Ratio Date1": d1["PE Ratio"],
                "PE Ratio Date2": d2["PE Ratio"],
                "EPS Date1": d1["EPS"],
                "EPS Date2": d2["EPS"],
                "Dividend Yield Date1": d1["Dividend Yield"],
                "Dividend Yield Date2": d2["Dividend Yield"],
                "Beta Date1": d1["Beta"],
                "Beta Date2": d2["Beta"],
                "52 Week High Date1": d1["52 Week High"],
                "52 Week High Date2": d2["52 Week High"],
                "52 Week Low Date1": d1["52 Week Low"],
                "52 Week Low Date2": d2["52 Week Low"],
                "Volume Date1": d1["Volume"],
                "Volume Date2": d2["Volume"],
                "Average Volume Date1": d1["Average Volume"],
                "Average Volume Date2": d2["Average Volume"],
                "Sector": d1["Sector"],
                "Industry": d1["Industry"],
                "Website": d1["Website"],
            })

    return comparison
