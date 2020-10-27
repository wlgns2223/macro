from bs4 import BeautifulSoup
from selenium import webdriver
import requests as req


class Validator:

    URL = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"

    def __init__(self, id='', password=''):
        self.id = id
        self.password = password
        self.chromedriver = None

        self.init_selenium()

    def init_selenium(self):
        driver_path = './chromedriver'
        driver_option = webdriver.ChromeOptions()
        driver_option.add_argument('headless')

        self.chromedriver = webdriver.Chrome(
            executable_path=driver_path, chrome_options=driver_option)

    def __open_naver(self):
        self.chromedriver.get(self.__class__.URL)
