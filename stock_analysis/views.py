from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import yfinance as yf
import google.generativeai as genai
from django.shortcuts import render
from datetime import datetime
import json
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini AI with error handling
GOOGLE_API_KEY = '___API-KEY___'  # Replace with your actual API key
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Use generation config to control output
    generation_config = {
        'temperature': 0.7,
        'max_output_tokens': 2048,
    }
    model = genai.GenerativeModel(
        'gemini-1.5-flash', 
        generation_config=generation_config
    )
except Exception as e:
    logger.error(f"Error configuring Gemini AI: {str(e)}")
    model = None

def stock_analysis_dashboard(request):
    return render(request, 'stock_analysis/dashboard.html')

def extract_json_from_text(text):
    """
    Extract JSON from text, handling markdown code block syntax
    """
    # Remove markdown code block syntax
    text = text.strip()
    
    # Remove ```json and ``` if present
    if text.startswith('```json'):
        text = text[7:]
    if text.endswith('```'):
        text = text[:-3]
    
    # Try to parse the cleaned text
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from text: {text}")
        return None

@csrf_exempt
def analyze_stock(request, stock_symbol):
    try:
        # Fetch stock data
        stock = yf.Ticker(stock_symbol)
        hist_data = stock.history(period="1y")
        
        if hist_data.empty:
            return JsonResponse({
                'status': 'error',
                'message': 'No historical data found for this stock'
            }, status=404)

        # Process price data
        price_data = {
            'start_price': round(float(hist_data.iloc[0]['Close']), 2),
            'end_price': round(float(hist_data.iloc[-1]['Close']), 2),
            'high': round(float(hist_data['High'].max()), 2),
            'low': round(float(hist_data['Low'].min()), 2),
            'volume_avg': int(hist_data['Volume'].mean()),
            'price_change': round(((hist_data.iloc[-1]['Close'] - hist_data.iloc[0]['Close']) 
                           / hist_data.iloc[0]['Close'] * 100), 2)
        }

        # Get news with error handling
        try:
            news = stock.news[:5]
            news_data = [{'title': n['title'], 
                         'date': datetime.fromtimestamp(n['providerPublishTime']).strftime('%Y-%m-%d')} 
                        for n in news]
        except Exception as e:
            logger.warning(f"Error fetching news: {str(e)}")
            news_data = []

        # If Gemini API is not available, provide basic analysis
        if model is None:
            analysis = {
                "price_summary": f"Stock {stock_symbol} has moved {price_data['price_change']}% over the past year.",
                "news_summary": "News analysis currently unavailable",
                "technical_analysis": f"Price range: ${price_data['low']} - ${price_data['high']}",
                "investment_recommendation": "Analysis service temporarily unavailable",
                "risk_factors": "Unable to analyze risks at the moment",
                "sentiment_score": 0.5
            }
        else:
            try:
                prompt = f"""
                Analyze this stock ({stock_symbol}) based on the following data:
                
                Price Analysis:
                - Starting Price (1 year ago): ${price_data['start_price']}
                - Current Price: ${price_data['end_price']}
                - 52-Week High: ${price_data['high']}
                - 52-Week Low: ${price_data['low']}
                - Price Change: {price_data['price_change']}%
                - Average Daily Volume: {price_data['volume_avg']:,}

                Recent News Headlines:
                {', '.join([n['title'] for n in news_data]) if news_data else 'No recent news available'}

                Provide a JSON analysis with these keys:
                - price_summary: Concise price performance analysis
                - news_summary: Brief news sentiment analysis
                - technical_analysis: Key technical indicators
                - investment_recommendation: Clear stock recommendation
                - risk_factors: Important risks to consider
                - sentiment_score: Numerical sentiment (0-1)

                Respond ONLY with the valid JSON. No additional text.
                """

                # Use generate_content with JSON-specific instructions
                response = model.generate_content(prompt)
                
                # Extract and parse JSON
                analysis = extract_json_from_text(response.text)
                
                # Fallback if JSON extraction fails
                if analysis is None:
                    analysis = {
                        "price_summary": "Unable to generate detailed analysis",
                        "news_summary": "AI analysis parsing failed",
                        "technical_analysis": "Analysis format error",
                        "investment_recommendation": "Please try again",
                        "risk_factors": "Analysis could not be processed",
                        "sentiment_score": 0.5
                    }
            except Exception as e:
                logger.error(f"Error with Gemini API: {str(e)}")
                analysis = {
                    "price_summary": f"Stock {stock_symbol} has moved {price_data['price_change']}% over the past year.",
                    "news_summary": "AI analysis temporarily unavailable",
                    "technical_analysis": f"Price range: ${price_data['low']} - ${price_data['high']}",
                    "investment_recommendation": "Service temporarily unavailable",
                    "risk_factors": "Unable to analyze risks at the moment",
                    "sentiment_score": 0.5
                }
        print(analysis['technical_analysis'])
        return JsonResponse({
            'status': 'success',
            'analysis': analysis,
            'price_data': price_data,
            'news_data': news_data
        })

    except Exception as e:
        logger.error(f"Error in analyze_stock: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f"Error analyzing stock: {str(e)}",
            'price_data': None,
            'news_data': None
        }, status=500)