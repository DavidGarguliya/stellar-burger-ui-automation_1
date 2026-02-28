"""Вспомогательные действия для тестов конструктора."""

import allure

from test_data.ingredients import Ingredient


class ConstructorHelper:
    """Набор действий для тестов конструктора."""

    @staticmethod
    @allure.step("Получить значения счётчика ингредиента до и после добавления")
    def get_ingredient_counter_before_and_after_adding(
        constructor_page,
        ingredient: Ingredient,
    ) -> tuple[int, int]:
        """Возвращает значения счётчика ингредиента до и после добавления в конструктор."""

        initial_counter = constructor_page.get_ingredient_counter(ingredient)
        constructor_page.add_ingredient_to_constructor(ingredient)
        updated_counter = constructor_page.get_ingredient_counter(ingredient)
        return initial_counter, updated_counter
