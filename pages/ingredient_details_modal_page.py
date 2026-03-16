"""Объект модального окна с деталями ингредиента."""

import allure

from locators.ingredient_details_modal_locators import IngredientDetailsModalLocators
from pages.base_page import BasePage


class IngredientDetailsModal(BasePage):
    """Модальное окно с деталями ингредиента."""

    @allure.step("Дождаться открытия модального окна ингредиента")
    def wait_until_opened(self):
        """Ожидает открытие модального окна."""

        self.wait_for_visibility(IngredientDetailsModalLocators.MODAL)
        return self

    @allure.step("Проверить, что модальное окно ингредиента открыто")
    def is_opened(self, timeout: int = 1) -> bool:
        """Возвращает признак открытого модального окна."""

        return self.is_element_visible(IngredientDetailsModalLocators.MODAL, timeout=timeout)

    @allure.step("Закрыть модальное окно ингредиента")
    def close(self):
        """Закрывает модальное окно по крестику."""

        self.js_click(IngredientDetailsModalLocators.CLOSE_BUTTON)
        self.wait_for_invisibility(IngredientDetailsModalLocators.MODAL)

    @allure.step("Получить заголовок модального окна ингредиента")
    def get_title(self) -> str:
        """Возвращает заголовок модального окна."""

        return self.get_text(IngredientDetailsModalLocators.TITLE)

    @allure.step("Получить имя ингредиента из модального окна")
    def get_ingredient_name(self) -> str:
        """Возвращает название ингредиента."""

        return self.get_text(IngredientDetailsModalLocators.INGREDIENT_NAME)

    @allure.step("Проверить, что модальное окно ингредиента закрыто")
    def is_closed(self) -> bool:
        """Возвращает признак закрытого модального окна."""

        return not self.is_element_visible(IngredientDetailsModalLocators.MODAL, timeout=1)
