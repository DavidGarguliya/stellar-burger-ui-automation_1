"""Объект шапки приложения."""

import allure
from selenium.common.exceptions import ElementClickInterceptedException

from locators.header_locators import HeaderLocators
from pages.base_page import BasePage


class HeaderComponent(BasePage):
    """Объект навигации в шапке сайта."""

    @allure.step("Перейти в конструктор из шапки")
    def click_constructor(self):
        """Кликает по ссылке конструктора."""

        try:
            self.click(HeaderLocators.CONSTRUCTOR_LINK)
        except ElementClickInterceptedException:
            self.js_click(HeaderLocators.CONSTRUCTOR_LINK)

    @allure.step("Открыть страницу конструктора через шапку")
    def open_constructor_page(self):
        """Переходит на страницу конструктора и возвращает её объект."""

        from pages.constructor_page import ConstructorPage

        self.click_constructor()
        return ConstructorPage(self.driver).wait_until_loaded()

    @allure.step("Перейти в ленту заказов из шапки")
    def click_order_feed(self):
        """Кликает по ссылке ленты заказов."""

        try:
            self.click(HeaderLocators.ORDER_FEED_LINK)
        except ElementClickInterceptedException:
            self.js_click(HeaderLocators.ORDER_FEED_LINK)

    @allure.step("Открыть страницу ленты заказов через шапку")
    def open_feed_page(self):
        """Переходит на страницу ленты заказов и возвращает её объект."""

        from pages.feed_page import FeedPage

        self.click_order_feed()
        return FeedPage(self.driver).wait_until_loaded()
