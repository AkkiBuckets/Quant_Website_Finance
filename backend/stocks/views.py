from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_stock_data
from .quant import calculate_returns, plot_efficient_frontier
from .models import SavedPortfolio
from django.views.generic import TemplateView
import numpy as np

@api_view(['POST'])
def stock_analysis(request):
    symbols = request.data.get('symbols', [])  # Expecting a list of tickers
    rf = 0.01  # Risk-free rate
    returns_data = {}

    # 🔁 Fetch and compute returns for each stock
    for symbol in symbols:
        df = get_stock_data(symbol)
        if df.empty or 'close' not in df:
            return Response({'error': f"Data for {symbol} not found or invalid"}, status=400)
        returns_data[symbol] = calculate_returns(df['close']).dropna()

    # 📊 Align all return series by date
    returns_df = np.array([returns_data[s].values[-60:] for s in symbols])
    mean_returns = np.mean(returns_df, axis=1)
    cov_matrix = np.cov(returns_df)

    # ⚖️ Equal weight portfolio
    weights = np.ones(len(symbols)) / len(symbols)
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (portfolio_return - rf) / portfolio_std

    # 📈 Treynor’s Ratio approximation using average beta
    market_returns = np.mean(returns_df, axis=0)
    portfolio_beta = np.cov(np.mean(returns_df, axis=0), market_returns)[0, 1] / np.var(market_returns)
    treynor_ratio = (portfolio_return - rf) / portfolio_beta if portfolio_beta != 0 else None

    # 🖼 Efficient Frontier Graph
    graph_base64 = plot_efficient_frontier(mean_returns, cov_matrix, rf)

    return Response({
        'expected_return': round(float(portfolio_return), 4),
        'std_deviation': round(float(portfolio_std), 4),
        'sharpe_ratio': round(float(sharpe_ratio), 4),
        'treynor_ratio': round(float(treynor_ratio), 4) if treynor_ratio else "N/A",
        'graph': graph_base64
    })


@api_view(['POST'])
def save_portfolio(request):
    data = request.data
    portfolio = SavedPortfolio.objects.create(
        portfolio_name=data['portfolio_name'],
        user_name=data.get('user_name', ''),
        tickers=",".join(data['symbols']),
        expected_return=data['expected_return'],
        std_deviation=data['std_deviation'],
        sharpe_ratio=data['sharpe_ratio'],
        treynor_ratio=data['treynor_ratio'],
    )
    return Response({
        'message': '✅ Portfolio saved successfully!',
        'id': portfolio.id
    })

class FrontendAppView(TemplateView):
    template_name = "index.html"
