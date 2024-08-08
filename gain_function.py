def calculate_percentage_gain_per_cent(gain_in_cents, percentage_gain):
    """
    Calculate the rate of conversion per cent.
    
    :param gain_in_cents: The gain in cents
    :param percentage_gain: The percentage gain
    :return: The percentage gain per cent
    """
    percentage_gain_per_cent = percentage_gain / gain_in_cents
    return percentage_gain_per_cent

def calculate_rate_per_percent(total_gain, percentage_gain):
    """
    Calculate the rate of conversion per percent.
    
    :param total_gain: The total gain in dollars
    :param percentage_gain: The percentage gain
    :return: The rate of conversion per percent
    """
    rate_per_percent = total_gain / percentage_gain
    return rate_per_percent

def calculate_money_gained_per_penny(money_per_percentage, percentage_gain_per_penny):
    """
    Calculate the money gained for a 1 penny increase in stock.
    
    :param money_per_percentage: The amount of money gained per percentage
    :param percentage_gain_per_penny: The percentage gain per penny
    :return: The money gained per penny
    """
    money_gained_per_penny = money_per_percentage * percentage_gain_per_penny
    return money_gained_per_penny

# Get user inputs
gain_in_cents = float(input("Enter the gain in cents: "))
percentage_gain = float(input("Enter the percentage gain: "))
total_gain = float(input("Enter the total gain in dollars: "))
money_per_percentage = float(input("Enter the money gained per percentage: "))

# Calculate percentage gain per cent
percentage_gain_per_cent = calculate_percentage_gain_per_cent(gain_in_cents, percentage_gain)
print(f"The rate of conversion per cent is approximately {percentage_gain_per_cent:.4f}% gain per cent.")

# Calculate rate per percent
rate_per_percent = calculate_rate_per_percent(total_gain, percentage_gain)
print(f"The rate of conversion per percent is approximately ${rate_per_percent:.3f} per percent.")

# Calculate money gained per penny
money_gained_per_penny = calculate_money_gained_per_penny(money_per_percentage, percentage_gain_per_cent)
print(f"You gain approximately ${money_gained_per_penny:.2f} when the stock goes up one penny.")
