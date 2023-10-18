import csv
import datetime
from difflib import diff_bytes
import os
from datetime import date

import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
from core.models import Stock, StockData
from dateutil import parser
import requests
from fuzzywuzzy import process

today = date.today()

two_years = datetime.datetime.now() - datetime.timedelta(days=731) 


def csv2json(stock):
    stock_ticker = yf.Ticker(stock)
    company_name = stock_ticker.info['longName']

    if(os.path.exists("algo/"+ stock + ".csv")): 
        latest_data = pd.read_csv("algo/"+stock + ".csv").iloc[-1]        
        latest_date = str(latest_data['Date'][:11])       
        l_date = date(int(latest_date[:4]), int(
            latest_date[5:7]), int(latest_date[9:11]))
        dates_diff = date.today()-l_date 
        if(str(dates_diff)=='0:00:00'):
            pass        
        else:
            if(int(str(dates_diff).split(" ")[0]) > 1):
                df = yf.download(stock, start=two_years, end=datetime.datetime.now())
                df.to_csv("algo/"+stock + ".csv")         
    else:
        df = yf.download(stock, start=two_years, end=datetime.datetime.now())
        df.to_csv("algo/"+stock + ".csv")
    
    latest_data = pd.read_csv("algo/"+ stock + ".csv")
    last_row = pd.read_csv("algo/"+stock + ".csv").iloc[-1]
    #print(last_row) 
    #a= Stock.objects.get(stock=stock)
    if Stock.objects.filter(stock=stock).exists():
        Stock.objects.filter(stock=stock).update(market_cap = last_row['Close'], last_update=last_row['Date'])
    else:
         Stock.objects.create(stock=stock,name=company_name, market_cap = last_row['Close'], last_update=last_row['Date'])           
    # a.market_cap = last_row['Close']       
    # a.last_update=last_row['Date']
    dates = []
    prices = []
    a = pd.DataFrame(latest_data['Date']).to_dict('records')
    b = pd.DataFrame(latest_data['Close']).to_dict('records')
    for i in range(len(a)):            
        dates.append(a[i]['Date'])
    for i in range(len(b)):
        prices.append(b[i]['Close'])
    StockData.objects.create(stock=stock, dates=dates, prices=prices)  
    return None

