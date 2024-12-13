# financial_forecasting/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'),  # Homepage
    path('accounts/register/', accounts_views.register, name='register'),  # Registration
    path('accounts/', include('django.contrib.auth.urls')),  # Login/logout
    path('', include('forecasting.urls')),  # Forecasting URLs
    path('news/', include('news.urls', namespace='news')),
    path('stock-analysis/', include('stock_analysis.urls', namespace='stock_analysis')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]