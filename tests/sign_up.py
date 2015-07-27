__author__ = 'Olga'

import os
import ConfigParser
import random
import string

from selenium import webdriver
from grail import BaseTest, step
from nose.tools import eq_

first_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
last_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
email = ''.join(random.choice(string.ascii_lowercase) for _ in range(5)) + '@gmail.com'
password = ''.join(random.choice(string.digits) for _ in range(8))


def setup_class():
    global url
    global implicit_timeout
    global wait_timeout
    global driver
    config = ConfigParser.RawConfigParser()
    path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    config.read(os.path.join(path, 'settings.properties'))
    chromedriver = config.get('BrowserSection', 'chromedriver')
    os.environ["webdriver.chrome.driver"] = chromedriver
    url = config.get('urlSection', 'url')
    implicit_timeout = config.get('driverSection', 'implicit.timeout')
    wait_timeout = config.get('driverSection', 'wait.timeout')
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    driver.implicitly_wait(implicit_timeout)


class BZW_38(BaseTest):
    def test_register_new_user(self):
        setup_class()
        self.open_sign_up_page()
        self.type_first_name()
        self.type_last_name()
        self.type_email()
        self.type_password()
        self.click_sign_up()
        self.open_main_app_page()

    @step
    def open_sign_up_page(self):
        self.url = url
        driver.get(self.url + '/sign-up')
        driver.implicitly_wait(implicit_timeout)
        eq_(str(driver.title).__contains__('Sign up | BlazeMeter'), True, "Failed to open 'Sign up' page")

    @step
    def type_first_name(self):
        elem = driver.find_element_by_name('firstName')
        elem.send_keys(first_name)
        value = elem.get_attribute('value')
        eq_(str(value), first_name, "First name was entered incorrect")

    @step
    def type_last_name(self):
        elem = driver.find_element_by_name('lastName')
        elem.send_keys(last_name)
        value = elem.get_attribute('value')
        eq_(str(value), last_name, "Last name was entered incorrect")

    @step
    def type_email(self):
        elem = driver.find_element_by_name('email')
        elem.send_keys(email)
        value = elem.get_attribute('value')
        eq_(str(value), email, "Email was entered incorrect")

    @step
    def type_password(self):
        elem = driver.find_element_by_name('password')
        elem.send_keys(password)
        value = elem.get_attribute('value')
        eq_(str(value), password, "Password name was entered incorrect")

    @step
    def click_sign_up(self):
        elem = driver.find_element_by_xpath("//button[@type='submit']")
        elem.click()
        eq_(driver.find_element_by_xpath("//button[text()='Start the test']").is_enabled(), True,
            "Failed to login or 'Welcome' page is not displayed'")

    @step
    def open_main_app_page(self):
        elem = driver.find_element_by_class_name('bm-logo')
        elem.click()
        welcome_message = driver.find_element_by_xpath("//div[@class='stat-block']//h2")
        eq_(str(welcome_message.text), "Hi, " + first_name +" " + last_name)
        logout_link = driver.find_element_by_xpath("//div[@title='Logout']//a[@class='menu-item-link']")
        eq_(logout_link.is_enabled(), True)
        logout_link.click()

    def tearDown(self):
        driver.close()
