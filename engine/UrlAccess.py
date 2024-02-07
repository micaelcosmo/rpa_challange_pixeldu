from logger import AppLogger

from RPA.core.webdriver import download, start, webdriver


class UrlAccess:
    """
    Class representing URL access and interaction.

    Args:
        url (str): The URL to be accessed.
        filename_screenshot (str): The filename for saving a screenshot (optional).

    Attributes:
        driver: The web driver instance.
        list_news: A list to store news items.
        logger: The logger instance.

    Methods:
        set_chrome_options: Sets the Chrome options for the web driver.
        set_webdriver: Sets the web driver based on the specified browser.
        open_url: Opens the specified URL in the web driver.
        driver_quit: Quits the web driver.
    """

    def __init__(self, url:str='', filename_screenshot:str=''):
        self.driver = None
        self.list_news = []
        self.logger = AppLogger().logger
        self.set_webdriver()
        self.set_chrome_options()
        self.open_url(url=url, screenshot=filename_screenshot)
        
    @property
    def driver_browser(self):
        return self.driver
    
    def set_chrome_options(self):
        """
        Sets the Chrome options for the web driver.

        Returns:
            options: The Chrome options object.
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-web-security')
        options.add_argument("--start-maximized")
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument("--log-level=3") 
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--disable-blink-features=AutomationControlled')
        return options

    def set_webdriver(self, browser:str="Chrome"):
        """
        Sets the web driver based on the specified browser.

        Args:
            browser (str): The browser to use for the web driver (default is "Chrome").
        """
        options = self.set_chrome_options()
        executable_driver_path = download(browser)
        self.logger.warning("Using downloaded driver: %s" % executable_driver_path)
        self.driver = start(browser=browser,  options=options)
       
    def open_url(self, url:str, screenshot:str=None):
        """
        Opens the specified URL in the web driver.

        Args:
            url (str): The URL to be opened.
            screenshot (str): The filename for saving a screenshot (optional).
        """
        self.driver.get(url)
        if screenshot:
            self.driver.get_screenshot_as_file(screenshot)

    def driver_quit(self):
        """
        Quits the web driver.
        """
        if self.driver:
            self.driver.quit()
