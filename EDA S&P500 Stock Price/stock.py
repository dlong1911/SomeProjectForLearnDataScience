from itertools import groupby
from symtable import Symbol
from turtle import color
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

st.title('S&P S500 app')

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, matplotlib, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')

@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df=html[0]
    return df

df=load_data()
# # df
# tf = pd.DataFrame(data['ABT'].Close)
# tf
# sector_unique = df['GICS Sector'].unique()
# sector_unique
# tf=df['Symbol']
# tf
sector = df.groupby('GICS Sector')

sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' row and ' + str(df_selected_sector.shape[1]) + ' column.'   )
st.dataframe(df_selected_sector)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

data = yf.download(
    tickers = list(df_selected_sector[0:5].Symbol),
    period = "ytd",
    interval = "1d",
    group_by = 'ticker',
    auto_adjust = True,
    prepost = True,
    threads = True,
    proxy = None
)

# tf = pd.DataFrame(data['ABT'].Close)
# tf

def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Close, color = 'skyblue', alpha = 0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation = 90)
    plt.title(symbol, fontweight = 'bold')
    plt.xlabel('Date', fontweight = 'bold')
    plt.ylabel('Closing Price', fontweight = 'bold')
    return st.pyplot()

num_company = st.sidebar.slider('Number of Companies',1,5)
st.set_option('deprecation.showPyplotGlobalUse', False)
if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)