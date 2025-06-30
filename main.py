import streamlit as st
from datetime import datetime, timedelta

# Import custom modules
from app.config.config import HISTORICAL_PERIOD_DAYS, BENCHMARK_TICKER, PORTFOLIO_EVOLUTION_YEARS
from app.ui.ui_components import (
    display_header, get_portfolio_amount, get_ticker_inputs, 
    display_ticker_weights, display_section_header, display_dataframe,
    display_percentage_return, display_recommendation
)
from app.data.data_loader import get_historical_prices, get_daily_returns, get_benchmark_data
from app.calculations.portfolio_calculations import (
    get_portfolio_returns, calculate_risk_parity_weights, 
    calculate_beta, calculate_beta_weights
)
from app.calculations.optimization import calculate_sharpe_ratio_optimization, calculate_markowitz_optimization
from app.visualization.visualization import (
    create_pie_chart, plot_historical_prices, plot_daily_returns,
    plot_portfolio_returns, plot_portfolio_evolution, plot_sharpe_ratio_scatter,
    plot_efficient_frontier
)
from app.analysis.portfolio_analyzer import PortfolioAnalyzer


def main():
    """Main application function"""
    # Display header
    display_header()
    
    # Get portfolio amount
    amount = get_portfolio_amount()  # noqa: F841
    
    # Get ticker inputs
    ticker_percentage, num_tickers, invalid_tickers = get_ticker_inputs()
    
    # Button to display entered data
    if st.button('Submit'):
        if invalid_tickers:
            st.error(f"Invalid or unsupported tickers: {', '.join(invalid_tickers)}. Please correct them.")
        elif abs(sum(ticker_percentage.values()) - 1.0) > 0.01:
            st.error("The weights must sum to 100%.")
        elif not ticker_percentage:
            st.error("Please enter at least one valid ticker.")
        else:
            display_ticker_weights(ticker_percentage)
            
            # Extract tickers and weights
            tickers = list(ticker_percentage.keys())
            weights = list(ticker_percentage.values())
            
            # Create pie chart of portfolio weights
            create_pie_chart(weights, tickers, 'Pie Chart of Portfolio Weights')
            
            # Get date range
            end_date = datetime.today().date()
            start_date = end_date - timedelta(days=HISTORICAL_PERIOD_DAYS)
            
            # Get historical prices
            prices = get_historical_prices(tickers, start_date, end_date)
            display_dataframe(prices, "Historic Prices for the past year")
            
            # Plot historical prices
            if prices is not None:
                plot_historical_prices(prices)
            else:
                st.write("Historical prices not available.")
            
            # Calculate and display daily returns
            daily_returns = get_daily_returns(prices)
            display_dataframe(daily_returns, "Daily Returns (pct_change)")
            plot_daily_returns(daily_returns)
            
            # Calculate and display portfolio daily returns
            port_daily_return = get_portfolio_returns(weights, daily_returns)
            display_dataframe(port_daily_return, "Portfolio Daily Returns")
            plot_portfolio_returns(port_daily_return)
            
            # Calculate Beta
            benchmark_daily_returns = get_benchmark_data(start_date, end_date)
            betas = calculate_beta(daily_returns, benchmark_daily_returns)
            display_dataframe(betas, f"Beta Coefficient By Tickers benchmarked with {BENCHMARK_TICKER}")
            
            # Calculate beta weights
            beta_weight = calculate_beta_weights(betas)
            display_dataframe(beta_weight, "Beta weight")
            
            # Calculate risk parity weights
            risk_parity_weights = calculate_risk_parity_weights(daily_returns)
            display_dataframe(risk_parity_weights, "Risk Parity Weights")
            create_pie_chart(risk_parity_weights, tickers, 'Risk Parity (Equally weighted portfolio)')

            # Initialize portfolio analyzer
            analyzer = PortfolioAnalyzer(tickers)
            
            # Analyze original portfolio
            original_portfolio_value, total_return_original = analyzer.analyze_strategy('User', weights, PORTFOLIO_EVOLUTION_YEARS)
            if original_portfolio_value is not None:
                display_section_header('Total return on initial allocation')
                plot_portfolio_evolution(original_portfolio_value, "Portfolio Value Evolution (10 years) using user allocation")
                display_percentage_return("Total portfolio return on user allocation", total_return_original)
            else:
                print(f"following data from original in case of none {original_portfolio_value}, {total_return_original}")
            
            # Analyze risk parity portfolio
            rp_portfolio_value, total_return_rp = analyzer.analyze_strategy('Risk Parity', risk_parity_weights, PORTFOLIO_EVOLUTION_YEARS)
            if rp_portfolio_value is not None:
                display_section_header('Total return on risk parity allocation')
                plot_portfolio_evolution(rp_portfolio_value, "Portfolio Value Evolution (10 years) using Risk parity")
                display_percentage_return("Total portfolio return on risk parity allocation", total_return_rp)
            else:
                print(f"following data from rp in case of none {rp_portfolio_value}, {total_return_rp}")
            
            # Analyze beta portfolio
            beta_portfolio_value, total_return_beta = analyzer.analyze_strategy('Beta', beta_weight, PORTFOLIO_EVOLUTION_YEARS)
            if beta_portfolio_value is not None:
                display_section_header('Total return on Beta Weight allocation')
                plot_portfolio_evolution(beta_portfolio_value, "Portfolio Value Evolution (10 years) using Beta Weights")
                display_percentage_return("Total portfolio return beta allocation", total_return_beta)
            else:
                print(f"following data from bet in case of none {beta_portfolio_value}, {total_return_beta}")
            
            # Sharpe Ratio Analysis
            display_section_header('Sharp Ratio')
            sharpe_data = calculate_sharpe_ratio_optimization(prices, num_tickers)
            
            display_section_header('Sharpe ratio of 10000 random weights')
            plot_sharpe_ratio_scatter(
                sharpe_data['test_volatility'], 
                sharpe_data['test_return'], 
                sharpe_data['sharpratio'], 
                sharpe_data['max_sharpratio']
            )
            
            # Analyze Sharpe ratio portfolio
            sr_portfolio_value, total_return_sr = analyzer.analyze_strategy('Sharp Ratio', sharpe_data['sharpratio_weight'], PORTFOLIO_EVOLUTION_YEARS)
            if sr_portfolio_value is not None:
                plot_portfolio_evolution(sr_portfolio_value, "Portfolio Value Evolution (10 years) using Sharp Ratio")
                display_percentage_return("Total portfolio return with Sharp ratio", total_return_sr)
            else:
                print(f"following data from sharpe in case of none {sr_portfolio_value}, {total_return_sr}")
            
            # Markowitz Analysis
            markowitz_data = calculate_markowitz_optimization(
                sharpe_data['meanlog'], 
                sharpe_data['sigma'], 
                num_tickers, 
                sharpe_data['test_return']
            )
            
            # Plot efficient frontier
            plot_efficient_frontier(
                sharpe_data['test_volatility'],
                sharpe_data['test_return'],
                sharpe_data['sharpratio'],
                sharpe_data['max_sharpratio'],
                markowitz_data['optimal_volatility'],
                markowitz_data['returns']
            )
            
            # Analyze Markowitz portfolio
            marcovic_portfolio_value, total_return_markowitz = analyzer.analyze_strategy('Markowitz', markowitz_data['optimal_weight'].x, PORTFOLIO_EVOLUTION_YEARS)
            if marcovic_portfolio_value is not None:
                display_section_header('Markowitz portfolio solver')
                plot_portfolio_evolution(marcovic_portfolio_value, "Portfolio Value Evolution (10 years) using Markowitz")
                display_percentage_return("Total portfolio return using markovic", total_return_markowitz)
            else:
                print(f"following data from markowitz in case of none {marcovic_portfolio_value}, {total_return_markowitz}")
            
            # Get best strategy and display recommendation
            best_strategy, best_return = analyzer.get_best_strategy()
            display_recommendation(best_strategy)
            
            # Display corresponding weights based on best strategy
            if best_strategy == 'Risk Parity':
                create_pie_chart(risk_parity_weights, tickers)
                df = analyzer.create_recommendation_dataframe(best_strategy, risk_parity_weights)
                st.write(df)
            elif best_strategy == 'Markowitz':
                create_pie_chart(markowitz_data['optimal_weight'].x, tickers)
                df = analyzer.create_recommendation_dataframe(best_strategy, markowitz_data['optimal_weight'].x)
                st.write(df)
            elif best_strategy == 'User':
                create_pie_chart(weights, tickers)
                st.write("Do not make changes to your allocation")
                df = analyzer.create_recommendation_dataframe(best_strategy, weights)
                st.write(df)
            elif best_strategy == 'Beta':
                create_pie_chart(beta_weight, tickers)
                df = analyzer.create_recommendation_dataframe(best_strategy, beta_weight)
                st.write(df)
            elif best_strategy == 'Sharp Ratio':
                create_pie_chart(sharpe_data['sharpratio_weight'], tickers)
                df = analyzer.create_recommendation_dataframe(best_strategy, sharpe_data['sharpratio_weight'])
                st.write(df)
            
            

if __name__ == "__main__":
    main()