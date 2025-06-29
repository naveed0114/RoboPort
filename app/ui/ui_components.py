import streamlit as st
from config.config import MIN_TICKERS, MAX_TICKERS, DEFAULT_TICKERS
from utils.utils import is_valid_ticker


def display_header():
    """Display the main header"""
    st.title('Welcome to RoboPort')
    st.subheader('Your ultimate robo portfolio optimization tool')


def get_portfolio_amount():
    """Get portfolio amount from user"""
    total_amount = st.number_input("Please enter the total dollar amount in your portfolio?:")
    amount = float(total_amount)
    formatted_amount = "${:,.2f}".format(amount)
    st.write('Total portfolio amount:', formatted_amount)
    return amount


def get_ticker_inputs():
    """Get ticker symbols and percentages from user"""
    st.subheader('Please enter the tickers in your portfolio and their respective percentages')
    
    # Initialize a dictionary to store ticker symbols and percentages
    ticker_percentage = {}
    invalid_tickers = []
    
    # Define the number of ticker symbols to input
    num_tickers = st.number_input('Number of tickers:', min_value=MIN_TICKERS, max_value=MAX_TICKERS, value=DEFAULT_TICKERS, step=1)
    
    # Input fields for ticker symbols and percentages
    for i in range(1, num_tickers + 1):
        ticker = st.text_input(f'Ticker {i}:', key=f'ticker_{i}').strip().upper()
        percentage = st.number_input(f'Percentage {i} ({ticker}):', key=f'percentage_{i}')
        if ticker:  # only validate non-empty input
            if is_valid_ticker(ticker):
                ticker_percentage[ticker] = percentage / 100
            else:
                invalid_tickers.append(ticker)
    
    return ticker_percentage, num_tickers, invalid_tickers


def display_ticker_weights(ticker_percentage):
    """Display entered ticker weights"""
    for ticker, percentage in ticker_percentage.items():
        st.write(f'Ticker: {ticker}, weight: {percentage}')


def display_section_header(title):
    """Display a section header"""
    st.subheader(title)


def display_dataframe(data, title=None):
    """Display a DataFrame with optional title"""
    if title:
        st.subheader(title)
    st.write(data)


def display_metric(label, value):
    """Display a metric"""
    st.write(f"{label}: {value}")


def display_percentage_return(label, return_value):
    """Display a percentage return"""
    st.write(f"{label}: {return_value:.2%}")


def display_recommendation(strategy_name):
    """Display the best strategy recommendation"""
    st.write(f"As per analysis using various methods the best return is got from using : {strategy_name}'s strategy. Below is the recommended distribution to get the best return:")
    st.write("Corresponding weights")