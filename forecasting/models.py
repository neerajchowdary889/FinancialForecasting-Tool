# forecasting/models.py
from django.db import models
from django.contrib.auth.models import User

class FinancialData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    expenses = models.DecimalField(max_digits=12, decimal_places=2)
    profit = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically calculate profit before saving
        self.profit = self.revenue - self.expenses
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']

class Forecast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    forecast_date = models.DateField()
    predicted_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    predicted_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    predicted_profit = models.DecimalField(max_digits=12, decimal_places=2)
    confidence_level = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        ordering = ['-forecast_date']

# forecasting/models.py
# Add these models to your existing models.py

class StockPrice(models.Model):
    stock_name = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class StockHistoricalData(models.Model):
    stock_name = models.CharField(max_length=10)
    date = models.DateTimeField()
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    period = models.CharField(max_length=5)  # To store the period used for fetching

    class Meta:
        ordering = ['-date']