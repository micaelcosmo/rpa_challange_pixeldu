from logger import AppLogger
from engine.WebScraping import WebScraping
from robocorp.tasks import task

NEWS_URL= "https://apnews.com/" # URL to scrape
SCREENSHOT_NAME = "apnews.png"  # Screenshot file name
EXCEL_NAME = "apnews.xlsx"      # Excel file name
MAX_ELEMENTS_TO_PROCESS = -1    # Max elements to process | -1 to process all
MAX_PAGES_TO_PROCESS = 10       # Max pages to process | -1 to process all
logger = AppLogger().logger

class Tasks:

    def rpa_challenge(months_range:int=0, search_phrase:str='money') -> None:
        """
        Performs a minimal task of web scraping news articles from a given URL,
        filtering by a specific search term, and saving the results to an Excel file
        and taking a screenshot of the webpage.

        Args:
            None

        Returns:
            None
        """
        logger.info("Starting minimal task")
        WebScraping(
            url=NEWS_URL, 
            search=search_phrase, 
            filename_excel=EXCEL_NAME, 
            filename_screenshot=SCREENSHOT_NAME, 
            max_elements_by_page=MAX_ELEMENTS_TO_PROCESS,
            max_pages=MAX_PAGES_TO_PROCESS,
            months_range=months_range)
        logger.info("Ending minimal task")
