import streamlit as st
import pandas as pd
import numpy as np
import requests
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.title("신한 PRM 카드 무료주차장 지도")

# 1. 데이터 파일 직접 불러오기
DATA_FILE = "신한RPM(250517)서울.xlsx"   # csv로 하려면 "신한RPM(250517)_seoul.csv"
df = pd.read_excel(DATA_FILE)   # csv 파일일 경우 pd.read_csv(DATA_FILE)

st.write("데이터 미리보기", df.head())

# 2. 네이버 API 입력 (변경 가능)
client_id = st.text_input("NAVER Client ID", value="buvx09i4ew")
client_pw = st.text_input("NAVER Client Secret", value="bteRnQRR6FJOyrN04UXulAVpI1ijl9MBXO0gb2jT")
api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='

# 3. 좌표 변환 실행 버튼
if st.button("위도/경도 변환 및 지도 생성"):
    geo_coordi = []
    for addr in df['주소']:
        url = api_url + requests.utils.quote(addr)
        headers = {
            'X-NCP-APIGW-API-KEY-ID': client_id,
            'X-NCP-APIGW-API-KEY': client_pw
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            result = res.json()
            if result['addresses']:
                latitude = float(result['addresses'][0]['y'])
                longitude = float(result['addresses'][0]['x'])
            else:
                latitude = None
                longitude = None
        else:
            latitude = None
            longitude = None
        geo_coordi.append([latitude, longitude])

    coords = np.array(geo_coordi)
    df['위도'] = coords[:, 0]
    df['경도'] = coords[:, 1]

    st.write("위도/경도 변환 결과", df.head())

    # 지도 표시
    valid_rows = df.dropna(subset=['위도', '경도'])
    if not valid_rows.empty:
        map_center = [valid_rows['위도'].values[0], valid_rows['경도'].values[0]]
        m = folium.Map(location=map_center, zoom_start=12)
        marker_cluster = MarkerCluster().add_to(m)
        for _, row in valid_rows.iterrows():
            folium.Marker(
                location=[row['위도'], row['경도']],
                tooltip=row['명칭'],
                icon=folium.Icon(color="green")
            ).add_to(marker_cluster)
        st_folium(m, width=700, height=500)
    else:
        st.warning("변환된 좌표가 없습니다. 주소 또는 API 키를 확인해주세요.")

    # 다운로드 기능
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="변환 결과 다운로드 (CSV)",
        data=csv,
        file_name="신한RPM_좌표포함.csv",
        mime='text/csv'
    )
