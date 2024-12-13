# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_dashboard, name='dashboard'),
    path('api/headlines/', views.get_stock_news, name='headlines'),
    path('api/stock/<str:stock_symbol>/', views.get_stock_news, name='stock_news'),
    path('api/story/<int:news_id>/', views.get_news_story, name='story'),
    path('api/refresh/', views.refresh_news, name='refresh'),
    path('api/search/<str:stock_symbol>/', views.search_news, name='search'),
]