import pandas as pd
import yfinance as yf
from app.config.config import BENCHMARK_TICKER
import streamlit as st


def get_historical_prices(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)

    if data.empty:
        st.error("Yahoo Finance returned empty data. Please check ticker symbols and try again.")
        return None

    # Handle MultiIndex data (whether single or multiple tickers)
    if isinstance(data.columns, pd.MultiIndex):
        try:
            adj_close = data.xs('Adj Close', level=1, axis=1)
            return adj_close
        except KeyError:
            st.error("No 'Adj Close' data found in MultiIndex columns.")
            return None

    # Handle flat DataFrame (only happens for some single tickers)
    if 'Adj Close' in data.columns:
        return pd.DataFrame(data['Adj Close'])

    st.error("Unexpected data format from Yahoo Finance.")
    return None




def get_daily_returns(price):
    """Use the `pct_change` function to calculate daily returns of closing prices for each column"""
    returns = price.pct_change()
    return returns


def get_benchmark_data(start_date, end_date):
    """Get benchmark data for beta calculations"""
    benchmark_prices = get_historical_prices(BENCHMARK_TICKER, start_date, end_date)
    
    if benchmark_prices is None:
        st.error("Benchmark prices could not be retrieved.")
        return None

    benchmark_daily_returns = get_daily_returns(benchmark_prices)

    if benchmark_daily_returns is None or benchmark_daily_returns.empty:
        st.error("Benchmark daily returns could not be computed.")
        return None

    return benchmark_daily_returns.iloc[:, 0]
