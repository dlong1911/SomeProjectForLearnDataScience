from turtle import position
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.title('NBA player Stats Explorer')

st.markdown("""
This app performs simple Webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Baseketball-reference.com](https://www.baseketball-reference.com/)
""")

st.sidebar.header('User Input Features')

selected_year = st.sidebar.selectbox('Year', list(reversed(range(1970,2022))))

@st.cache
def load_data(year):
    url = "https://www.baseketball-reference.com/nbl"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['RK'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team')
st.write('Data Demension:' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

def filedownload(df):
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)


