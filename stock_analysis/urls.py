# stock_analysis/urls.py
from django.urls import path
from . import views

app_name = 'stock_analysis'

urlpatterns = [
    path('', views.stock_analysis_dashboard, name='dashboard'),
    path('analyze/<str:stock_symbol>/', views.analyze_stock, name='analyze'),
]