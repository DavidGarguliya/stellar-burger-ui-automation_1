"""Тесты модального окна с деталями ингредиента."""

import allure

from helpers.ingredient_modal_helper import IngredientModalHelper
from test_data.ingredients import SPICY_SAUCE


@allure.parent_suite("Диплом. Задание 3")
@allure.suite("Конструктор")
@allure.sub_suite("Модальное окно ингредиента")
@allure.epic("Stellar Burgers")
@allure.feature("Основная функциональность")
class TestIngredientDetailsModal:
    """Проверки модального окна ингредиента."""

    @allure.story("Открытие деталей ингредиента")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что клик по карточке ингредиента открывает модальное окно с корректными деталями.")
    @allure.title("Клик по ингредиенту открывает всплывающее окно с деталями")
    def test_click_on_ingredient_opens_details_modal(self, constructor_page):
        """После клика по ингредиенту открывается модальное окно с его деталями."""

        _, title, ingredient_name = IngredientModalHelper.open_ingredient_modal_and_get_content(
            constructor_page,
            SPICY_SAUCE,
        )

        assert title == "Детали ингредиента"
        assert ingredient_name == SPICY_SAUCE.name

    @allure.story("Закрытие деталей ингредиента")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что модальное окно ингредиента закрывается по клику на крестик.")
    @allure.title("Всплывающее окно закрывается по клику на крестик")
    def test_click_on_close_button_closes_details_modal(self, constructor_page):
        """Клик по крестику закрывает модальное окно ингредиента."""

        modal = IngredientModalHelper.open_and_close_ingredient_modal(constructor_page, SPICY_SAUCE)

        assert modal.is_closed()
