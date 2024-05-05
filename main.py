import yfinance as yf
import pandas_ta as ta
import warnings
import matplotlib.pyplot as plt

# Suppress future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define the stock symbol and time period
symbol = "stock_name"  # Replace with your desired stock symbol

# Fetch the stock data
data = yf.download(symbol, period="1y")

# Calculate the 14-day RSI using pandas_ta
data["rsi"] = ta.rsi(data["Close"], length=14)

# Calculate the 5-day SMA of RSI
data["rsi_sma"] = ta.sma(data["rsi"], length=5)

# Hareketli 12 ve 26 günlük ortalamaları hesaplama
data['12_MA'] = data["Close"].ewm(span=12).mean()
data['26_MA'] = data["Close"].ewm(span=26).mean()

# MACD hesaplama
data['MACD'] = data['12_MA'] - data['26_MA']

# MACD sinyal hattı (9 günlük SMA)
data['Signal_Line'] = data['MACD'].ewm(span=9).mean()

# Create empty lists to store signals
rsi_signals = []
macd_signals = []
signal = []

# Loop through each row in the data
for i in range(len(data)):
    # RSI Signal
    if data["rsi_sma"].iloc[i] > 50:
        rsi_signals.append("Buy")
    else:
        rsi_signals.append("Sell")

    # MACD Signal
    if i >= 1:
        if data['MACD'].iloc[i] > data['Signal_Line'].iloc[i]:
            macd_signals.append("Buy")
        else:
            macd_signals.append("Sell")
    else:
        macd_signals.append("Sell")

# Add signals to DataFrame
data["RSI_Signal"] = rsi_signals
data["MACD_Signal"] = macd_signals

buy = False

for i in range(len(data)):
    if data["MACD_Signal"][i] == "Buy" and data["RSI_Signal"][i] == "Buy" and buy == False:
        buy = True
        signal.append("Buy")
    elif data["MACD_Signal"][i] == "Sell" and data["RSI_Signal"][i] == "Sell" and buy == True:
        buy = False
        signal.append("Sell")
    else:
        signal.append("Hold")


data["Signal"] = signal

# Save data to CSV
data.to_csv('test.csv', index=False)

# Plot close price
plt.figure(figsize=(14,7))
plt.plot(data.index, data['Close'], label='Close Price', color='blue')

# Plot buy signals
plt.plot(data[data['Signal'] == 'Buy'].index,
         data['Close'][data['Signal'] == 'Buy'],
         '^', markersize=10, color='green', lw=0, label='Buy Signal')

# Plot sell signals
plt.plot(data[data['Signal'] == 'Sell'].index,
         data['Close'][data['Signal'] == 'Sell'],
         'v', markersize=10, color='red', lw=0, label='Sell Signal')

plt.title('Close Price and Buy/Sell Signals')
plt.legend()
plt.savefig("test.png")

def backtest(data, initial_capital=10000, commission=0.005):
    capital = initial_capital  # Initial capital
    shares = 0  # Number of shares held
    position = None  # Current position (None, "Buy", or "Sell")
    buy_price = 0  # Price at which shares were bought
    sell_price = 0  # Price at which shares were sold
    pnl = 0  # Profit and Loss
    for i in range(len(data)):
        # Buy signal
        if data["Signal"][i] == "Buy" and position != "Buy":
            num_shares = int(capital / (data["Close"][i] * (1 + commission)))
            shares += num_shares
            buy_price = data["Close"][i]
            capital -= num_shares * buy_price * (1 + commission)
            position = "Buy"
            print(data.index[i], "Buy at:", buy_price, "Shares:", num_shares)
        # Sell signal
        elif data["Signal"][i] == "Sell" and position != "Sell":
            sell_price = data["Close"][i]
            pnl += (sell_price - buy_price) * shares
            capital += sell_price * shares * (1 - commission)
            shares = 0
            position = "Sell"
            print(data.index[i], "Sell at:", sell_price, "Profit/Loss:", pnl)
    return pnl

# Perform backtesting
profit_loss = backtest(data)
print("General Profit/Loss:", profit_loss)



