# stock_analysis/admin.py
from django.contrib import admin
from .models import StockAnalysis

@admin.register(StockAnalysis)
class StockAnalysisAdmin(admin.ModelAdmin):
    list_display = ('stock_symbol', 'analysis_date', 'overall_score')
    search_fields = ('stock_symbol',)
    list_filter = ('analysis_date',)