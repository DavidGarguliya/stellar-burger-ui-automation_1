"""Локаторы шапки приложения."""

from selenium.webdriver.common.by import By


class HeaderLocators:
    """Локаторы навигации в шапке."""

    CONSTRUCTOR_LINK = (
        By.XPATH,
        "//a[@href='/' and .//*[contains(normalize-space(), 'Конструктор')]]",
    )
    ORDER_FEED_LINK = (
        By.XPATH,
        "//a[@href='/feed' and .//*[contains(normalize-space(), 'Лента')]]",
    )
