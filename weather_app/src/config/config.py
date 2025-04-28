"""
配置文件：包含API設置和常量
"""
import os
from dotenv import load_dotenv

# 加載環境變數
load_dotenv()

# API設置
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0"

# 天氣圖層設置
WEATHER_LAYERS = {
    "PAC0": "對流降水",
    "PR0": "降水強度",
    "PA0": "累積降水量",
    "PAR0": "累積雨量",
    "PAS0": "累積降雪量",
    "SD0": "積雪深度",
    "WS10": "10米高度風速",
    "WND": "風速和風向",
    "APM": "海平面氣壓",
    "TA2": "2米高度氣溫",
    "TD2": "露點溫度",
    "TS0": "土壤溫度(0-10cm)",
    "TS10": "土壤溫度(>10cm)",
    "HRD0": "相對濕度",
    "CL": "雲量"
}

# 圖層單位
LAYER_UNITS = {
    "PAC0": "mm",
    "PR0": "mm/s",
    "PA0": "mm",
    "PAR0": "mm",
    "PAS0": "mm",
    "SD0": "m",
    "WS10": "m/s",
    "WND": "m/s",
    "APM": "hPa",
    "TA2": "°C",
    "TD2": "°C",
    "TS0": "K",
    "TS10": "K",
    "HRD0": "%",
    "CL": "%"
}

# 圖層默認設置
LAYER_DEFAULTS = {
    "PAC0": {"opacity": 0.8, "fill_bound": False},
    "PR0": {"opacity": 0.8, "fill_bound": False},
    "PA0": {"opacity": 0.6, "fill_bound": False},
    "PAR0": {"opacity": 0.6, "fill_bound": False},
    "PAS0": {"opacity": 0.7, "fill_bound": False},
    "SD0": {"opacity": 0.8, "fill_bound": False},
    "WS10": {"opacity": 0.6, "fill_bound": False},
    "WND": {"opacity": 0.6, "fill_bound": False, "use_norm": False, "arrow_step": 32},
    "APM": {"opacity": 0.4, "fill_bound": True},
    "TA2": {"opacity": 0.3, "fill_bound": True},
    "TD2": {"opacity": 0.3, "fill_bound": True},
    "TS0": {"opacity": 0.8, "fill_bound": True},
    "TS10": {"opacity": 0.8, "fill_bound": False},
    "HRD0": {"opacity": 0.8, "fill_bound": True},
    "CL": {"opacity": 0.5, "fill_bound": False}
}

# 地圖設置
DEFAULT_ZOOM = 10
DEFAULT_OPACITY = 0.7
MAP_STYLES = {
    "light": {
        "name": "亮色主題",
        "url": "CartoDB positron",
        "attr": "© OpenStreetMap contributors © CARTO"
    },
    "dark": {
        "name": "暗色主題",
        "url": "CartoDB dark_matter",
        "attr": "© OpenStreetMap contributors © CARTO"
    },
    "street": {
        "name": "街道地圖",
        "url": "OpenStreetMap",
        "attr": "© OpenStreetMap contributors"
    },
    "satellite": {
        "name": "衛星影像",
        "url": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        "attr": "© Google"
    },
    "terrain": {
        "name": "地形圖",
        "url": "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        "attr": "© Google"
    },
    "hybrid": {
        "name": "混合地圖",
        "url": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        "attr": "© Google"
    }
}

