"""
啟動天氣應用程序的入口點
"""
import os
import sys
import subprocess

if __name__ == "__main__":
    try:
        # 獲取當前腳本的目錄路徑
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 將 src 目錄加入 Python 路徑
        sys.path.append(os.path.join(current_dir, "src"))
        
        # 使用絕對路徑執行 Streamlit 應用程式
        app_path = os.path.join(current_dir, "src", "app.py")
        
        # 確保 app.py 存在
        if not os.path.exists(app_path):
            raise FileNotFoundError(f"找不到應用程式文件：{app_path}")
            
        # 設置環境變數
        env = os.environ.copy()
        env["PYTHONPATH"] = current_dir
        
        # 使用 subprocess 執行 Streamlit
        print(f"正在啟動應用程式：{app_path}")
        process = subprocess.Popen(
            ["streamlit", "run", app_path],
            env=env,
            text=True,
            encoding='utf-8'
        )
        process.wait()
        
    except FileNotFoundError as e:
        print(f"錯誤：{str(e)}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"啟動應用程式時發生錯誤：{str(e)}")
        sys.exit(1)
    except (SystemExit, KeyboardInterrupt):
        print("\n應用程式已終止")
        if 'process' in locals():
            process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"發生未預期的錯誤：{str(e)}", file=sys.stderr)
        sys.exit(1)
