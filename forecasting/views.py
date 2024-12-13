# forecasting/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinancialData, Forecast
from .forms import FinancialDataForm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import yfinance as yf
from .models import StockPrice, StockHistoricalData
from datetime import datetime
import pandas as pd


# @login_required
# def dashboard(request):
#     financial_data = FinancialData.objects.filter(user=request.user).order_by('-date')[:10]
#     forecasts = Forecast.objects.filter(user=request.user).order_by('-forecast_date')[:5]
    
#     context = {
#         'financial_data': financial_data,
#         'forecasts': forecasts,
#     }
#     return render(request, 'forecasting/dashboard.html', context)

@login_required
def dashboard(request):
    context = {
        'us_stocks': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
        'indian_stocks': ['INFY.BO', 'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'WIPRO.BO']
    }
    return render(request, 'forecasting/stock_dashboard.html', context)

@login_required
def add_financial_data(request):
    if request.method == 'POST':
        form = FinancialDataForm(request.POST)
        if form.is_valid():
            financial_data = form.save(commit=False)
            financial_data.user = request.user
            # Calculate profit
            financial_data.profit = financial_data.revenue - financial_data.expenses
            financial_data.save()
            messages.success(request, 'Financial data added successfully!')
            return redirect('dashboard')
    else:
        form = FinancialDataForm()
    
    return render(request, 'forecasting/add_financial_data.html', {'form': form})

@login_required
def generate_forecast(request):
    # Get historical data
    historical_data = FinancialData.objects.filter(user=request.user).values()
    if len(historical_data) < 10:  # Require minimum data points
        messages.warning(request, 'Need more historical data for accurate forecasting')
        return redirect('dashboard')
    
    # Prepare data for ML model
    df = pd.DataFrame(historical_data)
    df['date_ordinal'] = pd.to_datetime(df['date']).apply(lambda x: x.toordinal())
    
    # Simple linear regression for demonstration
    X = df[['date_ordinal']]
    y_revenue = df['revenue']
    
    # Train model
    model = LinearRegression()
    model.fit(X, y_revenue)
    
    # Generate forecast for next 3 months
    last_date = df['date_ordinal'].max()
    future_dates = np.array(range(last_date + 1, last_date + 91)).reshape(-1, 1)
    revenue_forecast = model.predict(future_dates)
    
    # Save forecast
    for i, date_ordinal in enumerate(future_dates):
        Forecast.objects.create(
            user=request.user,
            forecast_date=pd.Timestamp.fromordinal(int(date_ordinal[0])),
            predicted_revenue=revenue_forecast[i],
            predicted_expenses=revenue_forecast[i] * 0.7,  # Simplified expense prediction
            predicted_profit=revenue_forecast[i] * 0.3,
            confidence_level=95.0  # Simplified confidence level
        )
    
    messages.success(request, 'Forecast generated successfully!')
    return redirect('dashboard')

@csrf_exempt
def get_stock_price(request, stock_name):
    if request.method == 'GET':
        try:
            stock = yf.Ticker(stock_name)
            info = stock.info
            current_price = info.get('currentPrice', 'N/A')
            if current_price == 'N/A':
                raise ValueError("No price data found")
            
            # Store in database
            StockPrice.objects.create(
                stock_name=stock_name,
                current_price=current_price
            )
            
            return JsonResponse({
                'stock_name': stock_name,
                'current_price': current_price
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_stock_periodic_data(request, stock_name, period):
    if request.method == 'GET':
        try:
            stock = yf.Ticker(stock_name)
            historical_data = stock.history(period=period)
            if historical_data.empty:
                raise ValueError("No data found for the given period")
            
            # Store in database
            for index, row in historical_data.iterrows():
                StockHistoricalData.objects.create(
                    stock_name=stock_name,
                    date=index,
                    close_price=row['Close'],
                    open_price=row['Open'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    volume=row['Volume'],
                    period=period
                )
            
            # Format data for visualization
            chart_data = historical_data.reset_index().to_dict('records')
            
            return JsonResponse({
                'stock_name': stock_name,
                'period': period,
                'data': chart_data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def stock_dashboard(request):
    context = {
        'us_stocks': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
        'indian_stocks': ['INFY.BO', 'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'WIPRO.BO']
    }
    return render(request, 'forecasting/stock_dashboard.html', context)