import yfinance as yf
import pandas_ta as ta
import warnings
import matplotlib.pyplot as plt
import json
from os import system

def clear():
    system("clear")

def getconfig():
    with open('config.json') as f:
        return(json.load(f))

# Uyarıları görmezden gel
warnings.simplefilter(action='ignore', category=FutureWarning)

def indicator():

    config = getconfig()
    symbol = config["symbol"]
    period = config["period"]
    interval = config["interval"]
    rsi_length = config["rsi_length"]
    rsi_sma_length = config["rsi_sma_length"]
    macd_short = config["macd_short"]
    macd_long = config["macd_long"]
    macd_signal = config["macd_signal"]
    partial_stock = config["partial_stock"]
    plot = config["plot"]
    backtest = config["backtest"]
    capital = config["capital"]
    commission = config["commission"]
    stop_loss = config["stop_loss"]
    take_profit = config["take_profit"]
    data = yf.download(symbol, period=period, interval=interval)

    # RSI ve RSI'nin SMA'sını hesapla
    data["rsi"] = ta.rsi(data["Close"], length=rsi_length)
    data["rsi_sma"] = ta.sma(data["rsi"], length=rsi_sma_length)

    # Hareketli ortalama ve MACD hesapla
    data['12_MA'] = data["Close"].ewm(span=macd_short).mean()
    data['26_MA'] = data["Close"].ewm(span=macd_long).mean()
    data['MACD'] = data['12_MA'] - data['26_MA']
    data['Signal_Line'] = data['MACD'].ewm(span=macd_signal).mean()

    # Sinyalleri depolamak için boş listeler oluştur
    rsi_signals = []
    macd_signals = []

    # Sinyalleri oluştur
    for i in range(len(data)):
        # RSI sinyali
        if data["rsi_sma"].iloc[i] > 50:
            rsi_signals.append("Buy")
        else:
            rsi_signals.append("Sell")

        # MACD sinyali
        if i >= 1:
            if data['MACD'].iloc[i] > data['Signal_Line'].iloc[i]:
                macd_signals.append("Buy")
            else:
                macd_signals.append("Sell")
        else:
            macd_signals.append("Sell")

    # DataFrame'e sinyalleri ekle
    data["RSI_Signal"] = rsi_signals
    data["MACD_Signal"] = macd_signals

    # Satın alma durumunu takip etmek için bayrak tanımla
    buy = False

    # Sinyal listesi oluştur
    signal = []


    for i in range(len(data)):
        if data["MACD_Signal"][i] == "Buy" and data["RSI_Signal"][i] == "Buy" and not buy:
            buy = True
            buy_price = data["Close"][i]
            if stop_loss!= 0:stop_loss_price = buy_price * (1 - stop_loss)
            if take_profit !=0:take_profit_price = buy_price * (1 + take_profit)
            signal.append("Buy")
        elif buy:
            if (data["MACD_Signal"][i] == "Sell" and data["RSI_Signal"][i] == "Sell"):
                buy = False
                signal.append("Sell")
            elif stop_loss!= 0:
                if data["Close"][i] <= stop_loss_price:
                    buy = False
                    signal.append("Sell")
                else:
                    signal.append("Hold")
            elif take_profit !=0:
                if data["Close"][i] >= take_profit_price:
                    buy = False
                    signal.append("Sell")
                else:
                    signal.append("Hold")
            else:
                signal.append("Hold")
        else:
            signal.append("Hold")

    # Sinyal sütunu ekleyin
    data["Signal"] = signal

    # Veriyi CSV olarak kaydet
    data.to_csv(f'{symbol}.csv', index=False)

    if plot:
        plt.figure(figsize=(14,7))
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        plt.plot(data[data['Signal'] == 'Buy'].index, data['Close'][data['Signal'] == 'Buy'], '^', markersize=10, color='green', lw=0, label='Buy Signal')
        plt.plot(data[data['Signal'] == 'Sell'].index, data['Close'][data['Signal'] == 'Sell'], 'v', markersize=10, color='red', lw=0, label='Sell Signal')
        plt.title('Close Price and Buy/Sell Signals')
        plt.legend()
        plt.savefig(f"{symbol}.png")

    # Geri test fonksiyonu
    if backtest:
        shares = 0
        position = None
        buy_price = 0
        sell_price = 0
        pnl = 0
        for i in range(len(data)):
            if data["Signal"][i] == "Buy" and position != "Buy":
                num_shares = int(capital / (data["Close"][i] * (1 + commission)))
                shares += num_shares
                buy_price = data["Close"][i]
                capital -= num_shares * buy_price * (1 + commission)
                position = "Buy"
                print(data.index[i], "Buy at:", buy_price, "Shares:", num_shares)
            elif data["Signal"][i] == "Sell" and position != "Sell":
                sell_price = data["Close"][i]
                pnl += (sell_price - buy_price) * shares
                capital += sell_price * shares * (1 - commission)
                shares = 0
                position = "Sell"
                print(data.index[i], "Sell at:", sell_price, "Profit/Loss:", pnl)
        print(pnl)

def edit_config(config_data):
    print("Config Editor")
    print("-------------")

    while True:
        print("\nCurrent Configuration:")
        for key, value in config_data.items():
            print(f"{key}: {value}")

        print("\nOptions:")
        print("1. Edit a parameter")
        print("2. Save and exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            parameter = input("Enter the parameter you want to edit: ")
            if parameter in config_data:
                new_value = input(f"Enter the new value for {parameter}: ")
                if parameter == "partial_stock" or parameter == "plot" or parameter == "backtest":
                    config_data[parameter] = new_value.lower() == "true"
                elif parameter == "capital":
                    if float(new_value) > 0:
                        config_data[parameter] = float(new_value)
                    else:
                        clear()
                        print("Capital must be a positive number.")
                elif parameter == "period":
                    if new_value in ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]:
                        config_data[parameter] = new_value
                    else:
                        clear()
                        print("Invalid period. Choose from: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.")
                elif parameter == "interval":
                    if new_value in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]:
                        if new_value == "1m":
                            clear()
                            print("Warning: With interval 1m, maximum data length is 7 days.")
                            if config_data["period"] not in ["1d", "5d", "max"]:
                                config_data["period"] = "max"
                                clear()
                                print("Period changed to 7 days.")
                        elif new_value in ["2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d"]:
                            clear()
                            print("Warning: With interval from 2m to 1d, maximum data length is 60 days.")
                            if config_data["period"] in ["3mo", "6mo", "1y", "2y", "5y", "10y", "ytd"]:
                                config_data["period"] = "max"
                                clear()
                                print("Period changed to 2mo.")
                        config_data[parameter] = new_value
                    else:
                        clear()
                        print("Invalid interval. Choose from: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo.")
                else:
                    try:
                        config_data[parameter] = type(config_data[parameter])(new_value)
                    except ValueError:
                        clear()
                        print(f"Invalid value for {parameter}.")
            else:
                clear()
                print("Invalid parameter name.")
        elif choice == "2":
            with open('config.json', 'w') as f:
                json.dump(config_data, f, indent=4)
            clear()
            print("Configuration saved successfully.")
            break
        else:
            clear()
            print("Invalid choice.")

def main():
    config = getconfig()
    while True:
        print("1-run test\n2-edit config")
        choice = input("Enter your choice: ")
        if choice == "1":
            indicator()
        elif choice == "2":
            edit_config(config)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()



