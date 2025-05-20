import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로
MALE_FEMALE_CSV = "202504_202504_연령별인구현황_월간_남녀구분.csv"

# 데이터 불러오기
df_mf = pd.read_csv(MALE_FEMALE_CSV, encoding='cp949')

# 서울특별시 전체 데이터만 추출
df_seoul = df_mf[df_mf['행정구역'].str.contains('서울특별시  ')].iloc[0]

# 남자, 여자 연령별 컬럼 추출
male_cols = [col for col in df_mf.columns if "남_" in col and "세" in col]
female_cols = [col for col in df_mf.columns if "여_" in col and "세" in col]
ages = [col.split('_')[-1].replace('세', '') for col in male_cols]

# 숫자 변환 및 음수로 변환 (피라미드용)
male_counts = df_seoul[male_cols].str.replace(",", "").astype(int) * -1
female_counts = df_seoul[female_cols].str.replace(",", "").astype(int)

# Streamlit 화면 구성
st.title("📊 서울시 인구 피라미드 (남녀 구분) - 2025년 4월")

fig = go.Figure()
fig.add_trace(go.Bar(y=ages, x=male_counts, name='남자', orientation='h', marker_color='blue'))
fig.add_trace(go.Bar(y=ages, x=female_counts, name='여자', orientation='h', marker_color='red'))

fig.update_layout(
    barmode='relative',
    title='서울특별시 연령별 인구 피라미드',
    xaxis=dict(title='인구수', tickvals=[-30000, -15000, 0, 15000, 30000],
               ticktext=['30,000', '15,000', '0', '15,000', '30,000']),
    yaxis=dict(title='연령'),
    height=800
)

st.plotly_chart(fig, use_container_width=True)
