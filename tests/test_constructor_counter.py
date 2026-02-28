"""Тесты работы счётчика ингредиентов в конструкторе."""

import allure

from helpers.constructor_helper import ConstructorHelper
from test_data.ingredients import SPICY_SAUCE


@allure.parent_suite("Диплом. Задание 3")
@allure.suite("Конструктор")
@allure.sub_suite("Счётчики ингредиентов")
@allure.epic("Stellar Burgers")
@allure.feature("Основная функциональность")
class TestConstructorCounter:
    """Проверки счётчиков ингредиентов."""

    @allure.story("Обновление счётчика ингредиента")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка, что после добавления ингредиента в конструктор его счётчик увеличивается.")
    @allure.title("Добавление ингредиента в заказ увеличивает его счётчик")
    def test_ingredient_counter_increases_after_adding_to_constructor(self, constructor_page):
        """После добавления ингредиента в конструктор его счётчик увеличивается."""

        initial_counter, updated_counter = ConstructorHelper.get_ingredient_counter_before_and_after_adding(
            constructor_page,
            SPICY_SAUCE,
        )

        assert updated_counter > initial_counter
