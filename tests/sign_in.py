__author__ = 'Olga'

import os
import ConfigParser
from selenium import webdriver
from grail import BaseTest, step
from nose.tools import assert_is, eq_

def setup_class():
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
    wait_timeout = config.get('driverSection', 'wait.timeout')
    username = config.get('dataSection', 'username')
    password = config.get('dataSection', 'password')
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    driver.implicitly_wait(implicit_timeout)

class BZW_42(BaseTest):
    def test_empty_data(self):
        setup_class()
        self.open_sign_in_page()
        self.leave_empty_fields_and_sign_in()
        self.verify_action()

    @step
    def open_sign_in_page(self):
        self.url = url
        driver.get(self.url + '/sign-in')
        eq_(driver.title.__contains__('Sign in | BlazeMeter'), True, "Failed to open 'Sign in' page")

    @step
    def leave_empty_fields_and_sign_in(self):
        elem = driver.find_element_by_xpath("//button[@type='submit']")
        elem.click()

    @step
    def verify_action(self):
        eq_(driver.title.__contains__('Sign in | BlazeMeter'), True, "Failed to stay on the 'Sign in' page")


class BZW_44(BaseTest):

    def test_login_logout(self):
        self.open_sign_in_page()
        self.type_username()
        self.type_password()
        self.remember_me_uncheck()
        self.click_sign_in()
        self.logout()

    @step
    def open_sign_in_page(self):
        self.url = url
        driver.get(self.url + '/sign-in')
        eq_(driver.title.__contains__('Sign in | BlazeMeter'), True, "Failed to open 'Sign in' page")

    @step
    def type_username(self):
        elem = driver.find_element_by_name('email')
        elem.send_keys(username)

    @step
    def type_password(self):
        elem = driver.find_element_by_name('password')
        elem.send_keys(password)

    @step
    def remember_me_uncheck(self):
        elem = driver.find_element_by_xpath("//input[@title='Remember Me']")
        if elem.is_selected():
            elem.click()
        assert_is(elem.is_selected(), False, "'Remember me' is checked")

    @step
    def click_sign_in(self):
        elem = driver.find_element_by_xpath("//button[@type='submit']")
        elem.click()
        assert_is(driver.find_element_by_xpath("//button[text()='Start the test']").is_enabled(), True,
                  "Failed to login or 'Welcome' page is not displayed'")

    @step
    def logout(self):
        elem = driver.find_element_by_class_name('bm-logo')
        elem.click()
        logout_link = driver.find_element_by_xpath("//div[@title='Logout']//a[@class='menu-item-link']")
        logout_link.click()
        driver.implicitly_wait(implicit_timeout)
        eq_(driver.title.__contains__('Sign in | BlazeMeter'), True, "User is not logout")

    def tearDown(self):
        driver.close()
