from selenium.webdriver.common.by import By
from common.base_page import BasePage
from helpers.allure_helper import step


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    """
        Cart Page Locators
    """
    search_field = (By.CSS_SELECTOR, "input.cdx-text-input__input")
    searched_item = (By.CSS_SELECTOR, "li.cdx-menu-item")

    @step
    def search_text(self, text):
        self.wait_for_element_to_be_visible(self.search_field)
        self.enter_text(self.search_field, text)

    @step
    def count_search_results(self):
        self.wait_for_element_to_be_visible(self.searched_item)
        return len(self.find_elements(self.searched_item))
