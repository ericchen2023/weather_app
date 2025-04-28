"""
日誌處理模組：提供應用程式的日誌記錄功能
"""
import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    設置並返回一個日誌記錄器實例
    
    Args:
        name: 日誌記錄器名稱（通常是 __name__）
        
    Returns:
        logging.Logger: 配置好的日誌記錄器實例
    """
    # 創建日誌記錄器
    logger = logging.getLogger(name)
    
    # 如果日誌記錄器已經有處理器，直接返回
    if logger.handlers:
        return logger
        
    # 設置日誌級別
    logger.setLevel(logging.INFO)
    
    # 創建日誌目錄
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # 設置日誌文件名（按日期）
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
    
    # 創建文件處理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 創建控制台處理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 設置日誌格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 將格式器添加到處理器
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 將處理器添加到日誌記錄器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 