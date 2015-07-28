__author__ = 'Olga'

import os
import sys
from selenium.webdriver.common.keys import Keys
from grail import BaseTest, step
from nose.tools import assert_is, eq_
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.driver import start_driver
from utils.sign_in_page import SignIn


def setup_class():
    global url
    global implicit_timeout
    global wait_timeout
    global username
    global password
    global driver
    driver, wait_timeout, implicit_timeout, url, username, password = start_driver()


class BZW_41(BaseTest):

    def test_page_elements(self):
        setup_class()
        self.open_sign_in_page()
        self.verify_elements()
        self.click_to_website_logo()
        self.close_the_tab()
        self.check_remember_me_checkbox()
        self.uncheck_remember_me_checkbox()

    @step
    def open_sign_in_page(self):
        self.page = SignIn(driver, url, implicit_timeout)
        self.page.open(driver)
        eq_(self.page.get_title(driver).__contains__('Sign in | BlazeMeter'), True)

    @step
    def verify_elements(self):
        self.page.wait_for_element(driver, SignIn.logo)
        assert_is(self.page.is_element_displayed(driver, SignIn.logo), True,
                  "BlazeMeter logo is not displayed")
        assert_is(self.page.is_element_displayed(driver, SignIn.sign_in_google_button), True,
                  "'Sing in with Google' button is not displayed")
        assert_is(self.page.is_element_displayed(driver, SignIn.help_block), True,
                  "Information about using SAML is not displayed")
        assert_is(self.page.is_element_displayed(driver, SignIn.email), True,
                  "'Email' field is not displayed")
        assert_is(self.page.is_element_displayed(driver, SignIn.password), True,
                  "'Password' field is not displayed")
        assert_is(self.page.is_element_displayed(driver, SignIn.sign_in_button), True,
                  "'Sign in' button is not displayed")
        assert_is(self.page.is_element_displayed(driver, SignIn.remember_me_checkbox), True,
                  "'Remember me' checkbox is not displayed")
        assert_is(self.page.is_element_displayed(driver, SignIn.forgot_password_link), True,
                  "'Forgot your password' link is not displayed")

    @step
    def click_to_website_logo(self):
        self.page.click_on_logo(driver)
        eq_(self.page.get_title(driver).__contains__('Sign in | BlazeMeter'), True)

    @step
    def close_the_tab(self):
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    @step
    def check_remember_me_checkbox(self):
        box = driver.find_element_by_xpath("//input[@class='remember-me-check']")
        box.click()
        assert_is(box.is_selected(), True)

    @step
    def uncheck_remember_me_checkbox(self):
        box = driver.find_element_by_xpath("//input[@class='remember-me-check']")
        box.click()
        assert_is(box.is_selected(), False)


class BZW_42(BaseTest):
    def test_empty_data(self):
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
        #self.logout()

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
