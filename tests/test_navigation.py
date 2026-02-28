"""Тесты навигации по основным разделам."""

import allure

from config.settings import BASE_URL
from helpers.navigation_helper import NavigationHelper


@allure.parent_suite("Диплом. Задание 3")
@allure.suite("Навигация")
@allure.sub_suite("Переходы между основными разделами")
@allure.epic("Stellar Burgers")
@allure.feature("Основная функциональность")
class TestNavigation:
    """Проверки переходов между конструктором и лентой заказов."""

    @allure.story("Переход в конструктор")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что ссылка «Конструктор» возвращает пользователя на главную страницу со сборкой бургера.")
    @allure.title("Переход по клику на «Конструктор»")
    def test_click_on_constructor_opens_constructor_page(self, feed_page):
        """Переход из ленты заказов в конструктор открывает страницу конструктора."""

        _, current_url, heading = NavigationHelper.open_constructor_from_feed(feed_page)

        assert current_url == BASE_URL
        assert heading == "Соберите бургер"

    @allure.story("Переход в ленту заказов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что ссылка «Лента заказов» открывает страницу с публичной лентой и счётчиками заказов.")
    @allure.title("Переход по клику на «Лента заказов»")
    def test_click_on_order_feed_opens_feed_page(self, constructor_page):
        """Переход из конструктора открывает ленту заказов."""

        _, all_time_total = NavigationHelper.open_feed_from_constructor(constructor_page)

        assert all_time_total > 0
