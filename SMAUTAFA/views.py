from django.shortcuts import render
from bs4 import BeautifulSoup as BS
import requests as req
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
from .models import *
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from tabulate import tabulate
import ta
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns

tokenizer = AutoTokenizer.from_pretrained("ipuneetrathore/bert-base-cased-finetuned-finBERT")
finbert = AutoModelForSequenceClassification.from_pretrained("ipuneetrathore/bert-base-cased-finetuned-finBERT")


def get_sentiment_label(sentiment_score):
    if sentiment_score == 0:
        return "Negative"
    elif sentiment_score == 1:
        return "Neutral"
    elif sentiment_score == 2:
        return "Positive"
    else:
        return "Unknown"

def get_filtered_news_from_url(url, company_name):
    webpage = req.get(url)
    trav = BS(webpage.content, "html.parser")

    filtered_news = []
    current_link = None
    current_news = []
    for link in trav.find_all('a'):
        if link.string and len(link.string) > 35 and company_name.lower() in link.string.lower():
            headline = link.string
            encoded_inputs = tokenizer.encode_plus(headline, return_tensors="pt", padding=True)
            outputs = finbert(**encoded_inputs)[0]
            sentiment = np.argmax(outputs.detach().numpy())

            # Convert sentiment score to label
            sentiment_label = get_sentiment_label(sentiment)

            if link.get('href') == current_link:
                current_news.append((headline, sentiment_label))
            else:
                if current_link is not None and len(current_news) > 0:
                    filtered_news.append((current_link, current_news))
                current_link = link.get('href')
                current_news = [(headline, sentiment_label)]

    return filtered_news

def get_filtered_news(company_name):
    urls = [
        "https://www.businesstoday.in/latest/economy",
        "https://www.moneycontrol.com/news/business/",
        "https://www.ndtv.com/business/latest",
        "https://www.investing.com/news/stock-market-news",
        "https://www.livemint.com/news",
        "https://www.livemint.com/market",
        "https://www.cnbctv18.com/news/",
        "https://www.cnbctv18.com/market/",
        "https://www.ndtv.com/topic/stock-talk",
        "https://www.moneycontrol.com/markets/fno-market-snapshot",
        "https://pulse.zerodha.com/"
    ]

    filtered_news = []
    for url in urls:
        filtered_news.extend(get_filtered_news_from_url(url, company_name))

    # Filter out the headlines that are not related to the company name.
    filtered_news = [
        (link, news)
        for link, news in filtered_news
        if any(company_name in headline for headline, _ in news)
    ]

    # Sort the headlines based on sentiment polarity.
    filtered_news.sort(key=lambda news: news[1][0][1], reverse=True)

    # Limit the number of headlines to 10.
    filtered_news = filtered_news[:10]

    return filtered_news

def news_sentiment(request):
    if request.method == "POST":
        name = request.POST.get('stock')
        news = get_filtered_news(name)

        if news:
            return render(request, "news_sentiment.html", {'data': news, 'name': name})
        else:
            print(f"No news found related to {name}.")

    return render(request, "news_sentiment.html")



from django.shortcuts import render
from .utils import  calculate_indicators, calculate_pivot_points



def dashboard(request):
    if request.method == 'POST':
        selected_company_name = request.POST.get('ticker')
        interval = request.POST.get('interval')
        
        # Check if a company name is selected
        if selected_company_name:
            # Calculate indicators
            indicators = calculate_indicators(selected_company_name, interval)

            # Calculate pivot points
            pivot_values = calculate_pivot_points(selected_company_name)

            context = {
                'indicators': indicators,
                'pivot_values': pivot_values,
                'ticker': selected_company_name,
                'interval': interval,
            }
            return render(request, 'dashboard.html', context)
    return render(request, 'dashboard.html')




    
def fundamentals(request):
    return render(request, 'fundamentals.html')
def global_page(request):
    return render(request, 'global.html')
def home(request):
    return render(request, 'home.html')
def charts(request):
    return render(request, 'charts.html')
def technicals(request):
    return render(request, 'technicals.html')