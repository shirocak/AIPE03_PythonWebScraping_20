import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def setup_driver():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)


def scrape_manga(url, output_dir="downloaded_manga"):

    os.makedirs(output_dir, exist_ok=True)
    print(f"圖片將儲存至：{os.path.abspath(output_dir)}")

    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    total_image_count = 0

    try:
        driver.get(url)
        print("Page Title:", driver.title)

        driver.find_element(By.CSS_SELECTOR, "button.open-viewer.book-begin.ga").click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.PARTIAL_LINK_TEXT, "すぐに読む").click()

        while True:
            for img in driver.find_elements(By.CSS_SELECTOR, "div.page_image img.image"):
                if img.is_displayed():
                    file_path = os.path.join(output_dir, f"manga_page_{total_image_count:04d}.png")
                    img.screenshot(file_path)
                    print(f"已儲存：{file_path}")
                    total_image_count += 1

            try:
                next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.flip.flip-left")))
                next_page.click()
                time.sleep(2)
            except TimeoutException:
                print(f"已到最後一頁，共擷取 {total_image_count} 張圖片。")
                break

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_manga("https://www.mangaz.com/book/detail/157901")