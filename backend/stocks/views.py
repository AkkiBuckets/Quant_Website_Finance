from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_stock_data
from .quant import calculate_returns, calculate_capm

@api_view(['POST'])
def stock_analysis(request):
    symbol = request.data.get('symbol', 'AAPL')  # POST data
    df = get_stock_data(symbol)
    returns = calculate_returns(df['close'])
    rf = 0.01  # example risk-free rate
    market_returns = returns  # dummy for now
    beta, exp_ret = calculate_capm(rf, market_returns, returns)
    return Response({'beta': beta, 'expected_return': exp_ret})
