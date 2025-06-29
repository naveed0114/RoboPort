import yfinance as yf

def is_valid_ticker(ticker):
    try:
        info = yf.Ticker(ticker).info
        # Check if the ticker has market data
        return info and 'regularMarketPrice' in info and info['regularMarketPrice'] is not None
    except Exception:
        return False


