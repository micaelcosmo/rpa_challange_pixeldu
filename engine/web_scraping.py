from time import sleep
from engine.base_access import URLAccess
from selenium.webdriver.common.by import By

class WebScraping:
    def __init__(self, url:str=''):
        self.access = URLAccess(url)
        self.driver = self.access.driver_browser
        self.navigate_to_search()
        # self.access.close_browser()

    def navigate_to_search(self):
        self.select_search_box()
        self.submit_to_search()
        sleep(20)

    def select_search_box(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.CLASS_NAME, "SearchOverlay-search-button").click()

    def submit_to_search(self):
        self.driver.implicitly_wait(10)
        search_input = self.driver.find_element(By.CLASS_NAME, "SearchOverlay-search-input")
        search_input.send_keys("covid")
        serach_submit = self.driver.find_element(By.CLASS_NAME, "SearchOverlay-search-submit")
        serach_submit.click()
