from logger import AppLogger

from RPA.core.webdriver import download, start, webdriver


class URLAccess:
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
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-web-security')
        options.add_argument("--start-maximized")
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument("--log-level=3") 
        return options

    def set_webdriver(self, browser:str="Chrome"):
        options = self.set_chrome_options()
        executable_driver_path = download(browser)
        self.logger.warning("Using downloaded driver: %s" % executable_driver_path)
        self.driver = start(browser=browser,  options=options)
       
    def open_url(self, url:str, screenshot:str=None):
        self.driver.get(url)
        if screenshot:
            self.driver.get_screenshot_as_file(screenshot)

    def driver_quit(self):
        if self.driver:
            self.driver.quit()
