from pathlib import Path
from __future__ import annotations
import os, json, time, datetime, requests
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY: str | None os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1/quote"
CANDLE_URL = "https://finnhub.io/api/v1/stock/candle"
RATE_LIMIT_SLEEP = 0.05

def api_get(url: str, params: dict) -> dict: 
    res = requests.get(url, params=params)
    time.sleep(RATE_LIMIT_SLEEP) 
    res.raise_for_status()
    return res.json()

def fetch_daily_price(symbol: str) -> dict:
    if not FINNHUB_API_KEY:
        raise ValueError("Set your Finnhub API key as FINNHUB_API_KEY environment variable.")

    params = {"symbol": symbol, "token": FINNHUB_API_KEY}
    data = api_get(BASE_URL, params)

    if "c" not in data:
        raise ValueError(f"Invalid response for {symbol}: {data}")

    return {
        "timestamp": int(time.time()),
        "symbol": symbol,
        "current": data["c"],
        "high": data["h"],
        "low": data["l"],
        "open": data["o"],
        "previousClose": data["pc"]
    }

def fetch_historical_prices(symbol: str, days=200):
    if not FINNHUB_API_KEY:
        raise ValueError("Set your API key as FINNHUB_API_KEY")
    
    end_ts = int(time.time())
    start_ts = end_ts - int (days * 1.6 * 86400) 

    params = {
        "symbol": symbol,
        "resolution": "D",
        "from": start_ts,
        "to": end_ts,
        "token": FINNHUB_API_KEY,
    }
    raw = api_get(CANDLE_URL, params)

    if raw.get("s") != "ok":
        raise ValueError(f"Historical fetch failed for {symbol}: {raw}")
 
    dates = [datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")
    for t in raw["t"]
    ]
    closes = raw["c"]
    records = list(zip(dates, closes))[-days:]

    cache_dir = Path(f"data/{symbol}")
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / "history.json").write_text(json.dumps(records, indent=2))

    return records