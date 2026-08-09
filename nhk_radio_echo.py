import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_latest_play(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    play_locator = (
        By.XPATH,
        "//a[contains(normalize-space(.), 'このページで再生') or contains(normalize-space(.), '再生')]"
        "|//button[contains(normalize-space(.), 'このページで再生') or contains(normalize-space(.), '再生')]",
    )

    play_button = wait.until(EC.element_to_be_clickable(play_locator))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", play_button)
    play_button.click()
    print(f"[{datetime.now()}]再生ボタンをクリックしました。")
    driver.save_screenshot(f"/home/{os.environ.get('PI_USER', 'pi')}/nhk_debug.png")

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


    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get(url)
        click_latest_play(driver, wait)

        print(f"[{datetime.now()}]ブラウザを{keep_seconds // 60}分間維持します。")
        time.sleep(keep_seconds)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
