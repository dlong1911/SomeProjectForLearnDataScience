import streamlit as st
import yfinance as yf
import pandas as pd


st.write("""
# Simple Stock Price App

Shown are the stock **Closing price** and ***volume*** of Apple!



"""

)


tickerSymbol = 'AAPL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period ='1d', start='2021-5-31', end='2022-5-31')
st.write("""
# Closing price""")
st.line_chart(tickerDf.Close)
st.write("""
# Volume""")
st.line_chart(tickerDf.Volume)

