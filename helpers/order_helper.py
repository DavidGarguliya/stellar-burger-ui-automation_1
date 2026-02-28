"""Вспомогательные функции для тестов заказов."""

import allure

from pages.feed_page import FeedPage
from reporting.allure_reporter import attach_text
from test_data.ingredients import CRATER_BUN, LUMINESCENT_FILLING, SPICY_SAUCE


class OrderHelper:
    """Набор действий для тестов заказов."""

    @staticmethod
    @allure.step("Привести номер заказа к формату ленты")
    def format_order_number(order_number: int) -> str:
        """Приводит номер заказа к формату, который отображается в ленте."""

        return f"{order_number:07d}"

    @staticmethod
    @allure.step("Сохранить номер созданного заказа в отчёт")
    def attach_created_order_number(order_number: int):
        """Прикладывает номер созданного заказа в Allure."""

        attach_text("Номер созданного заказа", str(order_number))

    @staticmethod
    @allure.step("Сохранить форматированный номер заказа в отчёт")
    def attach_formatted_order_number(formatted_order_number: str):
        """Прикладывает форматированный номер заказа в Allure."""

        attach_text("Форматированный номер заказа для ленты", formatted_order_number)

    @staticmethod
    @allure.step("Сохранить значение счётчика заказов в отчёт")
    def attach_order_counter_value(counter_name: str, value: int, stage: str):
        """Прикладывает значение счётчика заказов в Allure."""

        attach_text(f"{counter_name} {stage}", str(value))

    @staticmethod
    @allure.step("Создать заказ и получить его номер")
    def place_order_and_get_number(authorized_constructor_page) -> int:
        """Собирает бургер, оформляет заказ и возвращает его номер."""

        with allure.step("Добавить булку в конструктор"):
            authorized_constructor_page.add_ingredient_to_constructor(CRATER_BUN)
        with allure.step("Добавить соус в конструктор"):
            authorized_constructor_page.add_ingredient_to_constructor(SPICY_SAUCE)
        with allure.step("Добавить начинку в конструктор"):
            authorized_constructor_page.add_ingredient_to_constructor(LUMINESCENT_FILLING)

        with allure.step("Оформить заказ и дождаться модального окна"):
            order_modal = authorized_constructor_page.place_order()

        with allure.step("Получить номер оформленного заказа"):
            order_number = order_modal.get_order_number()
            OrderHelper.attach_created_order_number(order_number)
            return order_number

    @staticmethod
    @allure.step("Открыть ленту заказов и получить общий счётчик до создания заказа")
    def open_feed_and_get_all_time_total(driver) -> tuple[FeedPage, int]:
        """Открывает ленту заказов и возвращает страницу и общий счётчик."""

        feed_page = FeedPage(driver).open()
        all_time_total = feed_page.get_all_time_total()
        OrderHelper.attach_order_counter_value(
            "Счётчик «Выполнено за всё время»",
            all_time_total,
            "до создания заказа",
        )
        return feed_page, all_time_total

    @staticmethod
    @allure.step("Повторно открыть ленту и получить обновлённый общий счётчик")
    def refresh_feed_and_get_all_time_total(feed_page: FeedPage, previous_value: int) -> int:
        """Повторно открывает ленту, ждёт рост общего счётчика и возвращает его значение."""

        feed_page.open()
        feed_page.wait_for_total_growth(previous_value, feed_page.get_all_time_total)
        all_time_total = feed_page.get_all_time_total()
        OrderHelper.attach_order_counter_value(
            "Счётчик «Выполнено за всё время»",
            all_time_total,
            "после создания заказа",
        )
        return all_time_total

    @staticmethod
    @allure.step("Открыть ленту заказов и получить дневной счётчик до создания заказа")
    def open_feed_and_get_today_total(driver) -> tuple[FeedPage, int]:
        """Открывает ленту заказов и возвращает страницу и дневной счётчик."""

        feed_page = FeedPage(driver).open()
        today_total = feed_page.get_today_total()
        OrderHelper.attach_order_counter_value(
            "Счётчик «Выполнено за сегодня»",
            today_total,
            "до создания заказа",
        )
        return feed_page, today_total

    @staticmethod
    @allure.step("Повторно открыть ленту и получить обновлённый дневной счётчик")
    def refresh_feed_and_get_today_total(feed_page: FeedPage, previous_value: int) -> int:
        """Повторно открывает ленту, ждёт рост дневного счётчика и возвращает его значение."""

        feed_page.open()
        feed_page.wait_for_total_growth(previous_value, feed_page.get_today_total)
        today_total = feed_page.get_today_total()
        OrderHelper.attach_order_counter_value(
            "Счётчик «Выполнено за сегодня»",
            today_total,
            "после создания заказа",
        )
        return today_total

    @staticmethod
    @allure.step("Создать новый заказ и подготовить номер для ленты")
    def place_order_and_get_formatted_number(authorized_constructor_page) -> str:
        """Создаёт заказ и возвращает его номер в формате ленты."""

        order_number = OrderHelper.place_order_and_get_number(authorized_constructor_page)
        formatted_order_number = OrderHelper.format_order_number(order_number)
        OrderHelper.attach_formatted_order_number(formatted_order_number)
        return formatted_order_number

    @staticmethod
    @allure.step("Определить, где отображается новый заказ в ленте")
    def get_order_feed_status(feed_page: FeedPage, formatted_order_number: str) -> str:
        """Возвращает статус отображения заказа в ленте."""

        if feed_page.has_order_in_progress(formatted_order_number, timeout=2):
            return "in_progress"
        if feed_page.has_order_in_ready(formatted_order_number):
            return "ready"
        if feed_page.has_order_card(formatted_order_number):
            return "feed"
        return "missing"
