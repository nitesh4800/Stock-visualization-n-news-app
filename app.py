import streamlit as st
import pandas as pd 
import numpy as np 
import yfinance as yf 
import plotly.express as px
import datetime 

st.title(':chart_with_upwards_trend: Stocks Dashboard')
ticker=st.sidebar.selectbox('Ticker',('MSFT','AAPL','TSLA','AMZN','BAC','GOOGL','PYPL','INTC','NVDA','AMD','BABA'))
start_date=st.sidebar.date_input('Start Date',value=datetime.date(2020, 1, 1))
end_date=st.sidebar.date_input('End Date')
data=yf.download(ticker,start=start_date,end=end_date)
fig=px.line(data,x=data.index,y=data['Adj Close'],title=ticker)
st.plotly_chart(fig)
pricing_data, news=st.tabs(["Pricing Data"," Top 10 News"])


with pricing_data:
    st.header("Price Movements")
    data2=data
    data2["% Change"]=data["Adj Close"]/data["Adj Close"].shift(1) -1
    st.write(data2)
    annual_return=data2['% Change'].mean()*252*100
    st.write("Annual Return is ", annual_return,'%')
    stdev=np.std(data2['% Change'])*np.sqrt(252)
    st.write("Standard Deviation is ",stdev*100,'%')

from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn=StockNews(ticker,save_news=False)
    df_news=sn.read_rss()
    for i in range(10):
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment=df_news['sentiment_title'][i]
        st.write(f'Title Sentiment : {title_sentiment}')
        news_sentiment=df_news['sentiment_summary'][i]
        st.write(f'News Sentiment : {news_sentiment}')
        st.write('----')
    
    