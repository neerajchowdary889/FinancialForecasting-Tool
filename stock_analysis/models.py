# stock_analysis/models.py
from django.db import models
from django.contrib.auth.models import User

class StockAnalysis(models.Model):
    stock_symbol = models.CharField(max_length=20)
    analysis_date = models.DateTimeField(auto_now_add=True)
    price_summary = models.TextField()
    news_summary = models.TextField()
    sentiment_analysis = models.TextField()
    investment_recommendation = models.TextField()
    overall_score = models.FloatField()  # 0 to 1 score
    
    class Meta:
        ordering = ['-analysis_date']
        verbose_name_plural = 'Stock Analyses'

    def __str__(self):
        return f"{self.stock_symbol} Analysis - {self.analysis_date.date()}"