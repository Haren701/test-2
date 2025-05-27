import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# 페이지 설정
# -------------------
st.set_page_config(layout="wide", page_title="배송 위치 지도", page_icon="📍")

# -------------------
# 타이틀 및 설명
# -------------------
st.markdown("<h1 style='text-align: center;'>📦 배송 위치 지도 시각화</h1>", unsafe_allow_html=True)
st.markdown("배송 데이터의 위치 정보를 기반으로 지도에 시각화한 결과입니다. 아래에서 지도 필터를 조정해보세요.")

# -------------------
# 데이터 불러오기
# -------------------
DATA_URL = "https://raw.githubusercontent.com/Haren701/test-2/refs/heads/main/Delivery.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

# -------------------
# 필수 컬럼 체크
# -------------------
if "Latitude" not in df.columns or "Longitude" not in df.columns:
    st.error("❌ 필수 컬럼(Latitude, Longitude)이 누락되었습니다.")
    st.stop()

# -------------------
# 레이아웃: 좌/우 컬럼 나눠서 필터 슬라이더 배치
# -------------------
st.subheader("📌 위치 필터")
col1, col2 = st.columns(2)

with col1:
    lat_range = st.slider(
        "위도 범위",
        float(df["Latitude"].min()), float(df["Latitude"].max()),
        (float(df["Latitude"].min()), float(df["Latitude"].max()))
    )

with col2:
    lon_range = st.slider(
        "경도 범위",
        float(df["Longitude"].min()), float(df["Longitude"].max()),
        (float(df["Longitude"].min()), float(df["Longitude"].max()))
    )

# 필터 적용
filtered_df = df[
    (df["Latitude"].between(*lat_range)) &
    (df["Longitude"].between(*lon_range))
]

# -------------------
# 지도 중심 자동 설정
# -------------------
center_lat = filtered_df["Latitude"].mean()
center_lon = filtered_df["Longitude"].mean()

# -------------------
# Plotly 지도 시각화
# -------------------
st.subheader("🗺️ 배송 위치 분포 지도")

fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Num" if "Num" in df.columns else None,
    hover_data={"Latitude": True, "Longitude": True},
    zoom=10,
    height=600,
    mapbox_style="carto-positron",
    color_discrete_sequence=["#2b83ba"],  # 파란 계열 지정
)

fig.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    mapbox_center={"lat": center_lat, "lon": center_lon},
    title=dict(
        text="📍 배송 위치 분포",
        x=0.5,
        xanchor="center",
        font=dict(size=24)
    )
)

st.plotly_chart(fig, use_container_width=True)

# -------------------
# 데이터 미리보기 (선택 사항)
# -------------------
with st.expander("🔍 데이터 미리보기"):
    st.dataframe(filtered_df)
