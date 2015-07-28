__author__ = 'Olga'

from selenium.webdriver.common.by import By
from driver import wait_for_element
from selenium.common.exceptions import NoSuchElementException


class SignIn(object):

    logo = "a img.top-logo-image"
    #logo_link = "//img[@class='top-logo-image']/parent::a"
    sign_in_google_button = "a.btn.btn-Google"
    help_block = "p.help-block"
    email = "input.form-input.email"
    password = "input.form-input.password"
    sign_in_button = "button.btn.btn-signin"
    remember_me_checkbox = "input.remember-me-check"
    forgot_password_link = "a.forgot-password"

    def __init__(self, driver, url, implicit_timeout):
        global logo
        global sign_in_google_button
        global help_block
        global email
        global password
        global sign_in_button
        global remember_me_checkbox
        global forgot_password_link

        self.driver = driver
        self.url = url
        self.implicit_timeout = implicit_timeout

    def open(self, driver):
        self.driver = driver
        self.driver.get(self.url + "/sign_in")
        self.driver.implicitly_wait(self.implicit_timeout)
        return SignIn

    def get_title(self, driver):
        self.driver = driver
        return self.driver.title

    def is_element_displayed(self, driver, elem):
        self.driver = driver
        try:
            self.driver.find_element_by_css_selector(elem).is_displayed()
            return True
        except NoSuchElementException:
            return False
        finally:
            driver.implicitly_wait(self.implicit_timeout)

    def wait_for_element(self, driver, elem):
        self.driver = driver
        return wait_for_element(self.driver, By.CSS_SELECTOR, elem)

    def click(self, driver, element):
        self.driver = driver
        elem = self.driver.find_element_by_css_selector(element)
        elem.click()

    def click_on_logo(self, driver):
        self.driver = driver
        elem = self.driver.find_element_by_css_selector(self.logo)
        elem.click()

