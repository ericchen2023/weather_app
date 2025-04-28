"""
天氣 API 請求模組
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from ..config.config import API_KEY, ENDPOINTS, DEFAULT_UNITS, DEFAULT_LANG
from ..utils.cache_manager import CacheManager
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
cache = CacheManager()

class WeatherAPI:
    """處理所有天氣相關的 API 請求"""
    
    def __init__(self):
        self.api_key = API_KEY
        self.endpoints = ENDPOINTS
        self.units = DEFAULT_UNITS
        self.lang = DEFAULT_LANG

    def _make_request(self, endpoint: str, params: Dict[str, Any], expect_list: bool = False) -> Union[Dict, List]:
        """發送 API 請求並返回結果
        
        Args:
            endpoint: API 端點
            params: 請求參數
            expect_list: 是否預期返回列表類型的響應
        """
        # 確保所有必要的參數都存在
        base_params = {
            "appid": self.api_key,
            "units": self.units,
            "lang": self.lang
        }
        
        # 合併基本參數和特定請求參數
        final_params = {**base_params, **params}
        
        # 記錄請求詳情（隱藏 API 金鑰）
        debug_params = {**final_params}
        debug_params["appid"] = "***"
        logger.debug(f"發送請求到端點: {endpoint}")
        logger.debug(f"請求參數: {debug_params}")
        
        try:
            response = requests.get(endpoint, params=final_params)
            
            # 記錄響應狀態和 URL（隱藏 API 金鑰）
            debug_url = response.url.replace(self.api_key, "***")
            logger.debug(f"完整請求 URL: {debug_url}")
            logger.debug(f"響應狀態碼: {response.status_code}")
            
            # 嘗試解析響應內容
            try:
                response_json = response.json()
                logger.debug(f"API 響應內容: {response_json}")
            except ValueError as e:
                logger.error(f"無法解析 JSON 響應: {response.text}")
                raise
            
            # 檢查響應狀態
            response.raise_for_status()
            
            # 驗證響應數據格式
            if expect_list:
                if not isinstance(response_json, list):
                    raise ValueError(f"預期響應為列表類型，實際收到: {type(response_json)}")
            elif not isinstance(response_json, dict):
                if isinstance(response_json, list):
                    # 如果收到列表但預期字典，將列表包裝成字典
                    response_json = {"list": response_json}
                else:
                    raise ValueError(f"預期響應為字典類型，實際收到: {type(response_json)}")
            
            return response_json
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP 錯誤 {e.response.status_code}: {str(e)}")
            logger.error(f"錯誤響應內容: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"請求錯誤: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"未預期的錯誤: {str(e)}", exc_info=True)
            raise

    def get_current_weather(self, lat: float, lon: float) -> Dict:
        """獲取當前天氣數據"""
        cache_key = f"current_weather_{lat}_{lon}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        params = {"lat": lat, "lon": lon}
        data = self._make_request(self.endpoints["current_weather"], params)
        cache.set(cache_key, data)
        return data

    def get_hourly_forecast(self, lat: float, lon: float) -> List[Dict]:
        """獲取每小時天氣預報（5天/3小時間隔）"""
        cache_key = f"hourly_forecast_{lat}_{lon}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'lang': 'en'  # 使用英文顯示國家名稱
        }
        data = self._make_request(self.endpoints["forecast"], params)
        hourly_data = data.get("list", [])
        cache.set(cache_key, hourly_data)
        return hourly_data

    def get_daily_forecast(self, lat: float, lon: float, days: int = 7) -> List[Dict]:
        """獲取每日天氣預報（最多16天）"""
        if days > 16:
            days = 16

        cache_key = f"daily_forecast_{lat}_{lon}_{days}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        params = {
            "lat": lat,
            "lon": lon,
            "cnt": days
        }
        data = self._make_request(self.endpoints["forecast_daily"], params)
        daily_data = data.get("list", [])
        cache.set(cache_key, daily_data)
        return daily_data

    def get_air_pollution(self, lat: float, lon: float) -> Dict:
        """獲取空氣品質數據"""
        cache_key = f"air_pollution_{lat}_{lon}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        params = {"lat": lat, "lon": lon}
        data = self._make_request(self.endpoints["air_pollution"], params)
        cache.set(cache_key, data)
        return data

    def get_location_by_name(self, city_name: str, country_code: Optional[str] = None) -> List[Dict]:
        """通過城市名稱獲取地理位置信息"""
        query = f"{city_name}"
        if country_code:
            query = f"{city_name},{country_code}"

        cache_key = f"geocoding_{query}_en"  # 加入語言標記
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        params = {
            "q": query,
            "limit": 5
        }
        
        # 指定預期返回列表類型的響應
        data = self._make_request(self.endpoints["geocoding"], params, expect_list=True)
        cache.set(cache_key, data)
        return data

    def get_monthly_forecast(self, lat: float, lon: float) -> List[Dict]:
        """獲取30天天氣預報（需要 Pro API）"""
        cache_key = f"monthly_forecast_{lat}_{lon}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        try:
            # 首先嘗試使用 Pro API
            params = {
                "lat": lat,
                "lon": lon,
                "cnt": 30  # 獲取30天的預報
            }
            data = self._make_request(self.endpoints["forecast_climate"], params)
            forecast_data = data.get("list", [])
            cache.set(cache_key, forecast_data)
            return forecast_data
        except Exception as e:
            # 如果 Pro API 失敗，回退到免費版的每日預報
            logger.warning(f"使用 Pro API 獲取30天預報失敗: {str(e)}，回退到免費版16天預報")
            params = {
                "lat": lat,
                "lon": lon,
                "cnt": 16  # 免費版最多支援16天
            }
            data = self._make_request(self.endpoints["forecast_daily"], params)
            forecast_data = data.get("list", [])
            cache.set(cache_key, forecast_data)
            return forecast_data
