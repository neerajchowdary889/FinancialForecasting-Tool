# news/models.py
from django.db import models

class StockNews(models.Model):
    stock_symbol = models.CharField(max_length=20)
    heading = models.CharField(max_length=500)
    full_story = models.TextField()
    date = models.DateTimeField()
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Stock News'

    def __str__(self):
        return f"{self.stock_symbol} - {self.heading[:50]}..."