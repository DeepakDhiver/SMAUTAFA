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

tokenizer = AutoTokenizer.from_pretrained("ipuneetrathore/bert-base-cased-finetuned-finBERT")
finbert = AutoModelForSequenceClassification.from_pretrained("ipuneetrathore/bert-base-cased-finetuned-finBERT")


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

            if link.get('href') == current_link:
                current_news.append((headline, sentiment))
            else:
                if current_link is not None and len(current_news) > 0:
                    filtered_news.append((current_link, current_news))
                current_link = link.get('href')
                current_news = [(headline, sentiment)]

    if current_link is not None and len(current_news) > 0:
        filtered_news.append((current_link, current_news))

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
from .utils import calculate_correlation, calculate_indicators, calculate_pivot_points


company_mapping = {
    'NIFTY 200': '^CNX200.NS',
    'BAJFINANCE': 'BAJFINANCE.NS',
    'TTML': 'TTML.NS',
    'BAJAJFINSV': 'BAJAJFINSV.NS',
    'PNB': 'PNB.NS',
    'YESBANK': 'YESBANK.NS',
    'BANKINDIA': 'BANKINDIA.NS',
    'FEDERALBNK': 'FEDERALBNK.NS',
    'INDIANB': 'INDIANB.NS',
    'BAJAJHLDNG': 'BAJAJHLDNG.NS',
    'HEROMOTOCO': 'HEROMOTOCO.NS',
    'BANKBARODA': 'BANKBARODA.NS',
    'CHOLAFIN': 'CHOLAFIN.NS',
    'JSWENERGY': 'JSWENERGY.NS',
    'OIL': 'OIL.NS',
    'POLICYBZR': 'POLICYBZR.NS',
    'TITAN': 'TITAN.NS',
    'TATACHEM': 'TATACHEM.NS',
    'UNIONBANK': 'UNIONBANK.NS',
    'ADANIPORTS': 'ADANIPORTS.NS',
    'HONAUT': 'HONAUT.NS',
    'CANBK': 'CANBK.NS',
    'SBIN': 'SBIN.NS',
    'NAUKRI': 'NAUKRI.NS',
    'POONAWALLA': 'POONAWALLA.NS',
    'UBL': 'UBL.NS',
    'BAJAJ-AUTO': 'BAJAJ-AUTO.NS',
    'AWL': 'AWL.NS',
    'PFC': 'PFC.NS',
    'BOSCHLTD': 'BOSCHLTD.NS',
    'HDFCAMC': 'HDFCAMC.NS',
    'CROMPTON': 'CROMPTON.NS',
    'M&M': 'M&M.NS',
    'ADANIENT': 'ADANIENT.NS',
    'PGHH': 'PGHH.NS',
    'LTTS': 'LTTS.NS',
    'SUNTV': 'SUNTV.NS',
    'IRFC': 'IRFC.NS',
    'DMART': 'DMART.NS',
    'ZEEL': 'ZEEL.NS',
    'JINDALSTEL': 'JINDALSTEL.NS',
    'CONCOR': 'CONCOR.NS',
    'LUPIN': 'LUPIN.NS',
    'LT': 'LT.NS',
    'TATAMOTORS': 'TATAMOTORS.NS',
    'WIPRO': 'WIPRO.NS',
    'SBICARD': 'SBICARD.NS',
    'UPL': 'UPL.NS',
    'SAIL': 'SAIL.NS',
    'AUROPHARMA': 'AUROPHARMA.NS',
    'DRREDDY': 'DRREDDY.NS',
    'DIXON': 'DIXON.NS',
    'MSUMI': 'MSUMI.NS',
    'TRENT': 'TRENT.NS',
    'DLF': 'DLF.NS',
    'TECHM': 'TECHM.NS',
    'TCS': 'TCS.NS',
    'HINDZINC': 'HINDZINC.NS',
    'HDFCBANK': 'HDFCBANK.NS',
    'ADANIGREEN': 'ADANIGREEN.NS',
    'APOLLOTYRE': 'APOLLOTYRE.NS',
    'CUMMINSIND': 'CUMMINSIND.NS',
    'ALKEM': 'ALKEM.NS',
    'TORNTPOWER': 'TORNTPOWER.NS',
    'IPCALAB': 'IPCALAB.NS',
    'ADANIPOWER': 'ADANIPOWER.NS',
    'HDFC': 'HDFC.NS',
    'DELHIVERY': 'DELHIVERY.NS',
    'FLUOROCHEM': 'FLUOROCHEM.NS',
    'BATAINDIA': 'BATAINDIA.NS',
    'COFORGE': 'COFORGE.NS',
    'NAVINFLUOR': 'NAVINFLUOR.NS',
    'DEVYANI': 'DEVYANI.NS',
    'PAYTM': 'PAYTM.NS',
    'PETRONET': 'PETRONET.NS',
    'PIDILITIND': 'PIDILITIND.NS',
    'TVSMOTOR': 'TVSMOTOR.NS',
    'IRCTC': 'IRCTC.NS',
    'PAGEIND': 'PAGEIND.NS',
    'BALKRISIND': 'BALKRISIND.NS',
    'ABBOTINDIA': 'ABBOTINDIA.NS',
    'PIIND': 'PIIND.NS',
    'NESTLEIND': 'NESTLEIND.NS',
    'PRESTIGE': 'PRESTIGE.NS',
    'MUTHOOTFIN': 'MUTHOOTFIN.NS',
    'ABB': 'ABB.NS',
    'FORTIS': 'FORTIS.NS',
    'SUNPHARMA': 'SUNPHARMA.NS',
    'NHPC': 'NHPC.NS',
    'MPHASIS': 'MPHASIS.NS',
    'DEEPAKNTR': 'DEEPAKNTR.NS',
    'ABFRL': 'ABFRL.NS',
    'JSWSTEEL': 'JSWSTEEL.NS',
    'DALBHARAT': 'DALBHARAT.NS',
    'TATAPOWER': 'TATAPOWER.NS',
    'ICICIBANK': 'ICICIBANK.NS',
    'VEDL': 'VEDL.NS',
    'SRF': 'SRF.NS',
    'POLYCAB': 'POLYCAB.NS',
    'CIPLA': 'CIPLA.NS',
    'JUBLFOOD': 'JUBLFOOD.NS',
    'IOC': 'IOC.NS',
    'HCLTECH': 'HCLTECH.NS',
    'BPCL': 'BPCL.NS',
    'COALINDIA': 'COALINDIA.NS',
    'AUBANK': 'AUBANK.NS',
    'ADANITRANS': 'ADANITRANS.NS',
    'INFY': 'INFY.NS',
    'OBEROIRLTY': 'OBEROIRLTY.NS',
    'GAIL': 'GAIL.NS',
    'BERGEPAINT': 'BERGEPAINT.NS',
    'APOLLOHOSP': 'APOLLOHOSP.NS',
    'BHEL': 'BHEL.NS',
    'HINDALCO': 'HINDALCO.NS',
    'POWERGRID': 'POWERGRID.NS',
    'BANDHANBNK': 'BANDHANBNK.NS',
    'TIINDIA': 'TIINDIA.NS',
    'TRIDENT': 'TRIDENT.NS',
    'LICI': 'LICI.NS',
    'COROMANDEL': 'COROMANDEL.NS',
    'SHRIRAMFIN': 'SHRIRAMFIN.NS',
    'KOTAKBANK': 'KOTAKBANK.NS',
    'MCDOWELL-N': 'MCDOWELL-N.NS',
    'INDUSINDBK': 'INDUSINDBK.NS',
    'HAL': 'HAL.NS',
    'NTPC': 'NTPC.NS',
    'HDFCLIFE': 'HDFCLIFE.NS',
    'RAMCOCEM': 'RAMCOCEM.NS',
    'SBILIFE': 'SBILIFE.NS',
    'MOTHERSON': 'MOTHERSON.NS',
    'NMDC': 'NMDC.NS',
    'MFSL': 'MFSL.NS',
    'RECLTD': 'RECLTD.NS',
    'VOLTAS': 'VOLTAS.NS',
    'ULTRACEMCO': 'ULTRACEMCO.NS',
    'SHREECEM': 'SHREECEM.NS',
    'ACC': 'ACC.NS',
    'MARUTI': 'MARUTI.NS',
    'GLAND': 'GLAND.NS',
    'COLPAL': 'COLPAL.NS',
    'ABCAPITAL': 'ABCAPITAL.NS',
    'LALPATHLAB': 'LALPATHLAB.NS',
    'AMBUJACEM': 'AMBUJACEM.NS',
    'SIEMENS': 'SIEMENS.NS',
    'GODREJCP': 'GODREJCP.NS',
    'TATACONSUM': 'TATACONSUM.NS',
    'ATGL': 'ATGL.NS',
    'ICICIGI': 'ICICIGI.NS',
    'INDHOTEL': 'INDHOTEL.NS',
    'TATACOMM': 'TATACOMM.NS',
    'M&MFIN': 'M&MFIN.NS',
    'TORNTPHARM': 'TORNTPHARM.NS',
    'PERSISTENT': 'PERSISTENT.NS',
    'CGPOWER': 'CGPOWER.NS',
    'MARICO': 'MARICO.NS',
    'OFSS': 'OFSS.NS',
    'TATASTEEL': 'TATASTEEL.NS',
    'ITC': 'ITC.NS',
    'LTIM': 'LTIM.NS',
    'ZYDUSLIFE': 'ZYDUSLIFE.NS',
    'TATAELXSI': 'TATAELXSI.NS',
    'BHARATFORG': 'BHARATFORG.NS',
    'DABUR': 'DABUR.NS',
    'ASTRAL': 'ASTRAL.NS',
    'ICICIPRULI': 'ICICIPRULI.NS',
    'NYKAA': 'NYKAA.NS',
    'BRITANNIA': 'BRITANNIA.NS',
    'MRF': 'MRF.NS',
    'HINDUNILVR': 'HINDUNILVR.NS',
    'BIOCON': 'BIOCON.NS',
    'DIVISLAB': 'DIVISLAB.NS',
    'SYNGENE': 'SYNGENE.NS',
    'ASIANPAINT': 'ASIANPAINT.NS',
    'SONACOMS': 'SONACOMS.NS',
    'IDEA': 'IDEA.NS',
    'AXISBANK': 'AXISBANK.NS',
    'IGL': 'IGL.NS',
    'BEL': 'BEL.NS',
    'INDIGO': 'INDIGO.NS',
    'GUJGASLTD': 'GUJGASLTD.NS',
    'WHIRLPOOL': 'WHIRLPOOL.NS',
    'ZOMATO': 'ZOMATO.NS',
    'PATANJALI': 'PATANJALI.NS',
    'ESCORTS': 'ESCORTS.NS',
    'HAVELLS': 'HAVELLS.NS',
    'HINDPETRO': 'HINDPETRO.NS',
    'MAXHEALTH': 'MAXHEALTH.NS',
    'INDUSTOWER': 'INDUSTOWER.NS',
    'ONGC': 'ONGC.NS',
    'GODREJPROP': 'GODREJPROP.NS',
    'VBL': 'VBL.NS',
    'LICHSGFIN': 'LICHSGFIN.NS',
    'RELIANCE': 'RELIANCE.NS',
    'GRASIM': 'GRASIM.NS',
    'LAURUSLABS': 'LAURUSLABS.NS',
    'PEL': 'PEL.NS',
    'BHARTIARTL': 'BHARTIARTL.NS',
    'ASHOKLEY': 'ASHOKLEY.NS',
    'L&TFH': 'L&TFH.NS',
    'IDFCFIRSTB': 'IDFCFIRSTB.NS',
    'EICHERMOT': 'EICHERMOT.NS'
}

