#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 06:21:54 2021

@author: suriyaprakashjambunathan
"""

#Description
import pandas as pd
from PIL import Image
import streamlit as st
import numpy as np
from itertools import compress
import sys
sys.path.append('src/')
from tradingview_ta import TA_Handler, Interval, Exchange
import joblib 




import pyutilib.subprocess.GlobalData

import ptvsd
#ptvsd.enable_attach(address=('localhost', 8501))

#Title and sub-title
#st.set_page_config(page_title='Stock Screen', page_icon = image, layout = 'wide', initial_sidebar_state = 'auto')
st.write("""
# STOCK SCREEN
""")


#function


import requests, json, datetime, warnings
#from .technicals import Compute
import joblib

__version__ = "3.2.3"

class Analysis(object):
    exchange = ""
    symbol = ""
    screener = ""
    time = ""
    interval = ""
    summary = {}
    oscillators = {}
    moving_averages = {}
    indicators = {}

class Interval:
    INTERVAL_1_MINUTE = "1m"
    INTERVAL_5_MINUTES = "5m"
    INTERVAL_15_MINUTES = "15m"
    INTERVAL_1_HOUR = "1h"
    INTERVAL_4_HOURS = "4h"
    INTERVAL_1_DAY = "1d"
    INTERVAL_1_WEEK = "1W"
    INTERVAL_1_MONTH = "1M"

class Exchange:
    FOREX = "FX_IDC"
    CFD = "TVC"


class TradingView:
    scan_url = "https://scanner.tradingview.com/"
    indicators = ["Recommend.Other{}","Recommend.All{}","Recommend.MA{}","RSI{}","RSI[1]{}","Stoch.K{}","Stoch.D{}","Stoch.K[1]{}","Stoch.D[1]{}","CCI20{}","CCI20[1]{}","ADX{}","ADX+DI{}","ADX-DI{}","ADX+DI[1]{}","ADX-DI[1]{}","AO{}","AO[1]{}","Mom{}","Mom[1]{}","MACD.macd{}","MACD.signal{}","Rec.Stoch.RSI{}","Stoch.RSI.K{}","Rec.WR{}","W.R{}","Rec.BBPower{}","BBPower{}","Rec.UO{}","UO{}","close{}","EMA5{}","SMA5{}","EMA10{}","SMA10{}","EMA20{}","SMA20{}","EMA30{}","SMA30{}","EMA50{}","SMA50{}","EMA100{}","SMA100{}","EMA200{}","SMA200{}","Rec.Ichimoku{}","Ichimoku.BLine{}","Ichimoku.CLine{}","Rec.VWMA{}","VWMA{}","Rec.HullMA9{}","HullMA9{}","Pivot.M.Classic.S3{}","Pivot.M.Classic.S2{}","Pivot.M.Classic.S1{}","Pivot.M.Classic.Middle{}","Pivot.M.Classic.R1{}","Pivot.M.Classic.R2{}","Pivot.M.Classic.R3{}","Pivot.M.Fibonacci.S3{}","Pivot.M.Fibonacci.S2{}","Pivot.M.Fibonacci.S1{}","Pivot.M.Fibonacci.Middle{}","Pivot.M.Fibonacci.R1{}","Pivot.M.Fibonacci.R2{}","Pivot.M.Fibonacci.R3{}","Pivot.M.Camarilla.S3{}","Pivot.M.Camarilla.S2{}","Pivot.M.Camarilla.S1{}","Pivot.M.Camarilla.Middle{}","Pivot.M.Camarilla.R1{}","Pivot.M.Camarilla.R2{}","Pivot.M.Camarilla.R3{}","Pivot.M.Woodie.S3{}","Pivot.M.Woodie.S2{}","Pivot.M.Woodie.S1{}","Pivot.M.Woodie.Middle{}","Pivot.M.Woodie.R1{}","Pivot.M.Woodie.R2{}","Pivot.M.Woodie.R3{}","Pivot.M.Demark.S1{}","Pivot.M.Demark.Middle{}","Pivot.M.Demark.R1{}", "open{}", "P.SAR{}", "BB.lower{}", "BB.upper{}"]
    def data(symbol, interval):
        """Format TradingView's Scanner Post Data
        Args:
            symbol (string): EXCHANGE:SYMBOL (ex: NASDAQ:AAPL or BINANCE:BTCUSDT)
            interval (string): Time Interval (ex: 1m, 5m, 15m, 1h, 4h, 1d, 1W, 1M)
        Returns:
            string: JSON object as a string.
        """
        if interval == "1m":
            # 1 Minute
            data_interval = "|1"
        elif interval == "5m":
            # 5 Minutes
            data_interval = "|5"
        elif interval == "15m":
            # 15 Minutes
            data_interval = "|15"
        elif interval == "1h":
            # 1 Hour
            data_interval = "|60"
        elif interval == "4h":
            # 4 Hour
            data_interval = "|240"
        elif interval == "1W":
            # 1 Week
            data_interval = "|1W"
        elif interval == "1M":
            # 1 Month
            data_interval = "|1M"
        else:
            if interval != '1d':
                warnings.warn("Interval is empty or not valid, defaulting to 1 day.")
            # Default, 1 Day
            data_interval = ""
            
        data_json = {"symbols":{"tickers":[symbol.upper()],"query":{"types":[]}},"columns":[x.format(data_interval) for x in TradingView.indicators]}

        return data_json

class TA_Handler(object):
    screener = ""
    exchange = ""
    symbol = ""
    interval = ""
    timeout = None

    def __init__(self, screener="", exchange="", symbol="", interval="", timeout=None):
        """Create an instance of TA_Handler class
        Args:
            screener (str, required): Screener (see documentation and tradingview's site).
            exchange (str, required): Exchange (see documentation and tradingview's site).
            symbol (str, required): Abbreviation of a stock or currency (see documentation and tradingview's site).
            interval (str, optional): See the interval class and the documentation. Defaults to 1 day.
            timeout (float, optional): Timeout for requests (in seconds). Defaults to None.
        """
        self.screener = screener
        self.exchange = exchange
        self.symbol = symbol
        self.interval = interval
        self.timeout = timeout

    #Set functions
    def set_screener_as_stock(self, country):
        """Set the screener as a country (for stocks). 
        Args:
            country (string): Stock's country (ex: If NFLX or AAPL, then "america" is the screener)
        """
        self.screener = country

    def set_screener_as_crypto(self):
        """Set the screener as crypto (for cryptocurrencies).
        """
        self.screener = "crypto"

    def set_screener_as_cfd(self):
        """Set the screener as cfd (contract for differences).
        """
        self.screener = "cfd"

    def set_screener_as_forex(self):
        """Set the screener as forex.
        """
        self.screener = "forex"

    def set_exchange_as_crypto_or_stock(self, exchange):
        """Set the exchange
        Args:
            exchange (string): Stock/Crypto's exchange (NASDAQ, NYSE, BINANCE, BITTREX, etc).
        """
        self.exchange = exchange

    def set_exchange_as_forex(self):
        """Set the exchange as FX_IDC for forex.
        """
        self.exchange = "FX_IDC"
    
    def set_exchange_as_cfd(self):
        """Set the exchange as TVC for cfd.
        """
        self.exchange = "TVC"

    def set_interval_as(self, intvl):
        """Set the interval.
        Refer to: https://python-tradingview-ta.readthedocs.io/en/latest/usage.html#setting-the-interval
        Args:
            intvl (string): interval. You can use values from the Interval class. 
        """
        self.interval = intvl

    def set_symbol_as(self, symbol):
        """Set the symbol.
        Refer to: https://python-tradingview-ta.readthedocs.io/en/latest/usage.html#setting-the-symbol
        Args:
            symbol (string): abbreviation of a stock or currency (ex: NFLX, AAPL, BTCUSD).
        """
        self.symbol = symbol
        

    #Get analysis
    def get_analysis(self):
        """Get analysis from TradingView and compute it.
        Returns:
            Analysis: Contains information about the analysis.
        """
        if self.screener == "" or type(self.screener) != str:
            raise Exception("Screener is empty or not valid.")
        elif self.exchange == "" or type(self.exchange) != str:
            raise Exception("Exchange is empty or not valid.")
        elif self.symbol == "" or type(self.symbol) != str:
            raise Exception("Symbol is empty or not valid.")

        exch_smbl = self.exchange.upper() + ":" + self.symbol.upper()
        data = TradingView.data(exch_smbl, self.interval)
        scan_url = TradingView.scan_url + self.screener.lower() + "/scan"
        headers = {"User-Agent": "tradingview_ta/{}".format(__version__)}
        response = requests.post(scan_url,json=data, headers=headers, timeout=self.timeout)

        # Return False if can't get data
        if response.status_code != 200:
            raise Exception("Can't access TradingView's API. HTTP status code: {}.".format(response.status_code))
        
        result = json.loads(response.text)["data"]
        if result != []:
            indicator_values = result[0]["d"]
        else:
            raise Exception("Exchange or symbol not found.")
        
        return(indicator_values)
        
stocks = joblib.load('src/stocks_etoro_xch.sav')


    
def stocks_find(exchange, ind, gel, data = None):
    #load = joblib.load('stocks_etoro_xch.sav')
    load = stocks
            
    arr = []
    if exchange.lower() == 'hk' or exchange.lower() == 'hong kong':
        i = 1
        xch1 = "HKEX"
        xch2 = "HK"
        scr  = "hongkong"
    elif exchange.lower() == 'london':
        i = 2
        xch1 = "LSE"
        xch2 = "LSIN"
        scr  = "UK"
    elif exchange.lower() == 'nasdaq':
        i = 3
        xch1 = "NASDAQ"
        xch2 = "NASDAQ"
        scr  = "america"
    elif exchange.lower() == 'nyse':
        i = 4
        xch1 = "LSE"
        xch2 = "LSIN"
        scr  = "UK"
    elif exchange.lower() == 'paris':
        i = 5
        xch1 = "EURONEXT"
        xch2 = "EURONEXT"
        scr  = "France"
        
    elif exchange.lower() == 'crypto':
        i = 6
        xch1 = "binance"
        xch2 = "bitstamp"
        scr  = "crypto"
        
    if data is not None:
        load = [[0]]*7
        load[i] = data
        
    for comp in load[i]:
        if i == 6:
            comp = comp + 'USD'
        try:
            handler = TA_Handler()
            handler.set_symbol_as(comp)
            try:
                handler.set_exchange_as_crypto_or_stock(xch1)
            except:
                handler.set_exchange_as_crypto_or_stock(xch2)
            handler.set_screener_as_stock(scr)
            handler.set_interval_as(Interval.INTERVAL_5_MINUTES)
            
            anls = handler.get_analysis()
            
            Blue_line = anls[47]
            Red_line  = anls[46]
            
            val    = anls[30]
            ema20  = anls[35]
            ema50  = anls[39]
            ema100 = anls[41]
            valo   = anls[83]
            
            if val > valo:
            
                if 'ichi' in ind.lower():
                    if (gel == '=') or (gel == 'eq'):
                        if Blue_line == Red_line :
                            print(comp)
                            arr.append(comp)
                    elif (gel == '>') or ('g' in gel):
                        if Blue_line > Red_line :
                            print(comp)
                            arr.append(comp)
                    elif (gel == '<') or ('l' in gel):
                        if Blue_line < Red_line :
                            print(comp)
                            arr.append(comp)
                            
                elif 'ema' in  ind.lower():
                    if (gel == '=') or ('b' in gel):
                        if (val < ema20) and (val > ema50) and ( ema50 > ema100) and (ema20 > ema50) :
                            print(comp)
                            arr.append(comp)
                    elif (gel == '>') or ('g' in gel):
                        if (val > ema20) and (ema20 > ema50) and (ema50 > ema100) :
                            print(comp)
                            arr.append(comp)
                    elif (gel == '<') or ('l' in gel):
                        if (val < ema100) :
                            print(comp)
                            arr.append(comp)
            
        except:
            continue
    return (arr)


#Get Feature inout from users

def get_user_password():
    password = st.text_input('Password', '')
    
    #transform the data into a dataframe
    #features = user_data.values
    #features = list(features)
    return(password)
    
drop_downs = [['','NASDAQ', 'NYSE', 'Crypto', 'London', 'Paris', 'Hong Kong'],
                  ['','Ichimoku', 'EMA'],
                  ['','<', '=', '>'],
                  ['','Find', 'Screen']]

def get_user_input():
    d_d = drop_downs
    run = st.checkbox('Run')
    exchange  = st.selectbox("Exchange/City: ",d_d[0])
    ind       = st.selectbox("Indicator: ",d_d[1])
    gel       = st.selectbox("</=/>: ",d_d[2])
    mode      = st.selectbox("Mode: ",d_d[3])
    
    #transform the data into a dataframe
    #features = user_data.values
    #features = list(features)
    return([exchange, ind, gel, mode, run])
    
#Store the user inputs
pw = get_user_password()
user_input = get_user_input()


if pw == '112699':
    
    #Set a subheader and display user input
    #st.subheader('User Input: ')
    #st.write(user_input)
    #user_input = ['112699','NASDAQ']
    
    #Store model predictions in a variable
    if user_input[4]:
        arr = []

        st.subheader('Prediction: ')
        load = stocks
        arr = []
        exchange  = user_input[0]
        indicator = user_input[1]
        gel       = user_input[2]
        mode      = user_input[3]

        if mode.lower() == 'find' :
            arr = stocks_find(exchange, indicator, gel)
            if len(arr) == 0:
                arr = ['No stock/crypto in the range']
        elif mode.lower() == 'screen':
            arr = stocks_find(exchange, indicator, '=')
            if len(arr) > 0:
                while True:
                    #print('\n')
                    arr_ = stocks_find(exchange,indicator, gel, arr)
                    if len(arr_) > 0:
                        break
                arr = arr_
            else:
                arr = ['No stock/crypto in the range']

        if exchange.lower() == 'nasdaq' or exchange.lower() == 'nyse' or exchange.lower() == 'crypto':
            suffix = ''
        elif exchange.lower() == 'london':
            suffix = '.l'
        elif exchange.lower() == 'paris':
            suffix = '.pa'
        elif exchange.lower() == 'hk' or exchange.lower() == 'hong kong':
            suffix = '.hk'

        #Set a subheader and display prediction
        for i in arr:
            if i == 'No stock/crypto in the range':
                st.write(i)
            else:
                if exchange.lower() == 'crypto':
                    i = i[:-3]
                link = '['+ i + ']' + '(https://www.etoro.com/markets/' + i + suffix + '/chart)'
                st.markdown(link, unsafe_allow_html=True)
                    

else :
    st.write('Incorrect Password')

    

import sys
from streamlit import cli as stcli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "webapp.py"]
    sys.exit(stcli.main())
