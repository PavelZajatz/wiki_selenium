import pytest
from common.base_test import BaseTest
from pages.main_page import MainPage


class TestSearch(BaseTest):

    @pytest.fixture(autouse=True)
    def driver_parse(self, driver):
        self.main_page = MainPage(self.driver)

    @pytest.mark.parametrize("keyword, searched_results", [
        ("Appium", 11),
        ("###############", 1)
    ])
    def test_verify_search(self, keyword, searched_results):
        self.main_page.search_text(keyword)
        results = self.main_page.count_search_results()
        assert results == searched_results, (f"Search menu listbox should have"
                                             f" {searched_results} elements, {results} are shown instead")
