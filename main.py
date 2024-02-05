from logger import AppLogger
from engine.web_scraping import WebScraping


NEWS_URL= "https://apnews.com/" # URL to scrape
SCREENSHOT_NAME = "apnews.png"  # Screenshot file name
EXCEL_NAME = "apnews.xlsx"      # Excel file name
SEARCH_WORLD = "money"          # Search term
MAX_ELEMENTS_TO_PROCESS = 10    # Max elements to process | -1 to process all
MAX_PAGES_TO_PROCESS = 1        # Max pages to process | -1 to process all

logger = AppLogger().logger

def minimal_task():
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
        search=SEARCH_WORLD, 
        filename_excel=EXCEL_NAME, 
        filename_screenshot=SCREENSHOT_NAME, 
        max_elements_by_page=MAX_ELEMENTS_TO_PROCESS,
        max_pages=MAX_PAGES_TO_PROCESS)
    logger.info("Ending minimal task")


if __name__ == "__main__":
    minimal_task()
