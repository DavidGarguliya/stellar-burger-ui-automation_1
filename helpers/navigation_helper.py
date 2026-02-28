"""Вспомогательные действия для тестов навигации."""

import allure

from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage


class NavigationHelper:
    """Набор действий для тестов навигации."""

    @staticmethod
    @allure.step("Перейти из ленты заказов в конструктор и получить состояние страницы")
    def open_constructor_from_feed(feed_page: FeedPage) -> tuple[ConstructorPage, str, str]:
        """Открывает конструктор из ленты и возвращает страницу, URL и заголовок."""

        constructor_page = feed_page.header.open_constructor_page()
        return (
            constructor_page,
            constructor_page.driver.current_url.rstrip("/"),
            constructor_page.get_heading_text(),
        )

    @staticmethod
    @allure.step("Перейти из конструктора в ленту заказов и получить значение счётчика")
    def open_feed_from_constructor(constructor_page: ConstructorPage) -> tuple[FeedPage, int]:
        """Открывает ленту из конструктора и возвращает страницу и общий счётчик."""

        feed_page = constructor_page.header.open_feed_page()
        return feed_page, feed_page.get_all_time_total()
