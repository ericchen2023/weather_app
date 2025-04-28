"""
主應用程式：整合所有天氣功能組件
"""
import os
import sys
import streamlit as st
from datetime import datetime, timedelta
import pytz
import plotly.express as px

# 將 src 目錄加入 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, os.path.dirname(current_dir))

from src.api.weather_api import WeatherAPI
from src.utils.data_processor import DataProcessor
from src.utils.cache_manager import CacheManager
from src.config.config import DEFAULT_CITY

# 導入UI組件
from src.ui.current_weather import show_current_weather
from src.ui.forecast import show_hourly_forecast, show_daily_forecast, show_monthly_forecast
from src.ui.air_quality import show_air_quality
from src.ui.weather_map import show_weather_map

# 初始化
weather_api = WeatherAPI()
data_processor = DataProcessor()
cache_manager = CacheManager()

# 設置頁面配置
st.set_page_config(
    page_title="天氣資訊儀表板",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 側邊欄
with st.sidebar:
    st.title("⚙️ 設置")
    city = st.text_input("城市", value=DEFAULT_CITY)
    
    # 獲取城市地理位置
    try:
        geo_data = weather_api.get_location_by_name(city)
        if geo_data:
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            location = f"{geo_data[0].get('local_names', {}).get('zh', city)}"
        else:
            st.error("找不到該城市")
            st.stop()
    except Exception as e:
        st.error(f"獲取地理位置失敗: {str(e)}")
        st.stop()

# 主頁面
st.title(f"🌤️ {location}天氣資訊儀表板")

# 當前天氣
show_current_weather(lat, lon, weather_api, data_processor)

# 天氣預報標籤頁
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 每小時預報",
    "📅 每日預報",
    "🌡️ 30天預報",
    "💨 空氣品質"
])

# 每小時預報
with tab1:
    show_hourly_forecast(lat, lon, weather_api, data_processor)

# 每日預報
with tab2:
    show_daily_forecast(lat, lon, weather_api, data_processor)

# 30天預報
with tab3:
    try:
        monthly_data = weather_api.get_monthly_forecast(lat, lon)
        monthly_df = data_processor.process_daily_forecast(monthly_data)
        
        forecast_days = len(monthly_df)
        st.subheader(f"🌡️ {forecast_days}天溫度趨勢")
        
        # 繪製溫度趨勢圖
        fig = px.line(monthly_df, x='date', y=['temp_day', 'temp_min', 'temp_max'],
                      title=f"未來{forecast_days}天溫度預報",
                      labels={
                          "temp_day": "日均溫度 (°C)",
                          "temp_min": "最低溫度 (°C)",
                          "temp_max": "最高溫度 (°C)",
                          "date": "日期"
                      })
        st.plotly_chart(fig, use_container_width=True)
        
        # 顯示降水和濕度信息
        st.subheader("💧 降水和濕度")
        fig2 = px.bar(monthly_df, x='date', y=['humidity', 'pop'],
                     title=f"未來{forecast_days}天降水機率和濕度",
                     labels={
                         "humidity": "濕度 (%)",
                         "pop": "降水機率 (%)",
                         "date": "日期"
                     },
                     barmode='group')
        st.plotly_chart(fig2, use_container_width=True)
        
        if st.checkbox("顯示詳細數據"):
            st.dataframe(
                monthly_df.style.format({
                    'temp_day': '{:.1f}°C',
                    'temp_min': '{:.1f}°C',
                    'temp_max': '{:.1f}°C',
                    'humidity': '{:.0f}%',
                    'pop': '{:.0f}%'
                })
            )
            
        if forecast_days < 30:
            st.info("注意：目前使用免費版 API，僅支援最多 16 天預報。若需要完整 30 天預報，請升級至 Pro 版本。")
            
    except Exception as e:
        st.error(f"獲取天氣預報失敗: {str(e)}")

# 空氣品質
with tab4:
    show_air_quality(lat, lon, weather_api, data_processor)

# 天氣地圖
show_weather_map(lat, lon, location, weather_api)

# 更新時間
st.sidebar.markdown("---")
st.sidebar.write(f"最後更新時間: {datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')}")

# 快取清理提示
if st.sidebar.button("清理快取"):
    cache_manager.clear()
    st.sidebar.success("快取已清理") 