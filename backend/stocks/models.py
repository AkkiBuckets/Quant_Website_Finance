from django.db import models

class SavedPortfolio(models.Model):
    portfolio_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    tickers = models.TextField()
    expected_return = models.FloatField()
    std_deviation = models.FloatField()
    sharpe_ratio = models.FloatField()
    treynor_ratio = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
