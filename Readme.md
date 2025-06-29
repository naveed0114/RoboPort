# RoboPort - Portfolio Optimization Tool

A Streamlit-based portfolio optimization application that helps users analyze and optimize their investment portfolios using various financial models and strategies.

## Features

- **Portfolio Analysis**: Analyze your current portfolio allocation
- **Risk Parity**: Equal risk contribution allocation strategy
- **Beta-based Optimization**: Portfolio optimization based on beta coefficients
- **Sharpe Ratio Optimization**: Maximize risk-adjusted returns
- **Markowitz Optimization**: Modern Portfolio Theory implementation
- **Interactive Visualizations**: Charts and graphs for better understanding
- **Performance Comparison**: Compare different allocation strategies

## Project Structure

```
roboport/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
├── config/
│   ├── __init__.py
│   └── config.py              # Configuration settings
├── data/
│   ├── __init__.py
│   └── data_loader.py         # Data retrieval and loading functions
├── calculations/
│   ├── __init__.py
│   ├── portfolio_calculations.py  # Portfolio calculation functions
│   └── optimization.py        # Optimization algorithms
├── visualization/
│   ├── __init__.py
│   └── visualization.py       # Plotting and visualization functions
├── analysis/
│   ├── __init__.py
│   └── portfolio_analyzer.py  # Portfolio analysis and comparison
└── ui/
    ├── __init__.py
    └── ui_components.py        # Streamlit UI components
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd roboport
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`)

3. Enter your portfolio details:
   - Total portfolio amount
   - Number of tickers
   - Ticker symbols and their percentages

4. Click "Submit" to analyze your portfolio

## Modules Description

### config/config.py
Contains all configuration settings including:
- Date settings
- Portfolio parameters
- Optimization settings
- Plot configurations

### data/data_loader.py
Handles data retrieval from Yahoo Finance:
- Historical price data
- Daily returns calculation
- Benchmark data loading

### calculations/portfolio_calculations.py
Core portfolio calculation functions:
- Portfolio returns calculation
- Risk parity weights
- Beta calculations
- Portfolio value evolution

### calculations/optimization.py
Advanced optimization algorithms:
- Sharpe ratio optimization
- Markowitz optimization
- Efficient frontier calculation

### visualization/visualization.py
All plotting and charting functions:
- Pie charts for portfolio weights
- Line plots for price history
- Scatter plots for optimization results
- Portfolio evolution charts

### analysis/portfolio_analyzer.py
Portfolio analysis and comparison:
- Strategy performance analysis
- Best strategy identification
- Results comparison

### ui/ui_components.py
Streamlit UI component functions:
- Input forms
- Display functions
- Headers and formatting

## Dependencies

- streamlit: Web application framework
- pandas: Data manipulation and analysis
- numpy: Numerical computing
- yfinance: Yahoo Finance data retrieval
- matplotlib: Plotting and visualization
- scipy: Scientific computing and optimization

## Key Features Explained

### Risk Parity
Allocates portfolio weights so that each asset contributes equally to the overall portfolio risk.

### Beta-based Optimization
Uses beta coefficients (relative to S&P 500) to optimize portfolio allocation for desired market exposure.

### Sharpe Ratio Optimization
Maximizes the risk-adjusted return by optimizing the ratio of excess return to volatility.

### Markowitz Optimization
Implements Modern Portfolio Theory to find the optimal portfolio on the efficient frontier.

## Output

The application provides:
- Portfolio weight recommendations
- Performance comparisons across strategies
- Interactive charts and visualizations
- Historical performance analysis
- Risk metrics and statistics

## Notes

- The application uses Yahoo Finance for historical data
- Analysis is based on 1-year historical data by default
- Portfolio evolution analysis covers 3 years by default
- All settings can be modified in the config file