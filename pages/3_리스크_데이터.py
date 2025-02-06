import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import gspread
from utils.utils import *
import plotly.express as pe
import plotly.graph_objects as go

@st.cache_data
def get_and_prepare_data():
    # Connect to GS
    GSHEETS_CREDENTIALS = 'market-sensing-449014-a6c257ded130.json'
    client = gspread.service_account(GSHEETS_CREDENTIALS)
    sheet = client.open('Dashboard_Marketsensing')
    
    worksheet_list = sheet.worksheets()
    pg = sheet.worksheet("Bloomberg")
    df_pg = pd.DataFrame(pg.get_all_records())
    df_pg = ensure_datetime(df_pg, 'Date')
    df_pg.set_index('Date', inplace=True)
    df_pg = df_pg.replace(r'^\s*$', np.nan, regex=True)
    df_pg = df_pg.ffill()
    df_pg = df_pg.bfill()
    
    return df_pg

df = get_and_prepare_data()

df = df.apply(pd.to_numeric, errors='coerce')
start_date = st.sidebar.date_input("시작 시점: ", value='2024-01-03')
end_date = st.sidebar.date_input("종료 시점: ", value="today")

idx = (df.index >= pd.to_datetime(start_date)) &\
        (df.index <= pd.to_datetime(end_date))

df_selection = df[idx]
df_selection = df_selection.replace(r'^\s*$', np.nan, regex=True)
df_selection = df_selection.fillna(method='ffill').fillna(method='bfill')
df_selection = df_selection[['CESIUSD Index']]
#st.write('히트맵 만들기 (Update)')

df_selection["20-Day MA"] =\
df_selection["CESIUSD Index"].rolling(window=20, min_periods=1).mean()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_selection.index, y=df_selection["CESIUSD Index"], mode='lines+markers', name="CESIUSD Index"))
fig.add_trace(go.Scatter(x=df_selection.index, y=df_selection["20-Day MA"], mode='lines', name="20-Day Moving Average"))

fig.update_layout(
    title="CESIUSD Index with 20-Day Moving Average",
    xaxis_title="Date",
    yaxis_title="Index Value",
    legend_title="Indicator",
    height = 600
)

st.plotly_chart(fig)









