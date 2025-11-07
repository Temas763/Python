import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.settings import settings
from utils.api_client import ScheduleAPI

@pytest.fixture(scope="session")
def api_client():
    return ScheduleAPI()

@pytest.fixture(scope="function")
def driver():
    if settings.BROWSER.lower() == "chrome":
        options = Options()
        if settings.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(options=options)
    elif settings.BROWSER.lower() == "firefox":
        options = FirefoxOptions()
        if settings.HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {settings.BROWSER}")

    driver.implicitly_wait(settings.TIMEOUT)

    yield driver

    driver.quit()

@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)

@pytest.fixture
def schedule_page(driver):
    from pages.schedule_page import SchedulePage
    return SchedulePage(driver)

@pytest.fixture
def auth_cookies():
    return {
        "token_global": settings.TOKEN,
        "session_teachers_cabinet": "ohnq4e36kcb3aci7r1ifhpultk"
    }


def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        try:
            if 'driver' in item.funcargs:
                driver = item.funcargs['driver']
                driver.save_screenshot("error_screenshot.png")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
