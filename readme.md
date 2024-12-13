# Financial Forecasting and Stock Analysis

## Project Description

This project is a comprehensive financial forecasting and stock analysis tool designed to help users make informed investment decisions. The application leverages various APIs and machine learning models to provide detailed analysis and forecasts for stocks and financial data.

### Features

1. **Stock Analysis Dashboard** :

* Fetches historical stock data using Yahoo Finance API.
* Provides a detailed analysis of stock performance over the past year.
* Displays key metrics such as starting price, current price, 52-week high/low, average daily volume, and price change percentage.

2. **News Integration** :

* Integrates with NewsAPI to fetch the latest news articles related to specific stocks.
* Displays recent news headlines and their publication dates.
* Analyzes news sentiment to provide insights into market sentiment.

3. **AI-Powered Analysis** :

* Utilizes Google Generative AI (Gemini) to generate detailed stock analysis reports.
* Provides insights into price performance, news sentiment, technical indicators, investment recommendations, and risk factors.
* Generates a sentiment score to gauge market sentiment.

4. **Financial Forecasting** :

* Generates revenue, expense, and profit forecasts based on historical data.
* Saves forecast data to the database for future reference.
* Provides a simplified confidence level for the forecasts.

5. **User-Friendly Interface** :

* Offers a clean and intuitive dashboard for easy navigation.
* Displays analysis and forecasts in a visually appealing format.
* Allows users to search for specific stocks and view detailed analysis.

### Technologies Used

* **Backend** : Django, Django REST Framework
* **Frontend** : HTML, CSS, JavaScript, Bootstrap
* **APIs** : Yahoo Finance API, NewsAPI, Google Generative AI (Gemini)
* **Database** : SQLite (can be configured to use other databases)
* **Machine Learning** : Google Generative AI for natural language processing and analysis

### Installation and Setup

1. **Clone the repository** :

   **git** **clone** **https://github.com/yourusername/financial_forecast**ing.git

   **cd** **financial_forecasting**
2. **Install dependencies** :

   **pip** **install** **-r** **requirements.txt**
3. **Configure API keys** :

   Replace placeholders in the code with your actual API keys for NewsAPI and Google Generative AI.
4. **Run database migrations** :

   **python** **manage.py** **migrate**
5. **Start the development server** :

   **python** **manage.py** **runserver**
6. **Access the application** :

* Open your web browser and navigate to `http://localhost:8000`.

### Usage

* Navigate to the stock analysis dashboard to view detailed analysis and forecasts for various stocks.
* Use the search functionality to find specific stocks and view their analysis.
* Check the latest news articles related to your stocks and analyze market sentiment.
* Generate financial forecasts and save them for future reference.
