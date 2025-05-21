# -- FILE: features/environment.py
from behave import fixture, use_fixture
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def before_scenario(context, scenario):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  # opcional
    chrome_options.set_capability("browserName", "chrome")

    context.driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=chrome_options
    )


def after_scenario(context, scenario):
    try:
        context.driver.quit()
    except WebDriverException as e:
        print(f"⚠️  Error al cerrar el navegador: {e}")
