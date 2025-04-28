"""
數據處理工具類：負責處理和轉換天氣數據
"""
from typing import Dict, List, Union
import pandas as pd
from datetime import datetime

class DataProcessor:
    @staticmethod
    def process_current_weather(data: Dict) -> Dict:
        """處理當前天氣數據"""
        try:
            return {
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind']['deg'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset'])
            }
        except KeyError as e:
            raise Exception(f"處理當前天氣數據失敗: 缺少關鍵數據 {str(e)}")

    @staticmethod
    def process_hourly_forecast(data: List[Dict]) -> pd.DataFrame:
        """處理每小時預報數據"""
        try:
            processed = []
            for hour in data:
                processed.append({
                    'time': datetime.fromtimestamp(hour['dt']),
                    'temperature': round(hour['main']['temp'], 1),
                    'feels_like': round(hour['main']['feels_like'], 1),
                    'humidity': hour['main']['humidity'],
                    'pressure': hour['main']['pressure'],
                    'wind_speed': hour['wind']['speed'],
                    'description': hour['weather'][0]['description'],
                    'icon': hour['weather'][0]['icon'],
                    'pop': hour.get('pop', 0) * 100
                })
            return pd.DataFrame(processed)
        except KeyError as e:
            raise Exception(f"處理每小時預報數據失敗: 缺少關鍵數據 {str(e)}")

    @staticmethod
    def process_daily_forecast(data: List[Dict]) -> pd.DataFrame:
        """處理每日預報數據"""
        try:
            processed = []
            for day in data:
                temp = day['temp']
                processed.append({
                    'date': datetime.fromtimestamp(day['dt']),
                    'temp_day': round(temp['day'], 1) if isinstance(temp, dict) else round(temp, 1),
                    'temp_min': round(day.get('temp_min', temp.get('min')), 1),
                    'temp_max': round(day.get('temp_max', temp.get('max')), 1),
                    'humidity': day['humidity'],
                    'pressure': day['pressure'],
                    'wind_speed': day.get('speed', day.get('wind_speed')),
                    'description': day['weather'][0]['description'],
                    'icon': day['weather'][0]['icon'],
                    'pop': day.get('pop', 0) * 100
                })
            return pd.DataFrame(processed)
        except KeyError as e:
            raise Exception(f"處理每日預報數據失敗: 缺少關鍵數據 {str(e)}")

    def __init__(self):
        # EPA AQI 斷點資料（單位均為 μg/m³，CO 已換算至 μg/m³）
        self.breakpoints = {
            'pm2_5': [(0.0, 9.0, 0, 50), (9.1, 35.4, 51, 100), (35.5, 55.4, 101, 150),
                      (55.5, 125.4, 151, 200), (125.5, 225.4, 201, 300), (225.5, 325.4, 301, 500)],
            'pm10': [(0.0, 54.0, 0, 50), (55.0, 154.0, 51, 100), (155.0, 254.0, 101, 150),
                     (255.0, 354.0, 151, 200), (355.0, 424.0, 201, 300), (425.0, 604.0, 301, 500)],
            'co': [(0.0, 4400, 0, 50), (4401, 9400, 51, 100), (9401, 12400, 101, 150),
                   (12401, 15400, 151, 200), (15401, 30400, 201, 300), (30401, 50400, 301, 500)],
            'no2': [(0.0, 40, 0, 50), (41, 70, 51, 100), (71, 150, 101, 150),
                    (151, 200, 151, 200), (201, 1200, 201, 300), (1201, 2049, 301, 500)],
            'o3': [(0.0, 60, 0, 50), (61, 100, 51, 100), (101, 140, 101, 150),
                   (141, 180, 151, 200), (181, 300, 201, 300), (301, 604, 301, 500)],
            'so2': [(0.0, 20, 0, 50), (21, 80, 51, 100), (81, 250, 101, 150),
                    (251, 350, 151, 200), (351, 500, 201, 300), (501, 1004, 301, 500)]
        }

    def _calc_sub_index(self, C: float, bps: List[tuple]) -> Union[float, None]:
        """根據斷點列表計算子指標值"""
        for C_lo, C_hi, I_lo, I_hi in bps:
            if C_lo <= C <= C_hi:
                return (I_hi - I_lo) / (C_hi - C_lo) * (C - C_lo) + I_lo
        return None

    def process_air_pollution(self, data: Dict) -> Dict:
        """處理空氣污染數據並計算 EPA 標準 AQI"""
        try:
            comps = data['list'][0]['components']
            # 若 CO API 回傳單位為 mg/m³，請先換算：comps['co'] *= 1000

            sub_idx = {}
            for key, bps in self.breakpoints.items():
                if key in comps:
                    val = comps[key]
                    idx = self._calc_sub_index(val, bps)
                    if idx is not None:
                        sub_idx[key] = round(idx)

            aqi = max(sub_idx.values())
            # 對應等級與顏色
            if aqi <= 50:
                label, color = '優', '#2ecc71'
            elif aqi <= 100:
                label, color = '良', '#f1c40f'
            elif aqi <= 150:
                label, color = '對敏感族群不健康', '#e67e22'
            elif aqi <= 200:
                label, color = '不健康', '#e74c3c'
            elif aqi <= 300:
                label, color = '非常不健康', '#8e44ad'
            else:
                label, color = '危害', '#7f8c8d'

            return {
                'aqi': aqi,
                'aqi_label': label,
                'aqi_color': color,
                **{k: comps[k] for k in comps}
            }
        except KeyError as e:
            raise Exception(f"處理空氣污染數據失敗: 缺少關鍵數據 {str(e)}")

    @staticmethod
    def process_historical_weather(data: List[Dict]) -> Dict:
        """處理歷史天氣數據並計算統計數據"""
        try:
            processed = {
                'temperature': [],
                'pressure': [],
                'humidity': [],
                'wind_speed': [],
                'precipitation': [],
                'clouds': [],
                'sunshine_hours': []
            }

            for record in data:
                processed['temperature'].append(record.get('temperature', 0))
                processed['pressure'].append(record.get('pressure', 0))
                processed['humidity'].append(record.get('humidity', 0))
                processed['wind_speed'].append(record.get('wind_speed', 0))
                processed['precipitation'].append(record.get('precipitation', 0))
                processed['clouds'].append(record.get('clouds', 0))
                processed['sunshine_hours'].append(record.get('sunshine_hours', 0))

            return {
                'temperature': {
                    'mean': round(sum(processed['temperature']) / len(processed['temperature']), 1),
                    'max': max(processed['temperature']),
                    'min': min(processed['temperature']),
                    'std': round((sum((x - (sum(processed['temperature']) / len(processed['temperature']))) ** 2 for x in processed['temperature']) / len(processed['temperature'])) ** 0.5, 1)
                },
                'pressure': {
                    'mean': round(sum(processed['pressure']) / len(processed['pressure']), 1),
                    'max': max(processed['pressure']),
                    'min': min(processed['pressure']),
                    'std': round((sum((x - (sum(processed['pressure']) / len(processed['pressure']))) ** 2 for x in processed['pressure']) / len(processed['pressure'])) ** 0.5, 1)
                },
                'humidity': {
                    'mean': round(sum(processed['humidity']) / len(processed['humidity']), 1),
                    'max': max(processed['humidity']),
                    'min': min(processed['humidity']),
                    'std': round((sum((x - (sum(processed['humidity']) / len(processed['humidity']))) ** 2 for x in processed['humidity']) / len(processed['humidity'])) ** 0.5, 1)
                },
                'wind_speed': {
                    'mean': round(sum(processed['wind_speed']) / len(processed['wind_speed']), 1),
                    'max': max(processed['wind_speed']),
                    'min': min(processed['wind_speed']),
                    'std': round((sum((x - (sum(processed['wind_speed']) / len(processed['wind_speed']))) ** 2 for x in processed['wind_speed']) / len(processed['wind_speed'])) ** 0.5, 1)
                },
                'precipitation': {
                    'mean': round(sum(processed['precipitation']) / len(processed['precipitation']), 1),
                    'max': max(processed['precipitation']),
                    'min': min(processed['precipitation']),
                    'std': round((sum((x - (sum(processed['precipitation']) / len(processed['precipitation']))) ** 2 for x in processed['precipitation']) / len(processed['precipitation'])) ** 0.5, 1)
                },
                'clouds': {
                    'mean': round(sum(processed['clouds']) / len(processed['clouds']), 1),
                    'max': max(processed['clouds']),
                    'min': min(processed['clouds']),
                    'std': round((sum((x - (sum(processed['clouds']) / len(processed['clouds']))) ** 2 for x in processed['clouds']) / len(processed['clouds'])) ** 0.5, 1)
                },
                'sunshine_hours': {
                    'mean': round(sum(processed['sunshine_hours']) / len(processed['sunshine_hours']), 1),
                    'max': max(processed['sunshine_hours']),
                    'min': min(processed['sunshine_hours']),
                    'std': round((sum((x - (sum(processed['sunshine_hours']) / len(processed['sunshine_hours']))) ** 2 for x in processed['sunshine_hours']) / len(processed['sunshine_hours'])) ** 0.5, 1)
                }
            }
        except KeyError as e:
            raise Exception(f"處理歷史天氣數據失敗: 缺少關鍵數據 {str(e)}")

    @staticmethod
    def get_weather_alert_level(current_weather: Dict) -> tuple:
        """根據天氣數據判斷警報等級"""
        temp = current_weather['temperature']
        humidity = current_weather['humidity']
        wind_speed = current_weather['wind_speed']
        alerts = []
        level = "正常"

        # 溫度警報
        if temp >= 38:
            alerts.append("極端高溫警報")
            level = "危險"
        elif temp >= 35:
            alerts.append("高溫警報")
            level = "警告"
        elif temp <= 0:
            alerts.append("低溫警報")
            level = "警告"

        # 濕度警報
        if humidity >= 85:
            alerts.append("高濕度警報")
            level = max(level, "警告")

        # 強風警報
        if wind_speed >= 20:
            alerts.append("強風警報")
            level = "危險"
        elif wind_speed >= 15:
            alerts.append("大風警報")
            level = max(level, "警告")

        return level, alerts
