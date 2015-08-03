__author__ = 'Olga'
import os
import ConfigParser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def start_driver():
    global url
    global implicit_timeout
    global wait_timeout
    global username
    global password
    global driver
    config = ConfigParser.RawConfigParser()
    path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    config.read(os.path.join(path, 'settings.properties'))
    chromedriver = config.get('BrowserSection', 'chromedriver')
    os.environ["webdriver.chrome.driver"] = chromedriver
    url = config.get('urlSection', 'url')
    implicit_timeout = config.get('driverSection', 'implicit.timeout')
    wait_timeout = int(config.get('driverSection', 'wait.timeout'))
    username = config.get('dataSection', 'username')
    password = config.get('dataSection', 'password')
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(implicit_timeout)
    return driver, wait_timeout, implicit_timeout, url, username, password


def is_element_present(wdriver, by, locator, timeout=10):
    try:
        wdriver.find_element(by, locator)
        return True
    except NoSuchElementException:
        try:
            WebDriverWait(wdriver, timeout).until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            return False
    finally:
        wdriver.implicitly_wait(implicit_timeout)


def get_element(wdriver, by, locator):
    return wdriver.find_element(by, locator)


def wait_for_element(wdriver, by, locator):
    wait = WebDriverWait(wdriver, wait_timeout)
    if by.__eq__("css selector"):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))


def title_present(wdriver, title):
        try:
            wait = WebDriverWait(wdriver, wait_timeout)
            wait.until(EC.title_is(title))
            return True
        except TimeoutException:
            return False
        finally:
            wdriver.implicitly_wait(implicit_timeout)
