import pandas as pd
from symbols import symbols
from data import fetch_data
from compare_data import compare_data
import time

def get_input(prompt, valid_responses):
    while True:
        response = input(prompt).strip().lower()
        if response in valid_responses:
            return response
        else:
            print(f"Please enter one of {valid_responses}.")

start_response = get_input("Are you ready??): ", ["y", "n"])

if start_response == "y":
    action = get_input("Choose an action: 1 for Closing data, 2 for Compare closing data (1/2): ", ["1", "2"])

    if action == "1":
        end_date = input("Enter the closing date yyyy-mm-dd: ")

        stock_data = fetch_data(symbols, end_date)

        with open("stock_data.txt", "w") as file:
            for data in stock_data:
                file.write(f"Ticker: {data['Ticker']}\n")
                file.write(f"Closing Price: {data['Closing Price']}\n")
                file.write(f"Current Price: {data['Current Price']}\n")
                file.write(f"Market Cap: {data['Market Cap']}\n")
                file.write(f"PE Ratio: {data['PE Ratio']}\n")
                file.write(f"EPS: {data['EPS']}\n")
                file.write(f"Dividend Yield: {data['Dividend Yield']}\n")
                file.write(f"Beta: {data['Beta']}\n")
                file.write(f"52 Week High: {data['52 Week High']}\n")
                file.write(f"52 Week Low: {data['52 Week Low']}\n")
                file.write(f"Volume: {data['Volume']}\n")
                file.write(f"Average Volume: {data['Average Volume']}\n")
                file.write(f"Sector: {data['Sector']}\n")
                file.write(f"Industry: {data['Industry']}\n")
                file.write(f"Website: {data['Website']}\n")
                file.write("\n")

        print("Stock data saved to stock_data.txt")

        stock_data_df = pd.DataFrame(stock_data)

        excel_filename = "Stock_it.xlsx"

        with pd.ExcelWriter(excel_filename) as writer:
            stock_data_df.to_excel(writer, sheet_name="Stock Data", index=False)

        print("We got two words for ya...")
        time.sleep(3)
        print("Stock it!")

    elif action == "2":
        date1 = input("Enter the first date yyyy-mm-dd: ")
        date2 = input("Enter the second date yyyy-mm-dd: ")

        comparison_data = compare_data(symbols, date1, date2)

        comparison_data_df = pd.DataFrame(comparison_data)

        excel_filename = "Stock_Comparison.xlsx"

        with pd.ExcelWriter(excel_filename) as writer:
            comparison_data_df.to_excel(writer, sheet_name="Comparison Data", index=False)

        print("Comparison data saved to Stock_Comparison.xlsx")

        print("We got two words for ya...")
        time.sleep(3)
        print("Stock it!")

else:
    print("Operation canceled.")
