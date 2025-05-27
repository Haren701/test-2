import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# 페이지 설정
# -------------------
st.set_page_config(layout="wide", page_title="배송 위치 밀도 시각화", page_icon="📍")

# -------------------
# 타이틀
# -------------------
st.markdown("<h1 style='text-align: center;'>📦 배송 위치 밀도 시각화</h1>", unsafe_allow_html=True)
st.markdown("배송 위치의 **군집 밀도**를 지도 위에 표현한 시각화입니다.")

# -------------------
# 데이터 불러오기
# -------------------
DATA_URL = DATA_URL = "https://raw.githubusercontent.com/Haren701/test-2/refs/heads/main/Delivery.csv"

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
# 지도 중심 좌표 계산
# -------------------
center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

# -------------------
# Plotly 밀도 지도 시각화
# -------------------
st.subheader("🗺️ 배송 위치 군집 밀도 지도")

fig = px.density_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    z=None,
    radius=20,  # 클수록 부드럽고 넓은 영역을 나타냄
    center=dict(lat=center_lat, lon=center_lon),
    zoom=10,
    mapbox_style="carto-positron",
    height=650,
    title="📍 배송 위치 밀도 분포"
)

fig.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    title=dict(
        x=0.5,
        xanchor="center",
        font=dict(size=22)
    )
)

st.plotly_chart(fig, use_container_width=True)

# -------------------
# 데이터 미리보기
# -------------------
with st.expander("🔍 데이터 미리보기"):
    st.dataframe(df)
