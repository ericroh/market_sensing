import streamlit as st
import pandas as pd 
import numpy as np
import gspread
from utils.utils import *
import plotly.express as pe
import os

config = {'displayModeBar': False}

#st.title(f"글로벌 주요 지수", anchor=False)

GSHEETS_CREDENTIALS = {
    "type": str(st.secrets["type"]),
    "project_id": str(st.secrets["project_id"]),
    "private_key_id": str(st.secrets["private_key_id"]),
    "private_key": str(st.secrets["private_key"]),
    "client_email": str(st.secrets["client_email"]),
    "client_id": str(st.secrets["client_id"]),
    "auth_uri": str(st.secrets["auth_uri"]),
    "token_uri": str(st.secrets["token_uri"]),
    "auth_provider_x509_cert_url": str(st.secrets["auth_provider_x509_cert_url"]),
    "client_x509_cert_url": str(st.secrets["client_x509_cert_url"]),
}


@st.cache_data
def get_and_prepare_data():
    # Connect to GS
    client = gspread.service_account_from_dict(GSHEETS_CREDENTIALS)
    sheet = client.open('Dashboard_Marketsensing')
    
    worksheet_list = sheet.worksheets()
    pg1 = sheet.worksheet("Index")
    df_pg1 = pd.DataFrame(pg1.get_all_records())
    df_pg1 = ensure_datetime(df_pg1, 'Date')
    df_pg1.set_index('Date', inplace=True)
    df_pg1.fillna(method='ffill',inplace=True)
    
    return df_pg1

df = get_and_prepare_data()
df.columns = ['SP500','NASDAQ','RUSSELL','HSI','KOSPI','NIKKEI','VIX','DOLLAR']


start_date = st.sidebar.date_input("시작 시점: ", value='2024-01-03')
end_date = st.sidebar.date_input("종료 시점: ", value="today")


idx = (df.index >= pd.to_datetime(start_date)) &\
        (df.index <= pd.to_datetime(end_date))

df_selection = df[idx]
df_selection = df_selection.replace(r'^\s*$', np.nan, regex=True)
df_selection = df_selection.fillna(method='ffill').fillna(method='bfill')


st.write('글로벌 지수 한눈에 보기 (시작시점 = 100)')
st.write('왼쪽 사이드바에서 시작시점을 변경할 수 있습니다.')

df_selection_100 = df_selection/df_selection.iloc[0]
line_charts = pe.line(df_selection_100, df_selection_100.index,
                      y = df_selection_100.columns[:4])

# 나중에 legend 사이즈 늘이고 줄이기
line_charts.update_layout(margin=dict(l=0, r=50, t=50, b=0))


st.plotly_chart(line_charts)


# columns
col1, col2 = st.columns(2)

# col1_sub = '(Last Price = ' +\
#                 str(round(df_selection[col1_var].iloc[-1])) + ')'
# st.markdown(f"""
#     <div style="text-align: center"> {col1_sub} </div>
#     """,
#     unsafe_allow_html=True)

with col1:
    col1_var = 'SP500'
    st.markdown(f"""
        <div style="color: Red; font-size: large;text-align: center"> {col1_var} </div>
        """, unsafe_allow_html=True)
    chart1 = pe.line(df_selection, df_selection.index,
                      y = df_selection['SP500'])
    chart1.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(chart1)

with col2:
    col2_var = 'NASDAQ'
    st.markdown(f"""
        <div style="color: Red; font-size: large;text-align: center"> {col2_var} </div>
        """, unsafe_allow_html=True)
    chart2 = pe.line(df_selection, df_selection.index,
                      y = df_selection['NASDAQ'])
    chart2.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(chart2)


col3, col4 = st.columns(2)

with col3:
    col3_var = 'KOSPI'
    st.markdown(f"""
        <div style="color: Red; font-size: large;text-align: center"> {col3_var} </div>
        """, unsafe_allow_html=True)
    chart3 = pe.line(df_selection, df_selection.index,
                      y = df_selection['KOSPI'])
    chart3.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(chart3)

with col4:
    col4_var = 'VIX'
    st.markdown(f"""
        <div style="color: Red; font-size: large;text-align: center"> {col4_var} </div>
        """, unsafe_allow_html=True)
    chart4 = pe.line(df_selection, df_selection.index,
                      y = df_selection['VIX'])
    chart4.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(chart4)
    
#st.table(df_selection)





