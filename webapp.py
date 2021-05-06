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

#Open and display image on webapp





#Get Feature inout from users

def get_user_input():
    password = st.text_input('Password', '')
    exchange  = st.text_input('Exchange/City', 'hk')
    
    #store a dictionary into a variable
    user_data = {'Password'   : password,
                 'Exchange'  : exchange}
    
    #transform the data into a dataframe
    #features = user_data.values
    #features = list(features)
    return([password, exchange])
    
#Store the user inputs
user_input = get_user_input()

#Set a subheader and display user input
#st.subheader('User Input: ')
#st.write(user_input)

#Store model predictions in a variable
if user_input[0] == '112699':
    prediction = stocks.find(user_input[1],'find')
else:
    prediction = ['Incorrect Password']

stocks = joblib.load('src/stocks_etoro_xch.sav')

arr = []

if user_input[0] != '112699':
    st.markdown('Incorrect Password')

else :
    st.subheader('Prediction: ')
    stocks = joblib.load('src/stocks_etoro_xch.sav')
    if user_input[0] == '112699':
            load = stocks
            arr = []
            exchange = user_input[1]
            mode = 'find'
            if exchange.lower() == 'hk':
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
                
            for comp in load[i]:
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
                    
                    ind = anls.indicators
                    
                    val = ind['close']
                    ema20 = ind['EMA20']
                    ema50 = ind['EMA50']
                    ema100 = ind['EMA100']
                    rsi = ind['RSI']
                    if mode.lower() == 'find':
                        if (val < ema20) and ((val >= ema50)) and (ema50 > ema100) and (ema20 > ema50) :# and ((rsi <= 30) or (rsi>= 55)):#or(val > ema100)):
                        #if ((rsi <= 30) or (rsi>= 55)):
                            print(comp)
                            arr.append(comp)
                    else :
                        if (val > ema20) :
                            os.system('say ' + comp)
                            st.write(comp)
                            arr.append(comp)
                except:
                    continue



#Set a subheader and display prediction
for i in arr:
    st.write(i)



#"/Users/suriyaprakashjambunathan/WebApp.py"
    


import sys
from streamlit import cli as stcli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "webapp.py"]
    sys.exit(stcli.main())
