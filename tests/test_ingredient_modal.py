"""Тесты модального окна с деталями ингредиента."""

import allure

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

        with allure.step("Открыть модальное окно ингредиента и получить его данные"):
            _, title, ingredient_name = constructor_page.open_ingredient_modal_and_get_content(
                SPICY_SAUCE,
            )

        with allure.step("Проверить заголовок и название ингредиента в модальном окне"):
            assert title == "Детали ингредиента"
            assert ingredient_name == SPICY_SAUCE.name

    @allure.story("Закрытие деталей ингредиента")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что модальное окно ингредиента закрывается по клику на крестик.")
    @allure.title("Всплывающее окно закрывается по клику на крестик")
    def test_click_on_close_button_closes_details_modal(self, constructor_page):
        """Клик по крестику закрывает модальное окно ингредиента."""

        with allure.step("Открыть и закрыть модальное окно ингредиента"):
            modal = constructor_page.open_and_close_ingredient_modal(SPICY_SAUCE)

        with allure.step("Проверить, что модальное окно закрыто"):
            assert modal.is_closed()