# 圖層顏色配置
LAYER_COLORS = {
    "PAC0": {
        "description": "對流降水顏色說明",
        "colors": [
            {"value": "0", "color": "#E6F3FF", "label": "無降水"},
            {"value": "1", "color": "#ACAAF7", "label": "輕度"},
            {"value": "10", "color": "#8D8AF3", "label": "中度"},
            {"value": "20", "color": "#706EC2", "label": "較強"},
            {"value": "40", "color": "#5658FF", "label": "強"},
            {"value": "100", "color": "#5B5DB1", "label": "很強"},
            {"value": "200", "color": "#3E3F85", "label": "極強"}
        ]
    },
    "PR0": {
        "description": "降水強度顏色說明",
        "colors": [
            {"value": "0", "color": "#FFFFFF", "label": "無降水"},
            {"value": "0.000005", "color": "#FEF9CA", "label": "極微"},
            {"value": "0.000463", "color": "#F2A33A", "label": "輕微"},
            {"value": "0.000926", "color": "#EB4726", "label": "中等"},
            {"value": "0.001388", "color": "#B02318", "label": "較強"},
            {"value": "0.002315", "color": "#971D13", "label": "強"},
            {"value": "0.023150", "color": "#090A08", "label": "極強"}
        ]
    },
    "PA0": {
        "description": "累積降水量顏色說明",
        "colors": [
            {"value": "0", "color": "#FFFFFF", "label": "無降水"},
            {"value": "0.1", "color": "#C8E6FF", "label": "毛毛雨"},
            {"value": "0.5", "color": "#7878BE", "label": "小雨"},
            {"value": "1", "color": "#6E6ECD", "label": "中雨"},
            {"value": "10", "color": "#5050E1", "label": "大雨"},
            {"value": "50", "color": "#3232FF", "label": "豪雨"},
            {"value": "140", "color": "#1414FF", "label": "暴雨"}
        ]
    },
    "PAR0": {
        "description": "累積雨量顏色說明",
        "colors": [
            {"value": "0", "color": "#FFFFFF", "label": "無雨"},
            {"value": "0.1", "color": "#C8E6FF", "label": "毛毛雨"},
            {"value": "1", "color": "#6E6ECD", "label": "小雨"},
            {"value": "10", "color": "#5050E1", "label": "中雨"},
            {"value": "50", "color": "#3232FF", "label": "大雨"},
            {"value": "140", "color": "#1414FF", "label": "暴雨"}
        ]
    },
    "PAS0": {
        "description": "累積降雪量顏色說明",
        "colors": [
            {"value": "0", "color": "#FFFFFF", "label": "無雪"},
            {"value": "0.1", "color": "#E6F3FF", "label": "微雪"},
            {"value": "1", "color": "#B4E1FF", "label": "小雪"},
            {"value": "5", "color": "#82CFFF", "label": "中雪"},
            {"value": "10", "color": "#50BDFF", "label": "大雪"},
            {"value": "25", "color": "#1EABFF", "label": "暴雪"}
        ]
    },
    "SD0": {
        "description": "積雪深度顏色說明",
        "colors": [
            {"value": "0", "color": "#FFFFFF", "label": "無積雪"},
            {"value": "0.05", "color": "#EDEDED", "label": "薄雪"},
            {"value": "0.2", "color": "#A5E5EF", "label": "淺雪"},
            {"value": "0.5", "color": "#00CCE8", "label": "中等"},
            {"value": "1.0", "color": "#3333CC", "label": "深雪"},
            {"value": "2.0", "color": "#85408C", "label": "很深"},
            {"value": "15.0", "color": "#E80068", "label": "極深"}
        ]
    },
    "WS10": {
        "description": "10米風速顏色說明",
        "colors": [
            {"value": "0", "color": "#FFFFFF", "label": "無風"},
            {"value": "1", "color": "#E6F3FF", "label": "軟風"},
            {"value": "5", "color": "#EECECC", "label": "輕風"},
            {"value": "15", "color": "#B364BC", "label": "強風"},
            {"value": "25", "color": "#3F213B", "label": "大風"},
            {"value": "50", "color": "#744CAC", "label": "烈風"},
            {"value": "100", "color": "#4600AF", "label": "颱風"}
        ]
    },
    "WND": {
        "description": "風速和風向顏色說明",
        "colors": [
            {"value": "0", "color": "#FFFFFF", "label": "無風"},
            {"value": "5", "color": "#EECECC", "label": "輕風"},
            {"value": "15", "color": "#B364BC", "label": "強風"},
            {"value": "25", "color": "#3F213B", "label": "大風"},
            {"value": "50", "color": "#744CAC", "label": "烈風"},
            {"value": "100", "color": "#4600AF", "label": "颱風"}
        ]
    },
    "APM": {
        "description": "海平面氣壓顏色說明",
        "colors": [
            {"value": "94000", "color": "#0073FF", "label": "低壓"},
            {"value": "98000", "color": "#4BD0D6", "label": "偏低"},
            {"value": "100000", "color": "#8DE7C7", "label": "正常"},
            {"value": "102000", "color": "#F0B800", "label": "偏高"},
            {"value": "104000", "color": "#FB5515", "label": "高壓"},
            {"value": "108000", "color": "#C60000", "label": "極高"}
        ]
    },
    "TA2": {
        "description": "2米氣溫顏色說明",
        "colors": [
            {"value": "-65", "color": "#821692", "label": "極寒"},
            {"value": "-30", "color": "#8257DB", "label": "嚴寒"},
            {"value": "-20", "color": "#208CEC", "label": "寒冷"},
            {"value": "-10", "color": "#20C4E8", "label": "冷"},
            {"value": "0", "color": "#23DDDD", "label": "溫和"},
            {"value": "10", "color": "#C2FF28", "label": "溫暖"},
            {"value": "20", "color": "#FFF028", "label": "熱"},
            {"value": "30", "color": "#FC8014", "label": "炎熱"}
        ]
    },
    "TD2": {
        "description": "露點溫度顏色說明",
        "colors": [
            {"value": "-65", "color": "#821692", "label": "極乾燥"},
            {"value": "-30", "color": "#8257DB", "label": "很乾燥"},
            {"value": "-20", "color": "#208CEC", "label": "乾燥"},
            {"value": "-10", "color": "#20C4E8", "label": "稍乾"},
            {"value": "0", "color": "#23DDDD", "label": "適中"},
            {"value": "10", "color": "#C2FF28", "label": "潮濕"},
            {"value": "20", "color": "#FFF028", "label": "很潮濕"},
            {"value": "30", "color": "#FC8014", "label": "極潮濕"}
        ]
    },
    "TS0": {
        "description": "土壤溫度(0-10cm)顏色說明",
        "colors": [
            {"value": "203", "color": "#491763", "label": "極冷"},
            {"value": "243", "color": "#5C85B7", "label": "很冷"},
            {"value": "263", "color": "#A7D8E5", "label": "冷"},
            {"value": "273", "color": "#D2E9C8", "label": "涼"},
            {"value": "283", "color": "#F2B68A", "label": "溫和"},
            {"value": "293", "color": "#EB702D", "label": "溫暖"},
            {"value": "313", "color": "#CC0000", "label": "熱"},
            {"value": "323", "color": "#990000", "label": "很熱"}
        ]
    },
    "TS10": {
        "description": "土壤溫度(>10cm)顏色說明",
        "colors": [
            {"value": "203", "color": "#491763", "label": "極冷"},
            {"value": "243", "color": "#5C85B7", "label": "很冷"},
            {"value": "263", "color": "#A7D8E5", "label": "冷"},
            {"value": "273", "color": "#D2E9C8", "label": "涼"},
            {"value": "283", "color": "#F2B68A", "label": "溫和"},
            {"value": "293", "color": "#EB702D", "label": "溫暖"},
            {"value": "313", "color": "#CC0000", "label": "熱"},
            {"value": "323", "color": "#990000", "label": "很熱"}
        ]
    },
    "HRD0": {
        "description": "相對濕度顏色說明",
        "colors": [
            {"value": "0", "color": "#DB1200", "label": "極乾燥"},
            {"value": "20", "color": "#965700", "label": "乾燥"},
            {"value": "40", "color": "#EDE100", "label": "較乾燥"},
            {"value": "60", "color": "#8BD600", "label": "適中"},
            {"value": "80", "color": "#00A808", "label": "潮濕"},
            {"value": "100", "color": "#000099", "label": "極潮濕"}
        ]
    },
    "CL": {
        "description": "雲量顏色說明",
        "colors": [
            {"value": "0", "color": "#FFFFFF", "label": "晴天"},
            {"value": "20", "color": "#FCFBFF", "label": "少雲"},
            {"value": "40", "color": "#F9F8FF", "label": "多雲"},
            {"value": "60", "color": "#F6F5FF", "label": "陰天"},
            {"value": "80", "color": "#E9E9DF", "label": "濃雲"},
            {"value": "100", "color": "#D2D2D2", "label": "密雲"}
        ]
    }
}

