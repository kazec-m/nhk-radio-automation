import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_latest_play(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    play_locator = (
        By.XPATH,
        (
            "//a[contains(normalize-space(.), 'このページで再生') or contains(normalize-space(.), '再生')]"
            "|//button[contains(normalize-space(.), 'このページで再生') or contains(normalize-space(.), '再生')]"
        ),
    )

    play_button = wait.until(EC.element_to_be_clickable(play_locator))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", play_button)
    try:
        label = driver.execute_script(r"""
            const button = arguments[0];
            const item = button.closest('article, li, section');
            return [button.getAttribute('aria-label'), button.getAttribute('title'),
                    button.innerText, item?.innerText]
                .filter(Boolean).join(' ').replace(/\s+/g, ' ').trim().slice(0, 180);
        """, play_button)
        print(f"[{datetime.now()}]選択した再生項目: {label or '情報なし'}", flush=True)
    except WebDriverException:
        print(f"[{datetime.now()}]再生項目の情報を取得できませんでした。", flush=True)
    play_button.click()
    print(f"[{datetime.now()}]再生ボタンをクリックしました。")
    driver.save_screenshot(f"/home/{os.environ.get('PI_USER', 'pi')}/nhk_debug.png")

def log_playback_progress(driver: webdriver.Chrome) -> None:
    try:
        media = driver.execute_script("""
            const items = [...document.querySelectorAll('audio, video')];
            return items.find(item => !item.paused) || items[0] || null;
        """)
        if media is None:
            print(f"[{datetime.now()}]音声要素が見つからず、再生位置は確認できません。", flush=True)
            return
        start = driver.execute_script("return arguments[0].currentTime", media)
        time.sleep(3)
        end = driver.execute_script("return arguments[0].currentTime", media)
        print(f"[{datetime.now()}]再生位置: {start:.1f}秒 → {end:.1f}秒", flush=True)
    except WebDriverException:
        print(f"[{datetime.now()}]再生位置を取得できませんでした。", flush=True)


def main() -> None:
    url = "https://www.nhk.or.jp/radio/ondemand/detail.html?p=368315KKP8_01"
    keep_seconds = 60 * 25

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-session-crashed-bubble")
    options.add_argument("--no-first-run")
    options.add_argument("--ozone-platform=x11")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get(url)
        click_latest_play(driver, wait)

        print(f"[{datetime.now()}]ブラウザを{keep_seconds // 60}分間維持します。")
        deadline = time.monotonic() + keep_seconds
        time.sleep(5)
        log_playback_progress(driver)
        time.sleep(max(0, deadline - time.monotonic()))
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
