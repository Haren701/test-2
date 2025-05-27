import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# 페이지 설정
# -------------------
st.set_page_config(layout="wide", page_title="배송 위치 지도", page_icon="📍")

# -------------------
# 타이틀
# -------------------
st.markdown(
    "<h1 style='text-align: center; color: #2c3e50;'>📦 배송 위치 시각화</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: #7f8c8d;'>배송 데이터의 위치 정보를 조용하고 깔끔하게 표현합니다.</p>",
    unsafe_allow_html=True
)

# -------------------
# 데이터 불러오기
# -------------------
DATA_URL = DATA_URL = DATA_URL = "https://raw.githubusercontent.com/Haren701/test-2/refs/heads/main/Delivery.csv"

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
# 중심 좌표
# -------------------
center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

# -------------------
# 지도 시각화 (산점도 방식)
# -------------------
st.subheader("🗺️ 배송 위치 지도")

fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Num" if "Num" in df.columns else None,
    zoom=10,
    height=650,
    mapbox_style="carto-positron",
    color_discrete_sequence=["#3498db"],  # 부드러운 파란색
)

fig.update_traces(marker=dict(size=7, opacity=0.6))  # 작은 마커 + 투명도

fig.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    mapbox_center={"lat": center_lat, "lon": center_lon},
    title=dict(
        text="📍 배송 위치 분포",
        x=0.5,
        font=dict(size=22, color="#2c3e50")
    )
)

st.plotly_chart(fig, use_container_width=True)

# -------------------
# 데이터 미리보기
# -------------------
with st.expander("📋 데이터 미리보기", expanded=False):
    st.dataframe(df)
