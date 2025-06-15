from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import datetime

client = StockHistoricalDataClient("PK42HK5LWV6SG0BYOZPM", "7rgloEtC4DdlQJLWbFc9RUksBLeakt0ES9yiu6I6")

def get_stock_data(symbol: str):
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=datetime.datetime.now() - datetime.timedelta(days=90),
        end=datetime.datetime.now()
    )
    bars = client.get_stock_bars(request_params)
    return bars.df
