import numpy as np
from scipy.optimize import minimize
from app.config.config import NUMBER_OF_PORTFOLIOS


def calculate_sharpe_ratio_optimization(prices, num_tickers):
    """Calculate optimal portfolio weights using Sharpe ratio optimization"""
    returns_marco = prices/(prices.shift(1))
    returns_marco.dropna(inplace=True)
    logreturns = np.log(returns_marco)
    meanlog = logreturns.mean()
    no_porfolio = NUMBER_OF_PORTFOLIOS
    test_weight = np.zeros((no_porfolio, num_tickers))
    sigma = logreturns.cov()
    test_return = np.zeros(no_porfolio)
    test_volatility = np.zeros(no_porfolio)
    sharpratio = np.zeros(no_porfolio)
    
    for k in range(no_porfolio):
        random_weight = np.array(np.random.random(num_tickers))
        random_weight = random_weight/sum(random_weight)
        test_weight[k,:] = random_weight
        #log returns
        test_return[k] = np.sum(meanlog * random_weight) 
        #volatility
        test_volatility[k] = np.sqrt(np.dot(random_weight.T, np.dot(sigma, random_weight)))
        #sharp ratio
        sharpratio[k] = test_return[k]/test_volatility[k]
    
    max_sharpratio = sharpratio.argmax()
    sharpratio_weight = test_weight[max_sharpratio,:]
    
    return {
        'test_volatility': test_volatility,
        'test_return': test_return,
        'sharpratio': sharpratio,
        'max_sharpratio': max_sharpratio,
        'sharpratio_weight': sharpratio_weight,
        'meanlog': meanlog,
        'sigma': sigma
    }


def calculate_markowitz_optimization(meanlog, sigma, num_tickers, test_return):
    """Calculate Markowitz optimal portfolio"""
    def negative_sharpratio(random_weight):
        random_weights = np.array(random_weight)
        R = np.sum(meanlog*random_weights)
        V = np.sqrt(np.dot(random_weight.T, np.dot(sigma, random_weights)))
        SR = R/V
        return -SR
    
    def checksumtoone(random_weight):
        return np.sum(random_weight)-1
    
    w_0 = [1/num_tickers for _ in range(num_tickers)]
    bounds = [(0,1) for _ in range(num_tickers)]
    constraints = ({'type':'eq','fun':checksumtoone})
    optimal_weight = minimize(negative_sharpratio, w_0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Calculate efficient frontier
    returns = np.linspace(0, max(test_return), 50)
    optimal_volatility = []  
    
    def minmizevolatility(random_weight):
        random_weights = np.array(random_weight)
        V = np.sqrt(np.dot(random_weight.T, np.dot(sigma, random_weights)))
        return V
    
    def getreturn(w):
        w = np.array(w)
        R = np.sum(meanlog*w)
        return R

    for r in returns:
        #find best volatility
        constraints = ({'type':'eq','fun':checksumtoone},{'type':'eq','fun': lambda random_weight: getreturn(random_weight)- r})
        optimal = minimize(minmizevolatility, w_0, method='SLSQP', bounds=bounds, constraints=constraints)
        optimal_volatility.append(optimal['fun'])
    
    return {
        'optimal_weight': optimal_weight,
        'returns': returns,
        'optimal_volatility': optimal_volatility
    }