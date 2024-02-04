from logger import AppLogger
from engine.web_scraping import WebScraping

# URL of the news website
NEWS_URL= "https://apnews.com/"
SCREENSHOT_NAME = "apnews.png"
EXCEL_NAME = "apnews.xlsx"
SEARCH_WORLD = "money"
MAX_ELEMENTS_TO_PROCESS = 5 

logger = AppLogger().logger

def minimal_task():
    logger.info("Starting minimal task")
    WebScraping(
        url=NEWS_URL, 
        search=SEARCH_WORLD, 
        filename_excel=EXCEL_NAME, 
        filename_screenshot=SCREENSHOT_NAME, 
        max_elements=MAX_ELEMENTS_TO_PROCESS)
    logger.info("Ending minimal task")


if __name__ == "__main__":
    minimal_task()