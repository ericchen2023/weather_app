"""
天氣地圖顯示組件
"""
import streamlit as st
import folium
from folium import plugins
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import branca.colormap as cm
from ..api.weather_api import WeatherAPI
from ..config.config import (
    WEATHER_LAYERS, LAYER_UNITS, LAYER_DEFAULTS,
    MAP_STYLES, LAYER_COLORS
)

def create_color_scale(colors):
    """創建顏色刻度"""
    return cm.LinearColormap(
        colors=[c["color"] for c in colors],
        vmin=float(colors[0]["value"]),
        vmax=float(colors[-1]["value"])
    )

def show_weather_map(lat: float, lon: float, location: str, api: WeatherAPI):
    """
    顯示天氣地圖的公共接口函數
    
    參數:
        lat: float - 緯度
        lon: float - 經度
        location: str - 位置名稱
        api: WeatherAPI - API實例
    """
    st.subheader(f"🗺️ {location}的天氣地圖")
    
    weather_map = WeatherMap(api)
    
    # 地圖樣式選擇
    map_style = st.selectbox(
        "選擇地圖樣式",
        options=list(MAP_STYLES.keys()),
        format_func=lambda x: MAP_STYLES[x]["name"],
        key="map_style"
    )
    
    # 圖層選擇
    layer_type = st.selectbox(
        "選擇天氣圖層",
        options=list(WEATHER_LAYERS.keys()),
        format_func=lambda x: f"{WEATHER_LAYERS[x]} ({LAYER_UNITS[x]})",
        key="weather_layer"
    )
    
    # 獲取圖層默認設置
    layer_defaults = LAYER_DEFAULTS[layer_type]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # 透明度控制
        opacity = st.slider(
            "圖層透明度",
            min_value=0.0,
            max_value=1.0,
            value=layer_defaults["opacity"],
            step=0.1,
            key="layer_opacity"
        )
    
    with col2:
        # 填充邊界控制
        fill_bound = st.checkbox(
            "填充邊界值",
            value=layer_defaults["fill_bound"],
            key="fill_bound"
        )
    
    # 特殊設置（如果是風向圖層）
    extra_params = {}
    if layer_type == "WND":
        col1, col2 = st.columns(2)
        with col1:
            arrow_step = st.slider(
                "箭頭間距",
                min_value=16,
                max_value=64,
                value=layer_defaults["arrow_step"],
                step=16,
                key="arrow_step"
            )
            extra_params["arrow_step"] = arrow_step
        
        with col2:
            use_norm = st.checkbox(
                "標準化箭頭長度",
                value=layer_defaults["use_norm"],
                key="use_norm"
            )
            extra_params["use_norm"] = use_norm
    
    # 創建地圖
    m = weather_map.create_map(lat, lon, location, layer_type, map_style, opacity, fill_bound, extra_params)
    
    # 顯示地圖
    col1, col2 = st.columns([3, 1])
    with col1:
        folium_static(m, width=700)
    
    with col2:
        st.markdown("### 圖層說明")
        st.markdown(f"**當前圖層**: {WEATHER_LAYERS[layer_type]}")
        st.markdown(f"**單位**: {LAYER_UNITS[layer_type]}")
        
        # 顯示顏色圖例
        if layer_type in LAYER_COLORS:
            st.markdown("---")
            st.markdown("### 顏色說明")
            colors = LAYER_COLORS[layer_type]["colors"]
            for color in colors:
                st.markdown(
                    f'<div style="display:flex;align-items:center;">'
                    f'<div style="width:20px;height:20px;background-color:{color["color"]};margin-right:10px;"></div>'
                    f'<div>{color["label"]}: {color["value"]} {LAYER_UNITS[layer_type]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        
        if layer_type == "WND":
            st.markdown("---")
            st.markdown("### 風向設置")
            st.markdown(f"**箭頭間距**: {arrow_step}像素")
            st.markdown(f"**標準化箭頭**: {'是' if use_norm else '否'}")
        
        st.markdown("---")
        st.markdown("### 位置資訊")
        st.markdown(f"**地點**: {location}")
        st.markdown(f"**緯度**: {lat:.2f}")
        st.markdown(f"**經度**: {lon:.2f}")
        st.markdown("---")
        st.markdown("### 數據更新時間")
        st.markdown(f"_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")

class WeatherMap:
    def __init__(self, api: WeatherAPI):
        self.api = api
        self.tile_url = "https://maps.openweathermap.org/maps/2.0/weather/{layer}/{z}/{x}/{y}?appid={api_key}"
        
    def create_map(self, lat: float, lon: float, location: str, layer_type: str = "TA2",
                  map_style: str = "light", opacity: float = 0.7, fill_bound: bool = False,
                  extra_params: dict = None):
        """
        創建天氣地圖
        
        參數:
            lat: float - 緯度
            lon: float - 經度
            location: str - 位置名稱
            layer_type: str - 天氣圖層類型
            map_style: str - 地圖樣式
            opacity: float - 圖層透明度
            fill_bound: bool - 是否填充邊界值
            extra_params: dict - 額外參數（用於風向圖層）
        """
        # 基礎地圖
        style = MAP_STYLES[map_style]
        m = folium.Map(
            location=[lat, lon],
            zoom_start=10,
            tiles=style["url"],
            attr=style["attr"]
        )
        
        # 構建天氣圖層URL
        params = {
            "layer": layer_type,
            "api_key": self.api.api_key,
            "z": "{z}",
            "x": "{x}",
            "y": "{y}",
            "fill_bound": str(fill_bound).lower()
        }
        
        # 添加風向圖層的特殊參數
        if layer_type == "WND" and extra_params:
            params.update({
                "arrow_step": extra_params.get("arrow_step", 32),
                "use_norm": str(extra_params.get("use_norm", False)).lower()
            })
        
        # 生成URL
        weather_tile = self.tile_url.format(**params)
        
        # 添加天氣圖層
        weather_layer = folium.TileLayer(
            tiles=weather_tile,
            attr='Weather data &copy; <a href="https://openweathermap.org">OpenWeather</a>',
            name=WEATHER_LAYERS[layer_type],
            overlay=True,
            opacity=opacity
        )
        weather_layer.add_to(m)
        
        # 添加圖層控制
        folium.LayerControl().add_to(m)
        
        # 添加數值顯示功能
        m.add_child(folium.LatLngPopup())
        
        # 添加標記
        folium.Marker(
            [lat, lon],
            popup=f"""
            <div style='width:200px'>
                <b>{location}</b><br>
                緯度: {lat:.2f}<br>
                經度: {lon:.2f}<br>
                圖層: {WEATHER_LAYERS[layer_type]}<br>
                單位: {LAYER_UNITS[layer_type]}
            </div>
            """,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        
        # 添加鼠標懸停提示
        m.add_child(plugins.MousePosition(
            position='topright',
            separator=' | ',
            prefix=f"{WEATHER_LAYERS[layer_type]}: ",
            num_digits=2,
            unit=f" {LAYER_UNITS[layer_type]}"
        ))
        
        return m 