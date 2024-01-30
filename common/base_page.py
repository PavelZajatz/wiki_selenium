from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from helpers.allure_helper import step
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @step
    def click(self, locator):
        """Clicks the specified object"""
        time.sleep(0.5)
        self.wait_for_element_to_be_clickable(locator=locator)
        element = self.driver.find_element(*locator)
        element.click()

    @step
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @step
    def is_displayed(self, locator):
        self.wait_for_element_to_be_visible(locator)
        element = self.driver.find_element(*locator)
        return element.is_displayed()

    @step
    def is_enabled(self, locator):
        element = self.driver.find_element(*locator)
        return element.is_enabled()

    @step
    def enter_text(self, locator, keys):
        self.wait_for_element_to_be_visible(locator=locator)
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(keys)

    @step
    def refresh_page(self):
        self.driver.refresh()

    @step
    def wait_for_element_to_be_clickable(self, locator):
        wait = WebDriverWait(self.driver, 7)
        try:
            return wait.until(EC.element_to_be_clickable(locator))
        except (TimeoutException, WebDriverException, NoSuchElementException):
            try:
                self.scroll_to_top()
                return wait.until(EC.element_to_be_clickable(locator))
            except (TimeoutException, WebDriverException, NoSuchElementException):
                self.scroll_to_bottom()
                return wait.until(EC.element_to_be_clickable(locator))

    @step
    def wait_for_element_to_be_visible(self, locator):
        wait = WebDriverWait(self.driver, 15)
        try:
            return wait.until(EC.visibility_of_element_located(locator))
        except (TimeoutException, WebDriverException, NoSuchElementException):
            try:
                self.scroll_to_top()
                return wait.until(EC.visibility_of_element_located(locator))
            except (TimeoutException, WebDriverException, NoSuchElementException):
                self.scroll_to_bottom()
                return wait.until(EC.visibility_of_element_located(locator))

    @step
    def scroll_to_top(self):
        self.implicit_wait(1)
        self.driver.execute_script("window.scrollTo(0, 0)")

    @step
    def scroll_to_bottom(self):
        self.implicit_wait(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    @step
    def implicit_wait(self, wait_time):
        time.sleep(wait_time)
