import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.data.data_loader import get_historical_prices
from app.config.config import TARGET_MARKET_BETA


def get_portfolio_returns(weights, daily_returns):
    """Use the `dot` function to multiply the weights by each stock's daily return to get the portfolio daily return"""
    portfolio_returns = daily_returns.dot(weights)
    return portfolio_returns


def calculate_risk_parity_weights(returns):
    """Risk Parity: invest such a way that every asset we have in the portfolio has the same risk contribution"""
    # Calculate asset volatilities
    asset_volatility = returns.std(axis=0)

    # Calculate asset risk contributions
    asset_risk_contribution = asset_volatility / asset_volatility.sum()

    # Determine target risk allocation (e.g., equal risk)
    target_risk_allocation = 1 / len(asset_volatility)

    # Calculate weights based on risk contributions
    weights = target_risk_allocation / asset_risk_contribution

    # Normalize weights to sum to 1
    weights /= weights.sum()

    return weights


def calculate_beta(daily_returns, benchmark_returns):
    """Calculate Beta coefficient for each ticker to benchmark, SP500"""
    beta_list = {}
    
    # Iterate over each asset in the portfolio
    for ticker in daily_returns:
        # Calculate covariance between asset returns and benchmark returns
        covariance = daily_returns[ticker].cov(benchmark_returns)
        
        # Calculate variance of benchmark returns
        variance = benchmark_returns.var()
        
        # Calculate beta coefficient
        beta = covariance / variance
        
        # Store beta value in the dictionary
        beta_list[ticker] = beta
    
    # Create a Series from the dictionary
    beta_series = pd.Series(beta_list, name='Beta')
    
    return beta_series


def calculate_beta_weights(data):
    """Calculate New Portfolio Weights Based on Stock Betas"""
    if isinstance(data, pd.Series):
        # If input is a Series, create a DataFrame with one column
        df = pd.DataFrame(data, columns=['Beta'])
    else:
        # If input is already a DataFrame, use it directly
        df = data

    beta_weights = {}
    target_market_beta = TARGET_MARKET_BETA
    sum_of_all_stock_betas = df['Beta'].sum()
    
    for index, row in df.iterrows():
        numerator = target_market_beta - row['Beta']
        denominator = sum_of_all_stock_betas - row['Beta']
        stock_weight = numerator / denominator
        beta_weights[index] = stock_weight
        
    beta_weights_df = pd.DataFrame.from_dict(beta_weights, orient='index', columns=['Weight'])
    beta_weights_df_normalized = beta_weights_df['Weight'] / beta_weights_df['Weight'].sum()
    
    return beta_weights_df_normalized


def portfolio_value_evoluvation(tickers, value_test_weight, years):
    """Calculate portfolio value evolution over time"""
    value_test_weight = np.array(value_test_weight)
    
    if not np.isclose(np.sum(value_test_weight), 1.0, atol=1e-6):
        print(np.sum(value_test_weight))
        print("Sum of weights must be 1.")
        return None

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=years * 365)

    stock_data = get_historical_prices(tickers, start_date, end_date)
    weighted_stock_price = stock_data * value_test_weight
    stock_data.loc[:, "Profit Close"] = weighted_stock_price.sum(axis=1)
    return stock_data