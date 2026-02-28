"""Объект страницы конструктора."""

import allure

from locators.constructor_page_locators import ConstructorPageLocators
from config.settings import BASE_URL
from pages.base_page import BasePage
from pages.header_page import HeaderComponent
from pages.ingredient_details_modal_page import IngredientDetailsModal
from pages.order_details_modal_page import OrderDetailsModal
from test_data.ingredients import Ingredient


class ConstructorPage(BasePage):
    """Объект страницы конструктора бургеров."""

    def __init__(self, driver):
        """Инициализирует объекты страницы конструктора."""

        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.ingredient_modal = IngredientDetailsModal(driver)
        self.order_modal = OrderDetailsModal(driver)

    @allure.step("Открыть страницу конструктора")
    def open(self):
        """Открывает конструктор."""

        self.open_url(BASE_URL)
        return self.wait_until_loaded()

    @allure.step("Дождаться загрузки страницы конструктора")
    def wait_until_loaded(self):
        """Ожидает загрузку страницы конструктора."""

        self.wait_for_visibility(ConstructorPageLocators.PAGE_HEADING)
        return self

    @allure.step("Получить заголовок страницы конструктора")
    def get_heading_text(self) -> str:
        """Возвращает заголовок страницы конструктора."""

        return self.get_text(ConstructorPageLocators.PAGE_HEADING)

    @allure.step("Открыть детали ингредиента")
    def open_ingredient_details(self, ingredient: Ingredient):
        """Открывает модальное окно ингредиента по клику."""

        self.js_click(ConstructorPageLocators.ingredient_card(ingredient.identifier))
        return self.ingredient_modal.wait_until_opened()

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_constructor(self, ingredient: Ingredient):
        """Перетаскивает ингредиент в конструктор."""

        self.drag_and_drop(
            ConstructorPageLocators.ingredient_card(ingredient.identifier),
            ConstructorPageLocators.CONSTRUCTOR_BASKET,
        )
        if self.ingredient_modal.is_opened():
            self.ingredient_modal.close()

    @allure.step("Получить значение счётчика ингредиента")
    def get_ingredient_counter(self, ingredient: Ingredient) -> int:
        """Возвращает текущее значение счётчика ингредиента."""

        return int(self.get_text(ConstructorPageLocators.ingredient_counter(ingredient.identifier)))

    @allure.step("Оформить заказ")
    def place_order(self):
        """Нажимает кнопку оформления заказа и ждёт модальное окно."""

        if self.ingredient_modal.is_opened():
            self.ingredient_modal.close()
        self.click(ConstructorPageLocators.ORDER_BUTTON)
        return self.order_modal.wait_until_opened()
