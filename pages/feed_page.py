"""Объект страницы ленты заказов."""

import allure

from config.settings import BASE_URL
from locators.feed_page_locators import FeedPageLocators
from pages.base_page import BasePage
from pages.header_page import HeaderComponent


class FeedPage(BasePage):
    """Объект страницы ленты заказов."""

    def __init__(self, driver):
        """Инициализирует объекты страницы ленты."""

        super().__init__(driver)
        self.header = HeaderComponent(driver)

    @allure.step("Открыть страницу ленты заказов")
    def open(self):
        """Открывает ленту заказов."""

        self.open_url(f"{BASE_URL}/feed")
        return self.wait_until_loaded()

    @allure.step("Дождаться загрузки страницы ленты заказов")
    def wait_until_loaded(self):
        """Ожидает загрузку страницы ленты заказов."""

        self.wait_for_visibility(FeedPageLocators.PAGE_HEADING)
        self.wait_for_visibility(FeedPageLocators.ORDER_FEED_LIST)
        return self

    @allure.step("Получить счётчик выполненных заказов за всё время")
    def get_all_time_total(self) -> int:
        """Возвращает значение общего счётчика заказов."""

        return int(self.get_text(FeedPageLocators.ALL_TIME_TOTAL))

    @allure.step("Получить счётчик выполненных заказов за сегодня")
    def get_today_total(self) -> int:
        """Возвращает значение дневного счётчика заказов."""

        return int(self.get_text(FeedPageLocators.TODAY_TOTAL))

    @allure.step("Дождаться увеличения счётчика заказов")
    def wait_for_total_growth(self, previous_value: int, getter):
        """Ожидает, что переданный счётчик увеличится."""

        self.wait.until(lambda _: getter() > previous_value)

    @allure.step("Повторно открыть ленту и получить обновлённый общий счётчик")
    def refresh_and_get_all_time_total(self, previous_value: int) -> int:
        """Повторно открывает ленту, ждёт рост общего счётчика и возвращает его значение."""

        self.open()
        self.wait_for_total_growth(previous_value, self.get_all_time_total)
        return self.get_all_time_total()

    @allure.step("Повторно открыть ленту и получить обновлённый дневной счётчик")
    def refresh_and_get_today_total(self, previous_value: int) -> int:
        """Повторно открывает ленту, ждёт рост дневного счётчика и возвращает его значение."""

        self.open()
        self.wait_for_total_growth(previous_value, self.get_today_total)
        return self.get_today_total()

    @allure.step("Проверить, что заказ отображается в карточках ленты")
    def has_order_card(self, formatted_order_number: str) -> bool:
        """Проверяет наличие карточки заказа в ленте."""

        return self.is_element_visible(FeedPageLocators.order_card(formatted_order_number))

    @allure.step("Проверить, что заказ отображается в разделе «Готовы»")
    def has_order_in_ready(self, formatted_order_number: str) -> bool:
        """Проверяет наличие номера заказа в списке готовых."""

        return self.is_element_visible(FeedPageLocators.order_in_ready_list(formatted_order_number))

    @allure.step("Проверить, что заказ отображается в разделе «В работе»")
    def has_order_in_progress(self, formatted_order_number: str, timeout: int = 3) -> bool:
        """Проверяет наличие номера заказа в списке заказов в работе."""

        return self.is_element_visible(
            FeedPageLocators.order_in_progress_list(formatted_order_number),
            timeout=timeout,
        )

    @allure.step("Определить, где отображается новый заказ в ленте")
    def get_order_status(self, formatted_order_number: str) -> str:
        """Возвращает статус отображения заказа в ленте."""

        if self.has_order_in_progress(formatted_order_number, timeout=2):
            return "in_progress"
        if self.has_order_in_ready(formatted_order_number):
            return "ready"
        if self.has_order_card(formatted_order_number):
            return "feed"
        return "missing"
