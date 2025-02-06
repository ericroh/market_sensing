import streamlit as st
import pandas as pd 
import numpy as np
import gspread
from utils.utils import *
import plotly.express as pe

@st.cache_data
def get_and_prepare_data():
    # Connect to GS
    GSHEETS_CREDENTIALS = 'market-sensing-449014-a6c257ded130.json'
    client = gspread.service_account(GSHEETS_CREDENTIALS)
    sheet = client.open('Dashboard_Marketsensing')
    
    worksheet_list = sheet.worksheets()
    pg1 = sheet.worksheet("Sectors")
    df_pg = pd.DataFrame(pg1.get_all_records())
    df_pg = ensure_datetime(df_pg, 'Date')
    df_pg.set_index('Date', inplace=True)
    df_pg.fillna(method='ffill',inplace=True)
    
    return df_pg

df = get_and_prepare_data()

start_date = st.sidebar.date_input("시작 시점: ", value='2024-01-03')
end_date = st.sidebar.date_input("종료 시점: ", value="today")

idx = (df.index >= pd.to_datetime(start_date)) &\
        (df.index <= pd.to_datetime(end_date))

df_selection = df[idx]
df_selection = df_selection.replace(r'^\s*$', np.nan, regex=True)
df_selection = df_selection.fillna(method='ffill').fillna(method='bfill')

#st.write('히트맵 만들기 (Update)')
st.write('### 미국 섹터별 가격 추이')

df_selection_100 = df_selection/df_selection.iloc[0]
line_charts = pe.line(df_selection_100, df_selection_100.index,
                      y = df_selection_100.columns)

# 나중에 legend 사이즈 늘이고 줄이기
line_charts.update_layout(margin=dict(l=0, r=50, t=50, b=0),
                         height = 600)
st.plotly_chart(line_charts, use_container_width=False)

# Calculate Monthly Returns
monthly_returns =df_selection_100.resample('M').last().pct_change().dropna()

# Format DataFrame
monthly_returns.index = monthly_returns.index.strftime('%Y-%m')

# Display Data
st.write("### Monthly Returns:")
st.dataframe(monthly_returns.transpose().style.format("{:.2%}"),
            use_container_width=True,height = 500)


