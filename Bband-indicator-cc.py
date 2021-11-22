# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 18:50:05 2021

@author: ZhangQi
"""
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

st.set_page_config(page_title="投资分析-Bband indicator",page_icon="🧊",layout="wide")

df = pd.read_csv("china_concept.csv",encoding="GB2312")
tickers = list(df.Ticker2)
names = list(df.Name)

years = [2019,2020,2021]
months = list(range(1,13))
days = list(range(1,31))
periods = list(range(10,31))


ticker = st.sidebar.selectbox(
    '中概股股票代码：',
     tickers)   

year = st.sidebar.selectbox(
    '选择开始的年份：一般选择2021年',
     years)  

month = st.sidebar.selectbox(
    '选择开始的月份',
     months) 

day = st.sidebar.selectbox(
    '选择开始的日期',
     days) 

period = st.sidebar.selectbox(
    '选择多少天作为基准来计算区间--一般选择20天',
     periods) 

start = dt.datetime(year, month, day)
end = dt.datetime(2021, 11, 15)


stock = yf.Ticker(ticker)
info = stock.info

name = names[tickers.index(ticker)]

st.title(name)
#subheader() 
#st.markdown('** Sector **: ' + info['sector'])
st.markdown('** Industry **: ' + info['industry'])
st.markdown('** Phone **: ' + info['phone'])
st.markdown('** Address **: ' + info['address1'] + ', ' + info['city'] + ', ' + info['zip'] + ', '  +  info['country'])
st.markdown('** Website **: ' + info['website'])
st.markdown('** 当黑色线低于绿色线，代表价格过高，是买点；当黑色线高于蓝色线，代表价格过高，是卖点 ** ')




df= stock.history(ticker, start=start, end=end)

multiplier = 2
df['up_band'] = df['Close'].rolling(period).mean() + df['Close'].rolling(period).std() * multiplier
df['mid_band'] = df['Close'].rolling(period).mean()
df['low_band'] = df['Close'].rolling(period).mean() - df['Close'].rolling(period).std() * multiplier


df[['Close','up_band','mid_band','low_band']].plot(figsize= (12,10))
fig, ax = plt.subplots()
#fig = plt.figure(figsize=(12,4)) 
ax.plot(df.index, df['up_band'], linewidth=1.0, linestyle="-",label="上界线")
ax.plot(df.index, df['Close'], linewidth=1.2,color='black',label="收盘价")
ax.plot(df.index, df['mid_band'], linewidth=1.0, linestyle="-",label="中界线")
ax.plot(df.index, df['low_band'], linewidth=1.0, linestyle="-",label="下界线")
ax.fill_between(df.index, df['up_band'],df['low_band'],alpha=.2, linewidth=0)
#plt.axis('tight')
plt.tick_params(axis='x', labelsize=8,rotation=15) 
st.pyplot(fig)

hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)
