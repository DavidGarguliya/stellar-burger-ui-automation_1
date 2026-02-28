"""Фабрика браузеров для UI-тестов."""

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from config.settings import (
    CHROME_BINARY_ENV,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    FIREFOX_BINARY_ENV,
)


def _apply_optional_binary(options, env_var_name: str):
    """Подкладывает путь к браузеру только если он явно передан через переменную окружения."""

    binary_path = os.getenv(env_var_name)
    if binary_path:
        options.binary_location = binary_path


def create_driver(browser_name: str):
    """Создаёт драйвер для указанного браузера."""

    if browser_name == "chrome":
        options = ChromeOptions()
        _apply_optional_binary(options, CHROME_BINARY_ENV)
        options.add_argument("--headless=new")
        options.add_argument(f"--window-size={DEFAULT_WINDOW_WIDTH},{DEFAULT_WINDOW_HEIGHT}")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        _apply_optional_binary(options, FIREFOX_BINARY_ENV)
        options.add_argument("-headless")
        service = FirefoxService(log_output=os.devnull)
        driver = webdriver.Firefox(options=options, service=service)
        driver.set_window_size(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

    driver.implicitly_wait(0)
    return driver
