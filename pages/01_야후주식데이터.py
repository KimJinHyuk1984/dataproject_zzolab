import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# 시가총액 상위 10개 글로벌 기업 (2025년 기준 예상)
TICKERS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Meta (Facebook)": "META",
    "Berkshire Hathaway": "BRK-B",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

st.title("글로벌 시가총액 Top 10 기업 - 최근 1년 주가 변화")
st.write("데이터 출처: Yahoo Finance")

# 날짜 범위 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 종목 선택
selected_companies = st.multiselect(
    "기업 선택 (최대 5개)", list(TICKERS.keys()), default=list(TICKERS.keys())[:5], max_selections=5
)

# 데이터 가져오기
if selected_companies:
    fig = go.Figure()
    for company in selected_companies:
        ticker = TICKERS[company]
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data["Adj Close"],
                mode="lines",
                name=company
            ))
        else:
            st.warning(f"{company} 데이터 없음")

    fig.update_layout(
        title="최근 1년 주가 (조정 종가 기준)",
        xaxis_title="날짜",
        yaxis_title="주가 (USD)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("최소 한 개 이상의 기업을 선택해주세요.")
