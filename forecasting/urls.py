from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-data/', views.add_financial_data, name='add_financial_data'),
    path('generate-forecast/', views.generate_forecast, name='generate_forecast'),
    path('stock-dashboard/', views.stock_dashboard, name='stock_dashboard'),
    path('api/stock/<str:stock_name>/price', views.get_stock_price, name='stock_price'),
    path('api/stock/<str:stock_name>/history/<str:period>', views.get_stock_periodic_data, name='stock_history'),
]