# 時間設置
FORECAST_DAYS = 5
HISTORY_DAYS = 5

# 語言設置
LANGUAGE = "zh_tw"

# 單位設置
UNITS = "metric"  # 公制單位

# 緩存設置
CACHE_EXPIRY = 300  # 5分鐘緩存過期

# API端點
ENDPOINTS = {
    "current_weather": f"{BASE_URL}/weather",
    "forecast": f"{BASE_URL}/forecast",
    "forecast_daily": f"{BASE_URL}/forecast/daily",
    "forecast_climate": f"{BASE_URL}/forecast/climate",  # 30天預報需要 Pro API
    "air_pollution": f"{BASE_URL}/air_pollution",
    "historical_temperature": "https://history.openweathermap.org/data/2.5/history/accumulated_temperature",  # 歷史溫度數據 API
    "historical_precipitation": "https://history.openweathermap.org/data/2.5/history/accumulated_precipitation",  # 歷史降水數據 API
    "geocoding": "http://api.openweathermap.org/geo/1.0/direct"
}

# 默認設置
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Taipei")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "TW")
DEFAULT_UNITS = os.getenv("DEFAULT_UNITS", "metric")  # 公制單位
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "zh_tw")    # 繁體中文

# 快取設置
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "cache")
CACHE_DURATION = int(os.getenv("CACHE_DURATION", "1800"))  # 30分鐘

# UI設置
UI_THEME = "light"
REFRESH_RATE = 300  # 5分鐘自動刷新
MAX_FORECAST_DAYS = 30  # 支援最多30天預報
