# news/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import requests
from .models import StockNews

NEWS_API_KEY = '___API-KEY___'  # Replace with your key

def news_dashboard(request):
    """
    Renders the news dashboard page.
    """
    return render(request, 'news/news_dashboard.html')

@csrf_exempt
def get_stock_news(request, stock_symbol=None):
    """
    Fetches news for a specific stock or all tracked stocks.
    """
    if request.method == 'GET':
        try:
            if stock_symbol:
                news = StockNews.objects.filter(stock_symbol=stock_symbol)
            else:
                news = StockNews.objects.all()
            
            news = news.order_by('-date')[:20].values(
                'id', 'stock_symbol', 'heading', 'date', 'url', 'source'
            )
            return JsonResponse({'news': list(news)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_news_story(request, news_id):
    """
    Fetches a specific news story.
    """
    if request.method == 'GET':
        try:
            news = get_object_or_404(StockNews, id=news_id)
            return JsonResponse({
                'heading': news.heading,
                'full_story': news.full_story,
                'date': news.date,
                'source': news.source,
                'url': news.url,
                'image_url': news.image_url
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def refresh_news(request):
    """
    Fetches fresh news for tracked stocks.
    """
    if request.method == 'POST':
        try:
            # Clear old news (older than 24 hours)
            yesterday = datetime.now() - timedelta(days=1)
            StockNews.objects.filter(created_at__lt=yesterday).delete()
            
            stock_symbols = [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
                'INFY.BO', 'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'WIPRO.BO'
            ]
            
            articles_added = 0
            for symbol in stock_symbols:
                url = (
                    f'https://newsapi.org/v2/everything?'
                    f'q={symbol}&apiKey={NEWS_API_KEY}&'
                    f'sortBy=publishedAt&language=en'
                )
                response = requests.get(url)
                data = response.json()
                
                if data.get('status') == 'ok':
                    for article in data['articles'][:5]:
                        StockNews.objects.create(
                            stock_symbol=symbol,
                            heading=article['title'],
                            full_story=article['content'] or article['description'],
                            date=article['publishedAt'],
                            url=article['url'],
                            source=article['source'].get('name', ''),
                            image_url=article.get('urlToImage')
                        )
                        articles_added += 1
            
            return JsonResponse({
                'status': 'success',
                'message': f'Added {articles_added} new articles'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def search_news(request, stock_symbol):
    """
    Searches for news about a specific stock.
    """
    if request.method == 'GET':
        try:
            url = (
                f'https://newsapi.org/v2/everything?'
                f'q={stock_symbol}&apiKey={NEWS_API_KEY}&'
                f'sortBy=publishedAt&language=en'
            )
            response = requests.get(url)
            data = response.json()
            
            if data.get('status') == 'ok':
                articles_added = 0
                for article in data['articles'][:10]:
                    StockNews.objects.create(
                        stock_symbol=stock_symbol,
                        heading=article['title'],
                        full_story=article['content'] or article['description'],
                        date=article['publishedAt'],
                        url=article['url'],
                        source=article['source'].get('name', ''),
                        image_url=article.get('urlToImage')
                    )
                    articles_added += 1
                
                news = StockNews.objects.filter(stock_symbol=stock_symbol)\
                    .order_by('-date')[:10]\
                    .values('id', 'stock_symbol', 'heading', 'date', 'url', 'source')
                
                return JsonResponse({
                    'status': 'success',
                    'message': f'Found {articles_added} articles',
                    'news': list((news))
                })
            return JsonResponse({'error': 'No news found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)