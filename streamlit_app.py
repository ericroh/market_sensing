import streamlit as st

# --- style control --- #

sidebar_css = """
   <style>
   [data-testid="stSidebar"][aria-expanded="true"]{
       min-width: 350px;
       max-width: 450px;
   }
   """
    
margins_css = """
    <style>
        .main > div {
            padding-up: 0rem;
            padding-down: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
    </style>
"""

block_css = """
    <style>
           .block-container {
                padding-top: 5rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
    </style>
"""

st.set_page_config(
    layout="wide"
)

st.markdown(sidebar_css+
            margins_css+
            block_css, 
    unsafe_allow_html=True,
)   

# --- PAGE SETUP ---
page1 = st.Page(
    "pages/1_글로벌_지수.py",
    title="글로벌 지수",
    icon=":material/finance_mode:",
    default=True,
)

page2 = st.Page(
    "pages/2_섹터_데이터.py",
    title="섹터 (미국)",
    icon=":material/bar_chart:",
)

page3 = st.Page(
    "pages/3_리스크_데이터.py",
    title="리스크 지수",
    icon=":material/attach_money:",
)

page4 = st.Page(
    "pages/4_금리_데이터.py",
    title="금리 데이터",
    icon=":material/account_balance:",
)

page5 = st.Page(
    "pages/5_연준_데이터.py",
    title="연준 데이터",
    icon=":material/money_bag:",
)

page6 = st.Page(
    "pages/6_포트폴리오.py",
    title="포트폴리오 모음",
    icon=":material/money_bag:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "마켓셍싱": [page1,page2,page3,page4,page5],
        "포트폴리오": [page6]
    }
)


# --- SHARED ON ALL PAGES ---
st.sidebar.markdown("Made by Channel Strategy")


# --- RUN NAVIGATION ---
pg.run()