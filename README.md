#  Weather App

一款基於 Streamlit 與 OpenWeather 學生方案打造的即時天氣應用，提供當前天氣、未來預報、空氣質量與氣象地圖功能，並透過本地快取與日誌機制優化效能與可維護性。

---

##  專案特色

- **即時天氣**：查詢全球任一城市當前天氣資料  
- **未來預報**：支援每小時與每日 7 天預報  
- **空氣質量**：提供 PM2.5、PM10、AQI 等指標  
- **互動式天氣地圖**：結合 Folium 顯示多種圖層（溫度、降雨、雲圖等）  
- **本地快取**：減少重複 API 呼叫、提升效能  
- **日誌管理**：記錄 API 請求與錯誤，方便除錯與監控  

---

##  技術棧

- **後端框架**：Python 3.10+  
- **前端框架**：Streamlit  
- **地圖套件**：Folium、streamlit-folium  
- **資料處理**：pandas、numpy、python-dateutil、pytz  
- **API 請求**：requests  
- **環境變數管理**：python-dotenv  
- **日誌**：自訂 logger 模組  
- **快取**：SQLite（weather.db） + cache_manager  

---

##  專案結構

```
.weather_app/
﹣
﹣-- .streamlit/
﹣   └﹣ secrets.toml
﹣
﹣-- instance/
﹣   └﹣ weather.db
﹣
﹣-- weather_app/
﹣   |
﹣   ├﹣ data/cache/
﹣   ├﹣ logs/
﹣   ├﹣ src/
﹣   |   |
﹣   |   ├﹣ api/
﹣   |   │   └﹣ weather_api.py
﹣   |   ├﹣ config/
﹣   |   │   └﹣ config.py
﹣   |   ├﹣ ui/
﹣   |   │   ├﹣ current_weather.py
﹣   |   │   ├﹣ forecast.py
﹣   |   │   ├﹣ air_quality.py
﹣   |   │   └﹣ weather_map.py
﹣   |   ├﹣ utils/
﹣   |   │   ├﹣ cache_manager.py
﹣   |   │   ├﹣ data_processor.py
﹣   |   │   └﹣ logger.py
﹣   |   |
﹣   |   └﹣ app.py
﹣   ├﹣ run.py
﹣   └﹣ requirements.txt
﹣
﹣-- README.md
```

---

##  相依套件

```text
requests==2.31.0
python-dotenv==1.0.0
streamlit==1.32.0
pandas==2.2.0
plotly==5.18.0
pillow==10.2.0
numpy==1.26.4
geopy==2.4.1
folium==0.15.1
streamlit-folium==0.18.0
python-dateutil==2.8.2
pytz==2024.1
```

---

##  環境設定

請於 `.streamlit/secrets.toml` 或根目錄 `.env` 中配置：

```toml
OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"
DEFAULT_CITY         = "Taipei"
TEMPERATURE_UNIT     = "metric"   # or "imperial"
LANGUAGE             = "zh_tw"
```

---

##  安裝與啟動

1. **複製專案**  
   ```bash
   git clone https://github.com/your-org/weather_app.git
   cd weather_app
   ```

2. **建立虛擬環境並安裝套件**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r weather_app/requirements.txt
   ```

3. **設定 API 金鑰與預設城市**  

4. **啟動 Streamlit**  
   ```bash
   streamlit run weather_app/run.py
   ```

---

##  使用說明

- **首頁**：顯示預設城市的當前天氣與圖示  
- **當前天氣**：`current_weather`分頁  
- **未來預報**：`每小時`＆`每日`分頁  
- **空氣質量**：AQI、PM2.5、PM10  
- **天氣地圖**：可切換多種地圖圖層  

> UI 模組在 `src/ui/` 目錄，可自由擴充與自定義。

---

##  擴充建議

- **極端氣候警示**（高溫、暴雨、颱風警示）  
- **個人化提醒**（出門前的穿搭、傘具推薦）  
- **節能提示**（根據天氣預測提醒凍暖機使用建議）  
- **資料視覺化**（結合 Plotly 繪製氣溫變化趨勢圖、熱力圖）

---

##  貢獻權

1. Fork 本專案，建立新分支 `feature/xxx`  
2. 提交 PR，加入測試說明或手動測試筆記  
3. 由 maintainers 審核同意後合併

---

##  授權條款

本專案採用 [MIT License](./LICENSE)，歡迎自由使用、修改與分享！

---

> 若有任何疑問或建議，歡迎於 Issues 中提出！預佳使用！

