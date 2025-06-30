import pandas as pd
from app.calculations.portfolio_calculations import portfolio_value_evoluvation


class PortfolioAnalyzer:
    """Class to analyze and compare different portfolio strategies"""
    
    def __init__(self, tickers):
        self.tickers = tickers
        self.return_values = {}
    
    def analyze_strategy(self, strategy_name, weights, years=3):
        """Analyze a specific portfolio strategy"""
        portfolio_value = portfolio_value_evoluvation(self.tickers, weights, years)
        
        if portfolio_value is not None:
            total_return = (portfolio_value['Profit Close'][-1]/portfolio_value['Profit Close'][0])-1
            self.return_values[strategy_name] = total_return
            return portfolio_value, total_return
        else:
            self.return_values[strategy_name] = 0
            return None, 0
    
    def get_best_strategy(self):
        """Get the strategy with the best return"""
        if not self.return_values:
            return None, 0
        
        best_strategy = max(self.return_values, key=lambda k: self.return_values[k])
        best_return = self.return_values[best_strategy]
        return best_strategy, best_return
    
    def get_all_returns(self):
        """Get all strategy returns"""
        return self.return_values
    
    def create_recommendation_dataframe(self, strategy_name, weights):
        """Create a DataFrame for weight recommendations"""
        return pd.DataFrame({'Key': self.tickers, 'Value': weights})