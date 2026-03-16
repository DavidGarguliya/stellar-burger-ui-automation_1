"""Объект модального окна оформленного заказа."""

import allure

from locators.order_details_modal_locators import OrderDetailsModalLocators
from pages.base_page import BasePage


class OrderDetailsModal(BasePage):
    """Модальное окно с номером оформленного заказа."""

    @allure.step("Дождаться открытия модального окна заказа")
    def wait_until_opened(self):
        """Ожидает открытие модального окна заказа."""

        self.wait_for_visibility(OrderDetailsModalLocators.MODAL)
        return self

    @allure.step("Получить номер заказа")
    def get_order_number(self) -> int:
        """Возвращает номер заказа из модального окна."""

        self.wait.until(
            lambda _: self.get_text(OrderDetailsModalLocators.ORDER_NUMBER) != "9999"
        )
        return int(self.get_text(OrderDetailsModalLocators.ORDER_NUMBER))

    @allure.step("Закрыть модальное окно заказа")
    def close(self):
        """Закрывает модальное окно заказа."""

        self.click(OrderDetailsModalLocators.CLOSE_BUTTON)
        self.wait_for_invisibility(OrderDetailsModalLocators.MODAL)
