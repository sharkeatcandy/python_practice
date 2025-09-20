import time
import json
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

BASE_URL = "https://www.iyf.tv/play/NpV0svYALp4"
EXPECTED_EPISODES = 49  # 預期總集數，可以根據需要修改


def handle_challenge_page(driver):
    """處理挑戰頁面的函數"""
    if "/challenge" not in driver.current_url:
        return driver  # 如果不是挑戰頁面，直接返回原driver

    print(f"[INFO] 檢測到挑戰頁面: {driver.current_url}")
    print("=" * 60)
    print("[NOTICE] 需要完成人機驗證")
    print("正在切換到有頭模式以便手動完成驗證...")
    print("=" * 60)

    # 關閉當前無頭瀏覽器
    current_url = driver.current_url
    driver.quit()

    # 重新創建有頭瀏覽器
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # 移除 --headless 參數以顯示瀏覽器

    new_driver = webdriver.Chrome(options=options)
    new_driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    # 導航到挑戰頁面
    new_driver.get(current_url)

    print("[INFO] 請在打開的瀏覽器窗口中完成人機驗證")
    print("[INFO] 完成後，腳本將自動繼續...")

    # 等待用戶完成驗證（檢查URL變化）
    verification_timeout = 300  # 5分鐘超時
    start_time = time.time()

    while time.time() - start_time < verification_timeout:
        current_url = new_driver.current_url
        if "/challenge" not in current_url:
            print(f"[INFO] 驗證完成！當前頁面: {current_url}")
            break
        time.sleep(2)  # 每2秒檢查一次
    else:
        print("[ERROR] 驗證超時，請重新運行腳本")
        new_driver.quit()
        raise TimeoutException("挑戰頁面驗證超時")

    return new_driver


