import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 로드
df = pd.read_csv("202504_202504_연령별인구현황_월간_남녀구분.csv", encoding="cp949")

# 서울시 전체 데이터만 선택 (맨 위 한 행)
df_seoul = df.iloc[0:1].copy()

# 남성/여성 연령별 열 선택
cols_male = [col for col in df_seoul.columns if '남_' in col and '세' in col]
cols_female = [col for col in df_seoul.columns if '여_' in col and '세' in col]

# 연령대 라벨 추출
ages = [col.split('_')[-1] for col in cols_male]

# 데이터 전처리
male_values = df_seoul[cols_male].iloc[0].str.replace(',', '').fillna(0).astype(int) * -1
female_values = df_seoul[cols_female].iloc[0].str.replace(',', '').fillna(0).astype(int)

# plotly 그래프
fig = go.Figure()
fig.add_trace(go.Bar(y=ages, x=male_values, name='남성', orientation='h'))
fig.add_trace(go.Bar(y=ages, x=female_values, name='여성', orientation='h'))

fig.update_layout(
    title='서울시 연령별 인구 피라미드 (2025년 4월)',
    barmode='relative',
    xaxis=dict(title='인구 수', tickvals=[-10000, -5000, 0, 5000, 10000], ticktext=['1만', '5천', '0', '5천', '1만']),
    yaxis=dict(title='연령'),
    template='plotly_white',
    height=900
)

# Streamlit 출력
st.title("📊 서울시 인구 피라미드 (2025년 4월)")
st.plotly_chart(fig, use_container_width=True)
