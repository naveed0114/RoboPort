import matplotlib.pyplot as plt
import streamlit as st

from app.config.config import (
    PLOT_FIGURE_SIZE, PLOT_FONT_SIZE, STANDARD_FIGURE_SIZE
)


def create_pie_chart(weights, labels, title=None, threshold=1e-2):
    """
    Create a pie chart for portfolio weights, filtering out near-zero values to avoid label overlap.

    Parameters:
    - weights: list of float
    - labels: list of str
    - title: str (optional)
    - threshold: float (weights below this are ignored in the chart)
    """

    # Filter weights and labels
    filtered_weights = []
    filtered_labels = []

    for w, la in zip(weights, labels):
        if w >= threshold:
            filtered_weights.append(w)
            filtered_labels.append(la)

    fig, ax = plt.subplots()
    ax.pie(filtered_weights, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    if title:
        st.subheader(title)
    st.pyplot(fig)


def plot_historical_prices(prices):
    """Plot historical prices"""
    plt.figure(figsize=STANDARD_FIGURE_SIZE)
    for column in prices.columns:
        plt.plot(prices.index, prices[column], label=column)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Historic Prices for the past year')
    plt.legend()
    st.pyplot(plt)


def plot_daily_returns(daily_returns):
    """Plot daily returns"""
    plt.figure(figsize=STANDARD_FIGURE_SIZE)
    for column in daily_returns.columns:
        plt.plot(daily_returns.index, daily_returns[column], label=column)
    plt.xlabel('Date')
    plt.ylabel('Percentage Change')
    plt.title('Percentage Change of Daily Returns')
    plt.legend()
    st.pyplot(plt)


def plot_portfolio_returns(port_daily_return):
    """Plot portfolio returns"""
    plt.figure(figsize=STANDARD_FIGURE_SIZE)
    plt.plot(port_daily_return.index, port_daily_return, label='Portfolio Returns')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Returns')
    plt.title('Portfolio Returns Over Time')
    plt.legend()
    st.pyplot(plt)


def plot_portfolio_evolution(portfolio_value, title):
    """Plot portfolio value evolution"""
    plt.figure(figsize=PLOT_FIGURE_SIZE)
    plt.title(title, fontsize=PLOT_FONT_SIZE)
    plt.plot(portfolio_value["Profit Close"], color='blue')
    plt.xlabel('Date', fontsize=PLOT_FONT_SIZE)
    plt.ylabel('Value in $', fontsize=PLOT_FONT_SIZE)
    st.pyplot(plt)


def plot_sharpe_ratio_scatter(test_volatility, test_return, sharpratio, max_sharpratio):
    """Plot Sharpe ratio scatter plot"""
    plt.figure(figsize=PLOT_FIGURE_SIZE)
    plt.scatter(test_volatility, test_return, c=sharpratio)
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.scatter(test_volatility[max_sharpratio], test_return[max_sharpratio], c='black')
    st.pyplot(plt)


def plot_efficient_frontier(test_volatility, test_return, sharpratio, max_sharpratio, optimal_volatility, returns):
    """Plot efficient frontier with Sharpe ratio"""
    plt.figure(figsize=PLOT_FIGURE_SIZE)
    plt.scatter(test_volatility, test_return, c=sharpratio)
    plt.xlabel('volatility', fontsize=PLOT_FONT_SIZE)
    plt.ylabel('return', fontsize=PLOT_FONT_SIZE)
    plt.colorbar(label='Sharpe Ratio')
    plt.scatter(test_volatility[max_sharpratio], test_return[max_sharpratio], c='black')
    plt.plot(optimal_volatility, returns, '--')
    st.pyplot(plt)