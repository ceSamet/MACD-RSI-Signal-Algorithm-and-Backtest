# Automated Trading Indicator
### Introduction
This Python script is designed to automate trading indicator analysis using historical stock price data. It utilizes the Yahoo Finance API (yfinance) to fetch historical stock data and calculates various technical indicators such as Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD). Based on the calculated indicators, it generates buy and sell signals. Additionally, it provides functionality for backtesting trading strategies.

### Prerequisites
Before running the script, ensure you have the following dependencies installed:

- yfinance
- pandas_ta
- matplotlib
You can install these dependencies via pip:

```
pip install yfinance pandas_ta matplotlib
```

### Usage
- Clone the Repository: Clone this repository to your local machine.
- Configuration: Edit the config.json file to set your desired parameters such as stock symbol, period, interval, trading strategy parameters, and more.
- Run the Script: Execute the script by running the following command:
```
python trading_indicator.py
```
- Choose Action:
  - Run Test: To execute the trading indicator analysis.
  - Edit Config: To modify the configuration parameters interactively.
### Configuration Parameters
- Symbol: The stock symbol you want to analyze.
- Period: The historical data period to fetch (e.g., 1d, 1mo, 1y).
- Interval: The time interval for data (e.g., 1d, 1h, 15m).
- RSI Length: Length of RSI calculation.
- RSI SMA Length: Length of SMA (Simple Moving Average) for RSI.
- MACD Short: Short period for MACD calculation.
- MACD Long: Long period for MACD calculation.
- MACD Signal: Signal period for MACD calculation.
- Partial Stock: Whether to allow partial stock purchases (e.g., fractional shares).
- Plot: Whether to plot buy/sell signals.
- Backtest: Whether to perform backtesting.
- Capital: Initial capital for backtesting.
- Commission: Commission fee per transaction.
- Stop Loss: Percentage for stop loss point.
- Take Profit: Percentage for take profit point.

### Output
- CSV File: The script saves the analyzed data along with buy/sell signals to a CSV file named symbol.csv.
- Plot (Optional): If enabled, it generates a plot showing buy/sell signals and saves it as symbol.png.
- Backtest Results (Optional): If backtesting is enabled, it prints out the trading transactions and the final profit/loss.
 
### Disclaimer
This script is provided for educational and informational purposes only. It should not be considered financial advice. Always do your own research and consult with a qualified financial professional before making any investment decisions.

### License
This project is licensed under the MIT License. 
