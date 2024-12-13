# news/admin.py
from django.contrib import admin
from .models import StockNews

@admin.register(StockNews)
class StockNewsAdmin(admin.ModelAdmin):
    list_display = ('stock_symbol', 'heading', 'date', 'source')
    list_filter = ('stock_symbol', 'source', 'created_at')
    search_fields = ('heading', 'full_story', 'stock_symbol')
    ordering = ('-date',)