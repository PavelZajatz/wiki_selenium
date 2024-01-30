import os
import sys
import uuid

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

user_agent = "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/102.0.0.0 Safari/537.36"

main_url = "https://lang.wikipedia.org/wiki/"


def pytest_addoption(parser):
    """ Parse pytest --option variables from shell """
    parser.addoption('--browser', help='Which test browser?',
                     default='chrome')
    parser.addoption('--headless', help='headless or non-headless?',
                     choices=['true', 'false'],
                     default='false')
    parser.addoption('--lang', help='en or fr?',
                     choices=['en', 'fr'],
                     default='en')


@pytest.fixture(scope='session')
def test_browser(request):
    """ :returns Browser.NAME from --browser option """
    return request.config.getoption('--browser')


@pytest.fixture(scope='session')
def headless(request):
    """ :returns true or false from --headless option """
    return request.config.getoption('--headless')


@pytest.fixture(scope='session')
def lang(request):
    """ :returns en or fr from --lang option """
    return request.config.getoption('--lang')


@pytest.fixture(scope='function')
def driver(request, test_browser, lang, headless):
    if test_browser == 'firefox':
        if headless == 'false':
            driver = webdriver.Firefox()
        else:
            geco_options = webdriver.FirefoxOptions()
            geco_options.add_argument("-headless")
            driver = webdriver.Firefox(options=geco_options)
    elif test_browser == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-popup-blocking")
        if headless == 'true':
            chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        raise ValueError(
            f'--browser="{test_browser}" is not chrome or firefox')
    request.cls.driver = driver
    driver.get(main_url.replace("lang", lang))
    yield
    result = request.session.testsfailed
    if result != 0:
        allure.attach(driver.get_screenshot_as_png(), name=request.node.originalname + "_Failed_Screenshot",
                      attachment_type=AttachmentType.PNG)
    else:
        print("Test case is passed successfully")
    driver.quit()


@pytest.fixture(scope="session")
def testrun_uid(request):
    """Return the unique id of the current test."""
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["testrunuid"]
    else:
        return uuid.uuid4().hex


@pytest.fixture(autouse=True)
def set_report_name(driver: str, request, testrun_uid):
    setattr(request.node, "test_run", testrun_uid)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        setattr(item, "rep_outcome", rep.outcome)
    else:
        setattr(item, "rep_outcome", "")
