"""Тесты навигации по основным разделам."""

import allure

from config.settings import BASE_URL


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

        with allure.step("Перейти из ленты заказов в конструктор"):
            constructor_page = feed_page.header.open_constructor_page()
            current_url = constructor_page.get_current_url().rstrip("/")
            heading = constructor_page.get_heading_text()

        with allure.step("Проверить URL и заголовок страницы конструктора"):
            assert current_url == BASE_URL
            assert heading == "Соберите бургер"

    @allure.story("Переход в ленту заказов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что ссылка «Лента заказов» открывает страницу с публичной лентой и счётчиками заказов.")
    @allure.title("Переход по клику на «Лента заказов»")
    def test_click_on_order_feed_opens_feed_page(self, constructor_page):
        """Переход из конструктора открывает ленту заказов."""

        with allure.step("Перейти из конструктора в ленту заказов"):
            feed_page = constructor_page.header.open_feed_page()
            all_time_total = feed_page.get_all_time_total()

        with allure.step("Проверить, что счётчик выполненных заказов отображается"):
            assert all_time_total > 0
