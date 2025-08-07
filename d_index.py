d_index
#!pip install hmmlearn
#!pip install matplotlib
#!pip install yfinance
import yfinance as yf
import pandas as pd
import numpy as np
empty_series = pd.Series(dtype='float64')
pd.Series(dtype='float64')
#from pyhhmm.gaussian import GaussianHMM
from hmmlearn.hmm import GaussianHMM
from pandas_datareader.data import DataReader
import matplotlib.pyplot as plt

#Data Extraction
start_date = '2017-01-01'
end_date = '2022-06-01'
symbol = 'SPY'
data = yf.download(symbol, auto_adjust=False, start=start_date, end=end_date)
data = data[["Open", "High", "Low", "Adj Close"]]


# Add Moving Average
df["MA_12"] = df["Adj Close"].rolling(window=12).mean()
df["MA_21"] = df["Adj Close"].rolling(window=21).mean()
#df.head(2)

# Structure Data
X_train = df[["Returns", "Range"]].iloc[:500] # First 500
X_test = df[["Returns", "Range"]].iloc[500:] #tested against everything after first 500
save_df = df.iloc[500:]

print("Train Length: ", len(X_train))
print("Test Length: ", len(X_test))
print("X_train From: ", X_train.head(1).index.item())
print("X_train To: ", X_train.tail(1).index.item())
print("X_test From: ", X_test.head(1).index.item())
print("X_test To: ", X_test.tail(1).index.item())

# Train HMM
model = GaussianHMM(n_components=4, covariance_type='full', n_iter=2)
model.fit(np.array(X_train.values))
model.predict(X_train.values)[:10]

# Make Prediction on Test Data
df_main = save_df.copy()
df_main.drop(columns=["High", "Low"], inplace=True)

if isinstance(df_main.columns,
pd.MultiIndex):
    df_main.columns = df_main.columns.map(lambda x: x if isinstance(x,str) else x[0])

hmm_results = model.predict(X_test.values)
df_main["HMM"] = hmm_results
#df_main.tail()

# Add MA Signals: 0=nothing, 1=long, -1=short
df_main.loc[df_main["MA_12"] > df_main["MA_21"], "MA_Signal"] = 1 #If 12 day moving average is above 21 MA
df_main.loc[df_main["MA_12"] <= df_main["MA_21"], "MA_Signal"] = 0
#df_main[:30]

# Add HMM Signals
favourable_states = [1,3]
hmm_values = df_main["HMM"].values
hmm_values = [1 if x in favourable_states else 0 for x in hmm_values]
df_main["HMM_Signal"] = hmm_values
#df_main.iloc[50:]

# Add Combined Signal
df_main["Main_Signal"] = 0
df_main.loc[(df_main["MA_Signal"] == 1) & (df_main["HMM_Signal"] == 1), "Main_Signal"] = 1
df_main["Main_Signal"] = df_main["Main_Signal"].shift(1) #Prevent look-ahead bias

# Benchmark Returns
df_main["lrets_bench"] = np.log(df_main["Adj Close"] / df_main["Adj Close"].shift(1))
df_main["bench_prod"] = df_main["lrets_bench"].cumsum()
df_main["bench_prod_exp"] = np.exp(df_main["bench_prod"]) - 1

# Strategy Returns

df_main["lrets_strat"] = (np.log(df_main["Open"].shift(-1) / df_main["Open"]).fillna(0)) * df_main["Main_Signal"]
df_main["lrets_prod"] = df_main["lrets_strat"].cumsum()
df_main["strat_prod_exp"] = np.exp(df_main["lrets_prod"]) - 1

# Review Results Table
df_main.dropna(inplace=True)
df_main.tail()

# Sharpe Ratio Function
def sharpe_ratio(returns_series):
    N = 255
    NSQRT = np.sqrt(N)
    rf = 0.01
    mean = returns_series.mean() * N
    sigma = returns_series.std() * NSQRT
    sharpe_ratio = round((mean - rf) / sigma, 2)
    return sharpe_ratio

# Metrics
bench_rets = round(df_main["bench_prod_exp"].values[-1] * 100, 1)
strat_rets = round(df_main["strat_prod_exp"].values[-1] * 100, 1)

bench_sharpe = sharpe_ratio(df_main["lrets_bench"].values)
strat_sharpe = sharpe_ratio(df_main["lrets_strat"].values)

# Print Metrics
print(f"Returns Benchmark: {bench_rets}%")
print(f"Returns Strategy: {strat_rets}%")
print("---- ---- ---- ---- ---- ----")
print(f"Sharpe Benchmark: {bench_sharpe}")
print(f"Sharpe Strategy: {strat_sharpe}")

# Plot Equity Curves
fig = plt.figure(figsize = (18, 10))
plt.plot(df_main["bench_prod_exp"])
plt.plot(df_main["strat_prod_exp"])
plt.show()

# Save Data
#df_main.to_csv("data/HMM-SPY.csv")
