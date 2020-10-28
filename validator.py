from bs4 import BeautifulSoup
from selenium import webdriver
import requests as req
from fake_useragent import UserAgent


class Validator:

    URL = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"

    def __init__(self, id='', password=''):
        self.id = id
        self.password = password
        self.chromedriver = None

        self.__init_selenium()

    def __set_driver_obtions(self):

        ua = UserAgent()
        ua = ua.random

        driver_option = webdriver.ChromeOptions()

        # driver_option.add_argument('headless')
        driver_option.add_argument(f'user-agent={ua}')

        return driver_option

    def __init_selenium(self):
        driver_path = './chromedriver'
        driver_option = self.__set_driver_obtions()
        self.chromedriver = webdriver.Chrome(
            executable_path=driver_path, chrome_options=driver_option)

    def open_naver(self):
        self.chromedriver.get(self.__class__.URL)


if __name__ == '__main__':

    from validator import Validator

    v = Validator(id='hello', password='world')
    v.init_selenium()
    v.open_naver()
