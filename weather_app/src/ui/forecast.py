"""
天氣預報顯示組件：包含每小時預報和每日預報
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ..api.weather_api import WeatherAPI
from ..utils.data_processor import DataProcessor

def show_hourly_forecast(lat: float, lon: float, weather_api: WeatherAPI, data_processor: DataProcessor):
    """顯示每小時天氣預報"""
    try:
        hourly_data = weather_api.get_hourly_forecast(lat, lon)
        hourly_df = data_processor.process_hourly_forecast(hourly_data)
        
        # 繪製溫度折線圖
        fig = px.line(hourly_df, x='time', y='temperature',
                     title="未來48小時溫度預報",
                     labels={"temperature": "溫度 (°C)", "time": "時間"})
        st.plotly_chart(fig, use_container_width=True)
        
        # 顯示詳細預報數據
        st.dataframe(hourly_df.set_index('time'))
        
        return hourly_df
    except Exception as e:
        st.error(f"獲取每小時預報失敗: {str(e)}")
        return None

def show_daily_forecast(lat: float, lon: float, weather_api: WeatherAPI, data_processor: DataProcessor):
    """顯示每日天氣預報"""
    try:
        daily_data = weather_api.get_daily_forecast(lat, lon)
        daily_df = data_processor.process_daily_forecast(daily_data)
        
        # 繪製溫度範圍圖
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_df['date'],
            y=daily_df['temp_max'],
            name="最高溫",
            line=dict(color='red')
        ))
        fig.add_trace(go.Scatter(
            x=daily_df['date'],
            y=daily_df['temp_min'],
            name="最低溫",
            line=dict(color='blue'),
            fill='tonexty'
        ))
        fig.update_layout(title="7天溫度預報",
                         xaxis_title="日期",
                         yaxis_title="溫度 (°C)")
        st.plotly_chart(fig, use_container_width=True)
        
        # 顯示詳細預報數據
        st.dataframe(daily_df.set_index('date'))
        
        return daily_df
    except Exception as e:
        st.error(f"獲取每日預報失敗: {str(e)}")
        return None

def show_monthly_forecast(lat: float, lon: float, weather_api: WeatherAPI, data_processor: DataProcessor):
    """顯示30天天氣預報"""
    try:
        monthly_data = weather_api.get_30_day_forecast(lat, lon)
        monthly_df = data_processor.process_daily_forecast(monthly_data)
        
        # 繪製30天溫度趨勢圖
        fig = px.line(monthly_df, x='date', y=['temp_day', 'temp_min', 'temp_max'],
                     title="30天溫度趨勢",
                     labels={"value": "溫度 (°C)", "date": "日期",
                            "variable": "類型"},
                     color_discrete_map={
                         "temp_day": "green",
                         "temp_min": "blue",
                         "temp_max": "red"
                     })
        st.plotly_chart(fig, use_container_width=True)
        
        return monthly_df
    except Exception as e:
        st.error(f"獲取30天預報失敗: {str(e)}")
        return None 