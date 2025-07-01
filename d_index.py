import json
import time
import datetime
import argparse
import requests
from symbols import symbols
import schedule
import threading
import holidays


def save_daily_price(symbol, data):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    path = f"data/{symbol}"
    os.makedirs(path, exist_ok=True)
    file_path = f"{path}/{today}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[SAVED] {symbol} -> {file_path}")

def fetch_all_symbols():
    print("\nFetching daily prices from Finnhub...\n")
    for sector, symbol_list in symbols.items():
        for sym in symbol_list:
            try:
                data = fetch_daily_price(sym)
                save_daily_price(sym, data)
                time.sleep(RATE_LIMIT_SLEEP)
            except Exception as e:
                print(f"[ERROR] {sym}: {e}")

def load_price_history(symbol, min_days=200):
    hist_path = f"data/{symbol}/history.json"
    if os.path.exists(hist_path):
        with open(hist_path) as f:
            records = json.load(f)
    else:
        records = []

    if len(records) < min_days:
        records = fetch_historical_prices(symbol, days=min_days)

        records.sort(key=lambda x: x[0]) #
        return records

def moving_average(data, window):
    if len(data) < window:
        return None
    return round(sum(data[-window:]) / window, 2)

def ytd_change(data):
    if not data:
        return None

    year = datetime.date.today().year
    jan_price = next(
        (p for d, p in data if datetime.datetime.strptime(d, "%Y-%m-%d").year == year),
        None
    )
    if jan_price is None:
        return None
    latest_price = data[-1][1]
    return round(((latest_price - jan_price) / jan_price) * 100, 2)

def get_metrics(symbol):
    try:
        price_series = load_price_history(symbol.upper())
        closes = [p for _, p in price_series]
        return {
            "YTD %": ytd_change(price_series), 
            "12-day MA": moving_average(closes, 12),
            "21-day MA": moving_average(closes, 21),
            "50-day MA": moving_average(closes, 50),
            "200-day MA": moving_average(closes, 200),
            }
    
    except Exception as e:
        return {"error": str(e)}

def display_metrics(symbol):
    print(f"\nMetrics for {symbol.upper()}:\n")
    data = get_metrics(symbol.upper())
    for k, v in data.items():
        print(f"{k}: {v}")
    print()

# === Scheduler for Daily Fetch ===

def is_market_day():
    today = datetime.date.today()
    return today.weekday() < 5 and today not in holidays.US()

def scheduled_fetch():
    if is_market_day():
        print("\n[Scheduler] Running daily fetch...")
        fetch_all_symbols()
    else:
        print("\n[Scheduler] Market is closed today. No fetch.")

def run_scheduler():
    schedule.every().day.at("16:30").do(scheduled_fetch)
    print("\n[Scheduler] Auto-fetch scheduled for 4:30 PM each market day.")
    
    def loop():
        while True:
            schedule.run_pending()
            time.sleep(30)
    
    thread = threading.Thread(target=loop)
    thread.daemon = True
    thread.start()

# === Symbol Management ===

def save_symbols():
    with open("symbols_saved.json", "w") as f:
        json.dump(symbols, f, indent=4)
    print("Symbols saved to symbols_saved.json.")

def get_input(prompt, valid_responses):
    while True:
        response = input(prompt).strip().lower()
        if response in valid_responses:
            return response
        else:
            print(f"Please enter one of {valid_responses}.")

def get_sector():
    print("Select the sector for the symbol:")
    sectors = list(symbols.keys())
    for i, sector in enumerate(sectors, 1):
        print(f"{i}. {sector}")
    while True:
        try:
            choice = int(input("Enter number: "))
            if 1 <= choice <= len(sectors):
                return sectors[choice - 1]
            print("Invalid number.")
        except ValueError:
            print("Please enter a valid number.")

def modify_symbols(symbol, action):
    if action == 'add':
        if any(symbol in lst for lst in symbols.values()):
            print(f"{symbol} already exists.")
        else:
            sector = get_sector()
            symbols[sector].append(symbol)
            print(f"Added {symbol} to {sector}.")
    elif action == 'rm':
        found = False
        for sector, lst in symbols.items():
            if symbol in lst:
                lst.remove(symbol)
                found = True
                print(f"Removed {symbol} from {sector}.")
                break
        if not found:
            print(f"{symbol} not found.")
    save_symbols()

def list_symbols():
    print("\nTracked Symbols:\n")
    for sector, symbol_list in symbols.items():
        print(f"{sector}: {', '.join(symbol_list)}")
    print()

# === Main CLI ===

def main():
    parser = argparse.ArgumentParser(description="Stock tracker using Finnhub + local cache.")
    parser.add_argument('--add', help='Add a stock symbol')
    parser.add_argument('--rm', help='Remove a stock symbol')
    parser.add_argument('--list', action='store_true', help='List tracked symbols')
    parser.add_argument('--fetch', action='store_true', help='Fetch daily prices from Finnhub')
    parser.add_argument('--auto', action='store_true', help='Run scheduler to auto-fetch at 4:30 PM daily')
    parser.add_argument('--metrics', help='Display local metrics for symbol')

    args = parser.parse_args()

    if args.add:
        modify_symbols(args.add.upper(), 'add')
    elif args.rm:
        modify_symbols(args.rm.upper(), 'rm')
    elif args.list:
        list_symbols()
    elif args.fetch:
        fetch_all_symbols()
    elif args.metrics:
        display_metrics(args.metrics)
    elif args.auto:
        run_scheduler()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Scheduler] Stopped.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
