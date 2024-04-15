from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import InsecureRequestWarning
from dotenv import load_dotenv
import warnings
import time
import re
import os


load_dotenv()


class NewsScraper:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "default_url_if_not_set")
        options = Options()
        options.page_load_strategy = 'eager'
        options.headless = True
        self.driver = webdriver.Chrome(service=Service("/Users/lj22pbvc/Code/python/flask/rpa/chromedriver-mac-arm64/chromedriver"), options=options)
        self.driver.set_page_load_timeout(30)

    def open_website(self):
        self.driver.get(self.base_url)
        try:
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
            WebDriverWait(self.driver, 10).until(element_present)
        except TimeoutException:
            print("Failed to load the website. The page might have loaded too slowly or the DOM structure might have changed.")

    def search_news(self):
        try:
            search_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='search-icon']")))
            search_icon.click()

            search_phrase = os.getenv("SEARCH_PHRASE", "default_search_if_not_set")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
            search_box.send_keys(search_phrase)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
        except TimeoutException as e:
            print(f"Error during search: {e}")
            self.driver.quit()

    def collect_news_data(self):
        news_elements = self.driver.find_elements(By.CSS_SELECTOR, "selector_for_news_items")
        news_data = []
        for element in news_elements:
            title = element.find_element(By.CSS_SELECTOR, "title_selector").text
            date = element.find_element(By.CSS_SELECTOR, "date_selector").text
            description = element.find_element(By.CSS_SELECTOR, "desc_selector").text
            image_url = element.find_element(By.CSS_SELECTOR, "img_selector").get_attribute("src")
            money_present = bool(re.search(r'\$\d+', title + description))
            news_data.append((title, date, description, image_url, money_present))

        return news_data
    
    def close_browser(self):
        self.driver.quit()

if __name__ == "__main__":
    warnings.simplefilter('ignore', InsecureRequestWarning)
    scraper = NewsScraper()
    scraper.open_website()
    scraper.search_news()
    news_data = scraper.collect_news_data()
    scraper.close_browser()
    print(news_data)