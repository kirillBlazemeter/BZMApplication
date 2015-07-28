__author__ = 'Olga'

from selenium.webdriver.common.by import By
from driver import is_element_present


class SignIn(object):
    def __init__(self, driver, url, implicit_timeout):
        self.logo = "//img[@class='top-logo-image']"
        self.sign_in_google_button = "//a[@class='btn btn-Google']"
        self.help_block = "//p[@class='help-block']"
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

    def is_logo_displayed(self, driver):
        self.driver = driver
        return is_element_present(self.driver, By.XPATH, self.logo)

    def is_google_button_displayed(self, driver):
        self.driver = driver
        return is_element_present(self.driver, By.XPATH, self.sign_in_google_button)

    def is_help_block_displayed(self, driver):
        self.driver = driver
        return is_element_present(self.driver, By.XPATH, self.help_block)
