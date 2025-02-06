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
    GSHEETS_CREDENTIALS = 'market-sensing-449014-056e2e3d0207.json'
    client = gspread.service_account(GSHEETS_CREDENTIALS)
    sheet = client.open('Dashboard_Marketsensing')
    
    worksheet_list = sheet.worksheets()
    pg1 = sheet.worksheet("Treasury Rates")
    df_pg = pd.DataFrame(pg1.get_all_records())
    df_pg = ensure_datetime(df_pg, 'Date')
    df_pg.set_index('Date', inplace=True)
    df_pg.fillna(method='ffill',inplace=True)
    
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

#st.write('히트맵 만들기 (Update)')

df_selection = df_selection[['DGS1','DGS3','DGS10','DGS30']]

weekly_yield = df_selection.resample('W').last()

# Plot Weekly Yield Rates with Plotly
#st.write("### Yield Curve Weekly Data")
fig = go.Figure()
for column in weekly_yield.columns:
    fig.add_trace(go.Scatter(x=weekly_yield.index, y=weekly_yield[column], mode='lines+markers', name=column))
    
fig.update_layout(
    title="미국 국채 수익률 (1년, 3년, 10년, 30년)",
    xaxis_title="Date",
    yaxis_title="Yield Rate",
    legend_title="Maturities",
    height = 600
)

st.plotly_chart(fig)

data = {
    "국가명": ["미국", "한국", "중국", "일본", "독일", "영국"],
    "1년": [0.0416, 0.0265, 0.0124, 0.0058, 0.0211, 0.0441],
    "2년": [0.0421, 0.0264, 0.0125, 0.0072, 0.0211, 0.0421],
    "5년": [0.0433, 0.0270, 0.0141, 0.0091, 0.0224, 0.0422],
    "10년": [0.0454, 0.0286, 0.0164, 0.0124, 0.0246, 0.0453],
    "30년": [0.0479, 0.0275, 0.0184, 0.0230, 0.0272, 0.0512]
}
yield_df = pd.DataFrame(data)
yield_df.set_index("국가명", inplace=True)

fig = go.Figure()
for country in yield_df.index:
    fig.add_trace(go.Scatter(x=yield_df.columns, y=yield_df.loc[country], mode='lines+markers', name=country))

fig.update_layout(
    title="글로벌 국채 금리",
    xaxis_title="Maturity",
    yaxis_title="Yield Rate",
    legend_title="Country"
)

st.plotly_chart(fig)
