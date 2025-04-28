"""
當前天氣顯示組件
"""
import streamlit as st
from ..api.weather_api import WeatherAPI
from ..utils.data_processor import DataProcessor

def show_current_weather(lat: float, lon: float, weather_api: WeatherAPI, data_processor: DataProcessor):
    """顯示當前天氣信息"""
    try:
        current_weather_data = weather_api.get_current_weather(lat, lon)
        current_weather = data_processor.process_current_weather(current_weather_data)
        
        # 顯示當前天氣
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("溫度", f"{current_weather['temperature']}°C",
                     f"體感 {current_weather['feels_like']}°C")
        with col2:
            st.metric("濕度", f"{current_weather['humidity']}%")
        with col3:
            st.metric("風速", f"{current_weather['wind_speed']} m/s")
            
        # 天氣警報
        alert_level, alerts = data_processor.get_weather_alert_level(current_weather)
        if alerts:
            alert_color = {"正常": "green", "警告": "orange", "危險": "red"}[alert_level]
            st.markdown(
                f"<div style='padding: 10px; background-color: {alert_color}; "
                f"color: white; border-radius: 5px;'><b>{alert_level}:</b> "
                f"{', '.join(alerts)}</div>",
                unsafe_allow_html=True
            )
            
        return current_weather
    except Exception as e:
        st.error(f"獲取當前天氣失敗: {str(e)}")
        return None 