import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver():
    """Глобальный webdriver для всех тестов с минимальными настройками."""

    options = Options()
    options.add_argument("--headless=new")          # без UI, чтобы тесты гонялись в CI
    options.add_argument("--window-size=1400,900")  # фиксированный размер окна

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)  # небольшой implicit wait, основное – явные ожидания в Page Object

    yield driver
    driver.quit()
