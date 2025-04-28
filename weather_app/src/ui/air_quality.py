import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ..api.weather_api import WeatherAPI
from ..utils.data_processor import DataProcessor


def show_air_quality(lat: float, lon: float, weather_api: WeatherAPI, data_processor: DataProcessor):
    """顯示專業級空氣品質儀表板"""
    try:
        # 取得原始空氣污染資料
        air_data = weather_api.get_air_pollution(lat, lon)
        # 使用 DataProcessor 計算 EPA 標準 AQI
        air_quality = data_processor.process_air_pollution(air_data)

        # --- 自訂 CSS ---
        st.markdown("""
            <style>
            .badge {
                display: inline-block;
                padding: 0.4rem 1rem;
                border-radius: 1rem;
                font-size: 1rem;
                font-weight: bold;
                color: white;
            }
            .kpi-container { display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem; }
            .kpi-title { color:#7f8c8d; font-size:1rem; }
            .kpi-value { font-size:2rem; font-weight:bold; }
            </style>
        """, unsafe_allow_html=True)

        # --- KPI 區塊 ---
        st.markdown(f"""
        <div class="kpi-container">
          <div>
            <span class="badge" style="background:{air_quality['aqi_color']}">
              {air_quality['aqi_label']}
            </span>
            <span style="margin-left:0.8rem; font-size:1.5rem; font-weight:700;">空氣品質</span>
          </div>
          <div>
            <div class="kpi-title">即時 AQI</div>
            <div class="kpi-value" style="color:{air_quality['aqi_color']}">
              {air_quality['aqi']}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # --- AQI Donut Chart ---
        fig_donut = go.Figure(go.Pie(
            values=[air_quality['aqi'], 500 - air_quality['aqi']],
            hole=0.7,
            sort=False,
            marker_colors=[air_quality['aqi_color'], 'rgba(0,0,0,0.05)'],
            textinfo='none'
        ))
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            annotations=[{
                'text': f"<span style='font-size:2.2rem;color:{air_quality['aqi_color']};'>{air_quality['aqi']}</span><br>"
                        f"<span style='font-size:1rem;color:#7f8c8d;'>{air_quality['aqi_label']}</span>",
                'showarrow': False,
                'x': 0.5, 'y': 0.5
            }]
        )
        st.plotly_chart(fig_donut, use_container_width=True, height=280)

        # --- 健康建議 ---
        advice_map = {
            '優': "空氣品質良好，適合所有戶外活動",
            '良': "敏感族群需留意呼吸道症狀",
            '對敏感族群不健康': "敏感族群避免劇烈戶外運動",
            '不健康': "一般人減少戶外活動",
            '非常不健康': "所有人避免外出",
            '危害': "立即採取防護並室內清淨"
        }
        st.info(f"**{air_quality['aqi_label']}**：{advice_map.get(air_quality['aqi_label'], '')}")

        # --- 主要污染物濃度柱狀圖 ---
        pollutants = {
            'PM2.5': air_quality['pm2_5'],
            'PM10': air_quality['pm10'],
            'NO₂': air_quality['no2'],
            'SO₂': air_quality['so2'],
            'O₃': air_quality['o3'],
            'CO': air_quality['co']
        }
        fig_bar = px.bar(
            x=list(pollutants.keys()),
            y=list(pollutants.values()),
            title="主要污染物濃度 (μg/m³)",
            labels={"x": "污染物", "y": "濃度 (μg/m³)"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # --- 詳細指標與進度條 ---
        col1, col2 = st.columns(2)
        with col1:
            for poll, thresh, unit in [
                ('pm2_5', 15, 'μg/m³'),
                ('no2', 200, 'μg/m³'),
                ('o3', 100, 'μg/m³')
            ]:
                st.metric(poll.upper(), f"{air_quality[poll]} {unit}", help=f"WHO 建議 {thresh} {unit} 以上為高風險")
                st.progress(min(air_quality[poll] / (thresh*2), 1.0), text=f"超標 {max(0, air_quality[poll]-thresh)} {unit}")
        with col2:
            for poll, thresh, unit in [
                ('pm10', 45, 'μg/m³'),
                ('so2', 40, 'μg/m³'),
                ('co', 4000, 'μg/m³')
            ]:
                st.metric(poll.upper(), f"{air_quality[poll]} {unit}", help=f"WHO 建議 {thresh} {unit} 以上為高風險")
                st.progress(min(air_quality[poll] / (thresh*2), 1.0), text=f"超標 {max(0, air_quality[poll]-thresh)} {unit}")

        return air_quality

    except Exception as e:
        st.error(f"獲取空氣品質數據失敗：{e}")
        return None
