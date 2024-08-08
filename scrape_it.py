import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from symbols import symbols
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

BASE_URL = "https://www.sec.gov/edgar/search/"
LOG_FILE = 'sec_filings_log.txt'

def read_last_update():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as file:
            log_data = file.readlines()
        last_updates = {}
        for line in log_data:
            symbol, last_update = line.strip().split(',')
            last_updates[symbol] = datetime.strptime(last_update, '%Y-%m-%d')
        return last_updates
    else:
        return {symbol: datetime(2024, 7, 1) for symbol in symbols}  # Default baseline date

def write_last_update(last_updates):
    with open(LOG_FILE, 'w') as file:
        for symbol, last_update in last_updates.items():
            file.write(f"{symbol},{last_update.strftime('%Y-%m-%d')}\n")

def fetch_filings(symbol, start_date):
    filings = []
    search_url = f"{BASE_URL}#/dateRange=custom&ciks={symbol}&startdt={start_date.strftime('%Y-%m-%d')}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('tr')
        for result in results:
            filing = {}
            columns = result.find_all('td')
            if len(columns) > 0:
                filing['symbol'] = symbol
                filing['filing_type'] = columns[0].text.strip()
                filing['filing_date'] = columns[3].text.strip()
                filing['filing_link'] = "https://www.sec.gov" + columns[1].find('a')['href']
                filings.append(filing)
    return filings

def summarize_text(text, max_words=100):
    prompt = f"Please summarize the following document in {max_words} words or less:\n\n{text}"
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=max_words*2,  # Approximate words to tokens
        temperature=0.7
    )
    return response.choices[0].text.strip()

def fetch_and_summarize_filings(symbols, start_date):
    filings = []
    for symbol in symbols:
        print(f"Fetching filings for {symbol}...")
        filings.extend(fetch_filings(symbol, start_date))
    return filings

def save_filings(filings):
    with open('sec_filings.txt', 'w') as file:
        for filing in filings:
            file.write(f"{filing['symbol']} - {filing['filing_type']} - {filing['filing_date']}\n")
            file.write(f"Link: {filing['filing_link']}\n")
            file.write("\n")

def save_summaries(filings):
    with open('sec_summaries.txt', 'w') as file:
        for filing in filings:
            # Fetch the full text of the filing document
            response = requests.get(filing['filing_link'])
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                filing_text = soup.get_text()
                summary = summarize_text(filing_text, max_words=100)
                file.write(f"{filing['symbol']} - {filing['filing_type']} - {filing['filing_date']}\n")
                file.write(f"Link: {filing['filing_link']}\n")
                file.write(f"Summary: {summary}\n")
                file.write("\n")

if __name__ == "__main__":
    last_updates = read_last_update()
    all_filings = fetch_and_summarize_filings(symbols, datetime(2024, 7, 1))
    save_filings(all_filings)
    save_summaries(all_filings)
    print("Filings and summaries saved.")
