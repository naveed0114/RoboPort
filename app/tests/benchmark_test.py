import yfinance as yf
from datetime import datetime, timedelta
from config.config import BENCHMARK_TICKER, HISTORICAL_PERIOD_DAYS
tickers = [BENCHMARK_TICKER]
end_date = datetime.today().date()
start_date = end_date - timedelta(days=HISTORICAL_PERIOD_DAYS)
data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)

print(data)