import re
from logger import AppLogger
from dataclasses import dataclass
from engine.base_access import URLAccess

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class News:
    title: str
    date: str
    description: str
    picture: str
    number_of_prhases: int
    is_financial: bool


class WebScraping:
    def __init__(self, url:str='', search:str='', filename_excel:str='', filename_screenshot:str='', max_elements:int=10):
        try:
            self.access = URLAccess(url=url, filename_screenshot=filename_screenshot)
            self.logger = AppLogger().logger
            self.search_word = search
            self.filename_excel = filename_excel
            self.max_elements = max_elements
            self.driver = self.access.driver_browser
            self.list_news = []
            self._run()
        finally:
            self.access.driver_quit()

    def _run(self):
        self.logger.info("Running web scraping process")
        self.search()
        self.store_news()
        self.news_to_excel()
        self.logger.info("Web scraping process finished")

    def store_news(self):
        self.logger.info("Storing news")
        results = WebDriverWait(self.driver, 0.1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "SearchResultsModule-results"))
        )
        elements = results.find_elements(By.CLASS_NAME, "PageList-items-item")
        self.logger.info(f"Found {len(elements)} news")

        for element in elements[:self.max_elements]:
            try:
                title = element.find_element(By.CLASS_NAME, "PagePromo-title").text
            except:
                title = 'No title found'
            
            self.logger.info(f"Starting processing news: {title}")
            try:
                description_div = element.find_element(By.CLASS_NAME, "PagePromo-description")
                description = description_div.find_element(By.CLASS_NAME, "PagePromoContentIcons-text").text
                number_of_prhases = description.count(".")
            except:
                description = 'No description found'
                number_of_prhases = 0
            try:
                date = element.find_element(By.CLASS_NAME, "PagePromo-date").text
            except:
                date = 'No date found'
            try:
                picture = element.find_element(By.CLASS_NAME, "Image")
                picture_filename = self.save_picture_to_file(element.text.split(' ')[0]+'.png', picture)
            except:
                picture_filename = 'No picture found'

            news = News(
                title=title, 
                date=date, 
                description=description, 
                picture=picture_filename, 
                number_of_prhases=number_of_prhases, 
                is_financial=self.is_a_finance_news(description)
                )
            self.list_news.append(news)

    def is_a_finance_news(self, text):
        currency_symbols = ["$", "€", "£", "¥", "USD", "EUR", "GBP", "JPY"]
        pattern = re.compile(fr'\b({"|".join(map(re.escape, currency_symbols))})?\s?\d+(\d+)?\b')
        return bool(pattern.search(text))
    
    def save_picture_to_file(self, filename, picture):
        if picture is None:
            return 'No picture found'
        path = f'data/{filename}'
        picture.screenshot(path)
        return path

    def to_snake_case(self, content_text:str):
        return '_'.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', content_text.replace('-', ' ').replace("'", "").replace("`s", ""))).split()).lower()

    def search(self):
        search_button = self.driver.find_element(By.CLASS_NAME, "SearchOverlay-search-button")
        search_button.click()
        self.driver.implicitly_wait(5)
        search_box = self.driver.find_element(By.CLASS_NAME, "SearchOverlay-search-input")
        search_box.send_keys(self.search_word)
        search_box.submit()
        self.driver.implicitly_wait(5)
        
    def news_to_excel(self):
        df = pd.DataFrame([news.__dict__ for news in self.list_news])
        df.to_excel(self.filename_excel, index=False)
        self.logger.info(f"News saved to {self.filename_excel}")
