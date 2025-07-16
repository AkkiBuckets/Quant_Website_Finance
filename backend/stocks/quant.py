import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def calculate_returns(prices):
    return np.log(prices / prices.shift(1))

def calculate_capm(rf, market_returns, stock_returns):
    beta = np.cov(stock_returns[1:], market_returns[1:])[0][1] / np.var(market_returns[1:])
    expected_return = rf + beta * (market_returns.mean() - rf)
    return beta, expected_return

def plot_efficient_frontier(mean_returns, cov_matrix, rf, num_portfolios=5000):
    results = np.zeros((3, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(len(mean_returns))
        weights /= np.sum(weights)

        portfolio_return = np.dot(weights, mean_returns)
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - rf) / portfolio_std

        results[0, i] = portfolio_return
        results[1, i] = portfolio_std
        results[2, i] = sharpe_ratio
        weights_record.append(weights)

    max_sharpe_idx = np.argmax(results[2])
    min_vol_idx = np.argmin(results[1])

    # 🎨 Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='viridis', marker='o', s=10, alpha=0.6)
    plt.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx], color='r', marker='*', s=200, label='Max Sharpe Ratio')
    plt.scatter(results[1, min_vol_idx], results[0, min_vol_idx], color='b', marker='X', s=200, label='GMV Portfolio')
    plt.title('Efficient Frontier')
    plt.xlabel('Volatility (Std Dev)')
    plt.ylabel('Expected Return')
    plt.legend()

    # 🔄 Convert plot to base64 image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return graph_base64
