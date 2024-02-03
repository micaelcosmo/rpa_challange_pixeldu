from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class URLAccess:
    def __init__(self, url):
        self.url = url
        self.service = Service(ChromeDriverManager().install())
        self.options = self.config_options()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.access_url()

    @property
    def driver_browser(self):
        return self.driver
        
    def config_options(self):
        options = Options()
        options.add_argument("--ignore-certificate-errors") # Ignore certificate errors
        options.add_argument("--ignore-ssl-errors") # Ignore SSL errors
        options.add_argument("--disable-blink-features=AutomationControlled") # Remove "automated process.." flag
        # options.add_argument("--headless") # Run Chrome in headless mode
        return options
    
    def access_url(self):
        # Open the browser and access the URL
        self.driver.get(self.url)

    def close_browser(self):
        # Close the browser
        self.driver.quit()
