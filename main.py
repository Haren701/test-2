import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(layout="wide")
st.title("📦 배송 위치 시각화")

# GitHub에 있는 CSV 파일 URL (예시로 대체)
DATA_URL = https://raw.githubusercontent.com/Haren701/test-2/refs/heads/main/Delivery.csv

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

# 데이터 로드
df = load_data()

# 필수 컬럼 검사
if "Latitude" not in df.columns or "Longitude" not in df.columns:
    st.error("❌ 필수 컬럼(Latitude, Longitude)이 누락되었습니다.")
    st.stop()

# 데이터 미리보기
st.subheader("🔍 데이터 미리보기")
st.dataframe(df)

# 위도/경도 필터 슬라이더
lat_range = st.slider(
    "위도 범위", float(df["Latitude"].min()), float(df["Latitude"].max()),
    (float(df["Latitude"].min()), float(df["Latitude"].max()))
)
lon_range = st.slider(
    "경도 범위", float(df["Longitude"].min()), float(df["Longitude"].max()),
    (float(df["Longitude"].min()), float(df["Longitude"].max()))
)

# 필터 적용
filtered_df = df[
    (df["Latitude"].between(*lat_range)) &
    (df["Longitude"].between(*lon_range))
]

# 지도 중심 좌표 계산
center_lat = filtered_df["Latitude"].mean()
center_lon = filtered_df["Longitude"].mean()

# Plotly 지도 시각화
st.subheader("🗺️ 배송 위치 지도")
fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Num" if "Num" in filtered_df.columns else None,
    zoom=10,
    height=600,
    mapbox_style="open-street-map",
    title="배송 위치 분포"
)
fig.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon})

# 결과 출력
st.plotly_chart(fig, use_container_width=True)
