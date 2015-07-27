from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

__author__ = 'Olga'

import os
import ConfigParser
from selenium import webdriver
from grail import BaseTest, step
from nose.tools import assert_is, eq_

username = 'olga@blazemeter.com'
password = '12345678'


def setup_class():
    global url
    global implicit_timeout
    config = ConfigParser.RawConfigParser()
    path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    config.read(os.path.join(path, 'settings.properties'))
    chromedriver = config.get('BrowserSection', 'chromedriver')
    os.environ["webdriver.chrome.driver"] = chromedriver
    url = config.get('urlSection', 'url')
    implicit_timeout = config.get('driverSection', 'implicit.timeout')
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    driver.implicitly_wait(implicit_timeout)
    return driver


class BZW_44(BaseTest):

    def test_login_logout(self):
        self.driver = setup_class()
        self.open_sign_in_page()
        self.type_username()
        self.type_password()
        self.click_sign_in()

    @step
    def open_sign_in_page(self):
        self.url = url
        self.driver.get(self.url + '/sign-in')
        eq_(self.driver.title.__contains__('Sign in | BlazeMeter'), True)

    @step
    def type_username(self):
        elem = self.driver.find_element_by_name('email')
        elem.send_keys(username)

    @step
    def type_password(self):
        elem = self.driver.find_element_by_name('password')
        elem.send_keys(password)

    @step
    def click_sign_in(self):
        elem = self.driver.find_element_by_xpath("//button[@type='submit']")
        elem.click()
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "headline-sub")))
        assert_is(self.driver.find_element_by_xpath("//button[text()='Start the test']").is_displayed(), True)

    def tearDown(self):
        self.driver.close()