def main():

    # 啟動瀏覽器
    options = Options()
    options.add_argument("--headless=new")  # 無頭模式

    # 添加用户代理以避免反爬虫检测
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # 禁用一些可能影响加载的功能
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # 启用日志记录以捕获网络请求
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=options)

    try:
        # 打開首頁
        print(f"[INFO] 正在載入頁面: {BASE_URL}")
        driver.get(BASE_URL)

        # 檢查並處理挑戰頁面
        driver = handle_challenge_page(driver)

        # 如果處理挑戰頁面後需要重新導航到目標頁面
        if BASE_URL not in driver.current_url:
            print("[INFO] 導航到目標頁面...")
            driver = webdriver.Chrome(options=options)
            driver.get(BASE_URL)
            time.sleep(3)

        # 先檢查頁面是否載入成功
        print(f"[INFO] 頁面標題: {driver.title}")
        print(f"[INFO] 當前URL: {driver.current_url}")  # 等待集數連結載入完成
        wait = WebDriverWait(driver, 20)  # 降低等待時間先測試

        # 檢查頁面結構
        body_elements = driver.find_elements(By.TAG_NAME, "body")
        print(f"[DEBUG] 找到 {len(body_elements)} 個 body 元素")

        # 等待包含集數連結的容器出現
        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".n-media-list"))
            )
            print("[INFO] 媒體列表容器載入完成")
        except TimeoutException:
            print("[ERROR] 找不到媒體列表容器 .n-media-list")
            # 嘗試查找其他可能的選擇器
            all_elements = driver.find_elements(By.TAG_NAME, "*")
            print(f"[DEBUG] 頁面總共有 {len(all_elements)} 個元素")

            # 查找包含 "media" 的類名
            media_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='media']")
            print(f"[DEBUG] 找到 {len(media_elements)} 個包含 'media' 的元素")

            for i, elem in enumerate(media_elements[:5]):  # 只顯示前5個
                print(f"[DEBUG] 媒體元素 {i+1}: {elem.get_attribute('class')}")

            return  # 等待至少有一個集數連結出現
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".n-media-list a.media-button")
            )
        )
        print("[INFO] 集數連結開始載入")

        # 等待直到收集到預期的集數
        print(f"[INFO] 等待收集到預期的 {EXPECTED_EPISODES} 集...")

        def check_episode_count(driver):
            current_count = len(
                driver.find_elements(By.CSS_SELECTOR, ".n-media-list a.media-button")
            )
            if current_count >= EXPECTED_EPISODES:
                print(f"[INFO] 已收集到預期的集數: {current_count}/{EXPECTED_EPISODES}")
                return True
            else:
                print(f"[INFO] 正在載入集數: {current_count}/{EXPECTED_EPISODES}")
                return False

        try:
            # 等待直到達到預期集數
            wait.until(check_episode_count)
            print(f"[SUCCESS] 成功載入所有 {EXPECTED_EPISODES} 集！")
        except TimeoutException:
            # 如果超時，檢查當前收集到的集數
            current_count = len(
                driver.find_elements(By.CSS_SELECTOR, ".n-media-list a.media-button")
            )
            if current_count > 0:
                print(f"[WARN] 載入超時，但已收集到 {current_count} 集，繼續執行...")
                if current_count < EXPECTED_EPISODES:
                    print(
                        f"[WARN] 預期 {EXPECTED_EPISODES} 集，但只找到 {current_count} 集"
                    )
            else:
                raise

    except TimeoutException as e:
        print(f"[WARN] 等待集數連結載入超時: {e}")
        print("[INFO] 繼續執行，嘗試解析現有內容")

    # 解析 HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.select(".n-media-list a.media-button")

    # 依序打開每集
    for a in links:
        title = a.get("title").strip()
        # 清理檔案名稱，移除可能的特殊字符
        safe_title = title.replace("/", "_").replace("\\", "_").replace(":", "_")
        filename = f"{safe_title}.mp4"
        # 檢查檔案是否已存在
        if os.path.exists(filename):
            print(f"[SKIP] 第 {title} 集已存在，跳過下載")
            continue
        href = a.get("href")
        episode_url = BASE_URL + href

        print(f"[INFO] 打開第 {title} 集: {episode_url}")
        driver.get(episode_url)

        # 清除瀏覽器日志以避免獲取上一個影片的 m3u8 連結
        try:
            driver.get_log("performance")  # 清除現有的 performance 日志
            print("[INFO] 已清除瀏覽器日志")
        except Exception as e:
            print(f"[WARN] 清除日志時發生錯誤: {e}")

        # 每集都檢查並處理挑戰頁面
        driver = handle_challenge_page(driver)

        # 如果處理挑戰頁面後需要重新導航到集數頁面
        if episode_url not in driver.current_url:
            print(f"[INFO] 重新導航到第 {title} 集...")
            driver = webdriver.Chrome(options=options)
            driver.get(episode_url)
            time.sleep(2)

        # 等待播放器載入並發出 m3u8 請求
        start_time = time.time()
        m3u8_url = None
        timeout = 10  # 最多等待10秒

        while time.time() - start_time < timeout and m3u8_url is None:
            # 从浏览器日志中查找 m3u8 请求
            logs = driver.get_log("performance")

            for log in logs:
                try:
                    message = json.loads(log["message"])
                    if message["message"]["method"] == "Network.responseReceived":
                        url = message["message"]["params"]["response"]["url"]
                        if ".m3u8" in url:
                            m3u8_url = url
                            break
                except (KeyError, json.JSONDecodeError):
                    continue

            # 如果还没找到，稍微等待一下再检查
            if m3u8_url is None:
                time.sleep(0.5)

        # 暫停網頁影片播放以節省效能和網路流量
        try:
            print("[INFO] 暫停網頁影片播放...")
            # 嘗試多種方式來暫停影片
            pause_scripts = [
                # 通用的 HTML5 video 元素暫停
                "document.querySelectorAll('video').forEach(v => v.pause());",
                # 常見的播放器 API 暫停
                "if(window.player && typeof window.player.pause === 'function') window.player.pause();",
                # JW Player 暫停
                "if(window.jwplayer && jwplayer().pause) jwplayer().pause();",
                # Video.js 暫停
                "if(window.videojs) { try { videojs.getAllPlayers().forEach(p => p.pause()); } catch(e) {} }",
                # 通用的播放器控制
                "document.querySelectorAll('[data-video-player]').forEach(p => { if(p.pause) p.pause(); });",
                # 點擊暫停按鈕的嘗試
                'document.querySelectorAll(\'.pause, .play-pause, [aria-label*="pause"], [title*="pause"]\').forEach(btn => btn.click());',
            ]

            for script in pause_scripts:
                try:
                    driver.execute_script(script)
                except Exception:
                    continue

            print("[INFO] 已執行暫停影片指令")

        except Exception as e:
            print(f"[WARN] 暫停影片時發生錯誤: {e}")

        if m3u8_url:
            cmd = f'ffmpeg -i "{m3u8_url}" -c copy "{filename}"'
            print(f"[INFO] 開始下載第 {title} 集...")
            print(f"[CMD] {cmd}")

            # 在下載前進一步優化瀏覽器效能
            try:
                print("[INFO] 優化瀏覽器效能...")
                # 最小化瀏覽器窗口減少渲染負擔
                driver.minimize_window()

                # 停用頁面中可能消耗資源的功能
                optimization_scripts = [
                    # 停止所有動畫
                    "document.querySelectorAll('*').forEach(el => { el.style.animationPlayState = 'paused'; el.style.animationDuration = '0s'; });",
                    # 隱藏所有影片元素
                    "document.querySelectorAll('video').forEach(v => { v.style.display = 'none'; v.muted = true; });",
                    # 停用自動播放
                    "document.querySelectorAll('video, audio').forEach(media => { media.autoplay = false; media.muted = true; });",
                    # 減少頁面更新頻率
                    "if(window.requestAnimationFrame) window.requestAnimationFrame = function(){};",
                ]

                for script in optimization_scripts:
                    try:
                        driver.execute_script(script)
                    except Exception:
                        continue

            except Exception as e:
                print(f"[WARN] 優化瀏覽器效能時發生錯誤: {e}")

            try:
                # 執行 ffmpeg 命令
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=7200,  # 2小時超時
                    check=False,  # 不要在非零退出代碼時拋出異常
                )

                if result.returncode == 0:
                    print(f"[SUCCESS] 第 {title} 集下載完成！")
                    # 檢查檔案大小
                    if os.path.exists(filename):
                        file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
                        print(f"[INFO] 檔案大小: {file_size:.2f} MB")

                    # 下載完成後進一步清理網頁資源
                    try:
                        print("[INFO] 清理網頁資源...")
                        cleanup_scripts = [
                            # 停止所有影片
                            "document.querySelectorAll('video').forEach(v => { v.pause(); v.src = ''; v.load(); });",
                            # 清除可能的定時器
                            "for(let i = 1; i < 99999; i++) clearTimeout(i);",
                            "for(let i = 1; i < 99999; i++) clearInterval(i);",
                            # 停止所有 WebSocket 連接
                            "if(window.WebSocket) { WebSocket.prototype.send = function(){}; }",
                        ]

                        for script in cleanup_scripts:
                            try:
                                driver.execute_script(script)
                            except Exception:
                                continue

                    except Exception as e:
                        print(f"[WARN] 清理網頁資源時發生錯誤: {e}")

                else:
                    print(f"[ERROR] 第 {title} 集下載失敗！")
                    print(f"[ERROR] 錯誤輸出: {result.stderr}")
                    # 如果下載失敗，刪除可能的部分檔案
                    if os.path.exists(filename):
                        os.remove(filename)
                        print(f"[INFO] 已刪除損壞的檔案: {filename}")

            except subprocess.TimeoutExpired:
                print(f"[ERROR] 第 {title} 集下載超時！")
                # 刪除可能的部分檔案
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"[INFO] 已刪除超時的檔案: {filename}")
            except (subprocess.SubprocessError, OSError) as e:
                print(f"[ERROR] 執行命令時發生錯誤: {e}")
        else:
            print(f"[WARN] 第 {title} 集沒抓到 m3u8")

    driver.quit()


if __name__ == "__main__":
    main()
