"""
快取管理模組
"""
import os
import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from src.config.config import CACHE_DIR, CACHE_DURATION

class CacheManager:
    def __init__(self):
        """初始化快取管理器"""
        self.cache_dir = CACHE_DIR
        self.cache_duration = CACHE_DURATION
        
        # 確保快取目錄存在
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _get_cache_path(self, key: str) -> str:
        """獲取快取文件路徑"""
        return os.path.join(self.cache_dir, f"{key}.json")
        
    def get(self, key: str) -> Optional[Any]:
        """從快取中獲取數據"""
        cache_path = self._get_cache_path(key)
        
        try:
            if os.path.exists(cache_path):
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                # 檢查快取是否過期
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cache_time < timedelta(seconds=self.cache_duration):
                    return cache_data['data']
        except Exception as e:
            print(f"讀取快取失敗: {str(e)}")
        
        return None
        
    def set(self, key: str, data: Any) -> None:
        """將數據存入快取"""
        cache_path = self._get_cache_path(key)
        
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"寫入快取失敗: {str(e)}")
    
    def clear(self) -> None:
        """清理所有快取"""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
        except Exception as e:
            print(f"清理快取失敗: {str(e)}")

    def clear_expired(self):
        """清除所有過期的快取"""
        for file in os.listdir(self.cache_dir):
            if not file.endswith('.json'):
                continue
                
            cache_path = os.path.join(self.cache_dir, file)
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cache_time > timedelta(seconds=self.cache_duration):
                    os.remove(cache_path)
            except Exception as e:
                print(f"清理過期快取失敗: {str(e)}")
                continue 