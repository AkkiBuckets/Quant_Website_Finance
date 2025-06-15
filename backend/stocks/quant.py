import numpy as np

def calculate_returns(prices):
    return np.log(prices / prices.shift(1))

def calculate_capm(rf, market_returns, stock_returns):
    beta = np.cov(stock_returns[1:], market_returns[1:])[0][1] / np.var(market_returns[1:])
    expected_return = rf + beta * (market_returns.mean() - rf)
    return beta, expected_return
