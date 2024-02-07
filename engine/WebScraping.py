import re
import datetime
from dateutil import parser
from logger import AppLogger
from dataclasses import dataclass
from engine.UrlAccess import UrlAccess

import nltk
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


nltk.download('punkt')


@dataclass
class News:
    title: str
    date: str
    description: str
    picture: str
    number_of_prhases: int
    is_financial: bool


class WebScraping:
    """
    A class for performing web scraping tasks.

    Args:
        url (str): The URL of the website to scrape.
        search (str): The search term to use for scraping.
        filename_excel (str): The filename to save the scraped data in Excel format.
        filename_screenshot (str): The filename to save the screenshots.
        max_elements_by_page (int): The maximum number of elements to scrape per page, if value is equal -1 will process all.
        max_pages (int): The maximum number of pages to scrape, if value is equal -1 will process all.

    Attributes:
        access (URLAccess): An instance of the URLAccess class for accessing the website.
        logger (Logger): An instance of the AppLogger class for logging.
        search_word (str): The search term.
        filename_excel (str): The filename for saving the scraped data.
        max_elements (int): The maximum number of elements to scrape per page.
        max_pages (int): The maximum number of pages to scrape.
        driver (WebDriver): The web driver instance.
        list_news (list): A list to store the scraped news.

    Methods:
        _run(): Runs the web scraping process.
        store_news(): Stores the scraped news.
        _is_a_finance_news(text): Checks if the given text is related to finance news.
        _save_picture_to_file(filename, picture): Saves the picture to a file.
        to_snake_case(content_text): Converts the given text to snake case.
        search(): Performs the search operation.
        news_to_excel(): Saves the scraped news to an Excel file.
        search_for_pagination(): Checks if the search has pagination.
        next_page(): Moves to the next page.
    """
    def __init__(self, url:str='', search:str='', filename_excel:str='', filename_screenshot:str='', max_elements_by_page:int=-1, max_pages:int=1, months_range:int=1):
        try:
            self.access = UrlAccess(url=url, filename_screenshot=filename_screenshot)
            self.logger = AppLogger().logger
            self.search_word = search
            self.filename_excel = filename_excel
            self.max_elements = max_elements_by_page
            self.max_pages = 9999999 if max_pages == -1 else max_pages
            self.months_range = months_range
            self.driver = self.access.driver_browser
            self.list_news = []
            self._run()
        finally:
            self.access.driver_quit()

    def _run(self):
        """
        Runs the web scraping process.
        """
        self.logger.info("Running web scraping process")
        self.search()
        for i in range(self.max_pages):
            self.logger.info(f"Processing page {i+1}")
            if self.search_for_pagination():
                self.logger.info("This search has pagination")
                _ = self.store_news()
                self.next_page()
            else:
                self.logger.info("This search does not have pagination")
                _ = self.store_news()
                break
        self.news_to_excel()
        self.logger.info("Web scraping process finished")

    def store_news(self):
        """
        Stores the scraped news.
        """
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
                number_of_prhases = len(nltk.sent_tokenize(description))
            except:
                description = 'No description found'
                number_of_prhases = 0
            try:
                date = element.find_element(By.CLASS_NAME, "PagePromo-date").text
            except:
                date = 'No date found'
                self.logger.warning(f"Date not found for news {title}, skipping")
                continue
            try:
                picture = element.find_element(By.CLASS_NAME, "Image")
                picture_filename = self._save_picture_to_file(element.text.split(' ')[0]+'.png', picture)
            except:
                picture_filename = 'No picture found'

            news = News(
                title=title, 
                date=date, 
                description=description, 
                picture=picture_filename, 
                number_of_prhases=number_of_prhases, 
                is_financial=self._is_a_finance_news(description)
                )
            may_continue = False
            months_range = self.months_range if self.months_range != 0 and self.months_range != 1 else 1
            may_continue = self.verify_month(date, months_range)
            if may_continue == True:
                self.list_news.append(news)
        return True

    def verify_month(self, date, months_range):
        for month in range(months_range):
            if self._is_equal_current_month(date, month) == True:
                may_continue = True
                break
            else:
                may_continue = False
        return may_continue

    def _is_a_finance_news(self, text):
        """
        Checks if the given text is related to finance news.

        Args:
            text (str): The text to check.

        Returns:
            bool: True if the text is related to finance news, False otherwise.
        """
        currency_symbols = ["$", "€", "£", "¥", "USD", "EUR", "GBP", "JPY"]
        pattern = re.compile(fr'\b({"|".join(map(re.escape, currency_symbols))})?\s?\d+(\d+)?\b')
        return bool(pattern.search(text))
    
    def _save_picture_to_file(self, filename, picture):
        """
        Saves the picture to a file.

        Args:
            filename (str): The filename to save the picture.
            picture (WebElement): The picture element.

        Returns:
            str: The path of the saved picture file.
        """
        if picture is None:
            return 'No picture found'
        path = f'data/{filename}'
        picture.screenshot(path)
        return path

    def to_snake_case(self, content_text:str):
        """
        Converts the given text to snake case.

        Args:
            content_text (str): The text to convert.

        Returns:
            str: The converted text in snake case.
        """
        return '_'.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', content_text.replace('-', ' ').replace("'", "").replace("`s", ""))).split()).lower()

    def search(self):
        """
        Performs the search operation.
        """
        search_button = self.driver.find_element(By.CLASS_NAME, "SearchOverlay-search-button")
        search_button.click()
        self.driver.implicitly_wait(5)
        search_box = self.driver.find_element(By.CLASS_NAME, "SearchOverlay-search-input")
        search_box.send_keys(self.search_word)
        search_box.submit()
        self.driver.implicitly_wait(5)
        
    def news_to_excel(self):
        """
        Saves the scraped news to an Excel file.
        """
        df = pd.DataFrame([news.__dict__ for news in self.list_news])
        df.to_excel(self.filename_excel, index=False)
        self.logger.info(f"News saved to {self.filename_excel}")

    def search_for_pagination(self):
        """
        Checks if the search has pagination.

        Returns:
            bool: True if the search has pagination, False otherwise.
        """
        try:
            self.driver.find_element(By.CLASS_NAME, "Pagination")
            return True
        except Exception as e:
            self.logger.error(f"This search does not have pagination")
            return False

    def next_page(self):
        """
        Moves to the next page.
        """
        self.logger.info("Searching for next page")
        try:
            next_page_link = self.driver.find_element(By.CSS_SELECTOR, 'div.Pagination-nextPage a')
            next_page_link.click()
        except Exception as e:
            self.logger.error(f"Error clicking next page: {e}, maybe it does not work for this page")

    @staticmethod
    def _subtract_month(date, months):
        """
        Subtract the specified number of months from the given date.

        Args:
            date (datetime.date): The date to subtract months from.
            months (int): The number of months to subtract.

        Returns:
            datetime.date: The resulting date after subtracting the months.
        """
        month = date.month - months
        year = date.year
        if month <= 0:
            year -= 1
            month += 12
        return date.replace(year=year, month=month)

    def _is_equal_current_month(self, date_str, months_range=1):
        """
        Checks if the given date is less than or equal to the current month.

        Args:
            date_str (str): The date string to compare.

        Returns:
            bool: True if the given date is less than or equal to the current month, False otherwise.
        """
        current_date = datetime.datetime.now()
        if months_range > 0:
            current_date = self._subtract_month(current_date, months_range)
        try:
            given_date = parser.parse(date_str, fuzzy_with_tokens=True)[0]
        except parser.ParserError:
            self.logger.warning(f"Invalid date format: {date_str}")
            self.logger.warning(f"Skipping date comparison")
            return True
        result = given_date.month == current_date.month and given_date.year == current_date.year
        if result == False:
            self.logger.info(f"News date {date_str} is not in the current month'{current_date}'")
        return result
