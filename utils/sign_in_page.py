__author__ = 'Olga'


from selenium.webdriver.common.by import By
from driver import is_element_present


class SignIn(object):
    global logo

    logo = "//img[@class='top-logo-image']"

    def __init__(self, driver, url, implicit_timeout):
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
        return is_element_present(self.driver, By.XPATH, logo)
