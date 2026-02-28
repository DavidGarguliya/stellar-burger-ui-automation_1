"""Вспомогательные действия для тестов модального окна ингредиента."""

import allure

from pages.ingredient_details_modal_page import IngredientDetailsModal
from test_data.ingredients import Ingredient


class IngredientModalHelper:
    """Набор действий для тестов модального окна ингредиента."""

    @staticmethod
    @allure.step("Открыть модальное окно ингредиента и получить его данные")
    def open_ingredient_modal_and_get_content(
        constructor_page,
        ingredient: Ingredient,
    ) -> tuple[IngredientDetailsModal, str, str]:
        """Открывает модальное окно ингредиента и возвращает его объект, заголовок и название."""

        modal = constructor_page.open_ingredient_details(ingredient)
        return modal, modal.get_title(), modal.get_ingredient_name()

    @staticmethod
    @allure.step("Открыть и закрыть модальное окно ингредиента")
    def open_and_close_ingredient_modal(constructor_page, ingredient: Ingredient) -> IngredientDetailsModal:
        """Открывает модальное окно ингредиента, закрывает его и возвращает объект модали."""

        modal = constructor_page.open_ingredient_details(ingredient)
        modal.close()
        return modal