def dashboard(request):

    
    # Get the list of company names from the mapping
    company_names = list(company_mapping.keys())
    
    if request.method == 'POST':
        ticker = request.POST['ticker']
        interval = request.POST['interval']
        
        # Convert the selected company name to the corresponding ticker symbol
        ticker = company_mapping.get(ticker, '')
        
        # Calculate indicators
        indicators = calculate_indicators(ticker, interval)

        # Calculate pivot points
        pivot_values = calculate_pivot_points(ticker)

        context = {
            'indicators': indicators,
            'pivot_values': pivot_values,
            'ticker': ticker,
            'interval': interval,
            'company_names': company_names,  # Pass the company names to the template
        }
        return render(request, 'dashboard.html', context)
    
    context = {
        'company_names': company_names,  # Pass the company names to the template
    }

    indices = ["^NSEI", "^IXIC", "^GSPC", "^FTSE", "^FCHI",  "^STI", "^HSI"]
    correlation_matrix_jpeg = calculate_correlation(indices)

    # Pass the JPEG data to the template
    correlation_matrix_path = r'C:\Users\deepa\OneDrive\Desktop\Final Integration\SMAUTAFA\SMAUTAFA\static\images\correlation_matrix.jpg'
    context = {
        'correlation_matrix_path': correlation_matrix_path
    }
    return render(request, 'dashboard.html', context)




    
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
