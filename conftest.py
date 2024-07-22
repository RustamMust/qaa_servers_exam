import os
from selenium import webdriver
import pytest
from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv('BASE_URL')
BASE_URL_2 = os.getenv('BASE_URL_2')
LOCAL_BROWSER = False


@pytest.fixture(scope='session')
def open_browser():
    if LOCAL_BROWSER:
        chrome_browser = webdriver.Chrome()
        chrome_browser.implicitly_wait(10)
        chrome_browser.get(BASE_URL)
        yield chrome_browser
        chrome_browser.quit()

    else:
        options = webdriver.ChromeOptions()
        server = os.getenv('REMOTE_BROWSER')
        driver = webdriver.Remote(command_executor=server, options=options)
        driver.implicitly_wait(10)
        driver.get(BASE_URL_2)
        yield driver
        driver.quit()





