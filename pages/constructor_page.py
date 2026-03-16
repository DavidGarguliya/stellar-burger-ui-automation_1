"""Объект страницы конструктора."""

from collections.abc import Iterable

import allure

from api.api_client import TestUser
from config.settings import BASE_URL
from locators.constructor_page_locators import ConstructorPageLocators
from pages.base_page import BasePage
from pages.header_page import HeaderComponent
from pages.ingredient_details_modal_page import IngredientDetailsModal
from pages.order_details_modal_page import OrderDetailsModal
from reporting.allure_reporter import attach_json, mask_secret
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

    @allure.step("Авторизовать пользователя через localStorage")
    def authorize_user(self, test_user: TestUser):
        """Подкладывает токены пользователя в localStorage и обновляет страницу."""

        self.open_url(BASE_URL)
        self.execute_script(
            """
            window.localStorage.setItem('accessToken', arguments[0]);
            window.localStorage.setItem('refreshToken', arguments[1]);
            """,
            test_user.access_token,
            test_user.refresh_token,
        )
        attach_json(
            "Токены, записанные в localStorage",
            {
                "email": test_user.email,
                "accessToken": mask_secret(test_user.access_token),
                "refreshToken": mask_secret(test_user.refresh_token),
            },
        )
        self.refresh_page()
        return self

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

    @allure.step("Открыть модальное окно ингредиента и получить его данные")
    def open_ingredient_modal_and_get_content(
        self,
        ingredient: Ingredient,
    ) -> tuple[IngredientDetailsModal, str, str]:
        """Открывает модальное окно и возвращает его объект, заголовок и имя ингредиента."""

        modal = self.open_ingredient_details(ingredient)
        return modal, modal.get_title(), modal.get_ingredient_name()

    @allure.step("Открыть и закрыть модальное окно ингредиента")
    def open_and_close_ingredient_modal(self, ingredient: Ingredient) -> IngredientDetailsModal:
        """Открывает модальное окно ингредиента, закрывает его и возвращает объект модали."""

        modal = self.open_ingredient_details(ingredient)
        modal.close()
        return modal

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_constructor(self, ingredient: Ingredient):
        """Перетаскивает ингредиент в конструктор."""

        self.drag_and_drop(
            ConstructorPageLocators.ingredient_card(ingredient.identifier),
            ConstructorPageLocators.CONSTRUCTOR_BASKET,
        )
        if self.ingredient_modal.is_opened():
            self.ingredient_modal.close()

    @allure.step("Добавить набор ингредиентов в заказ")
    def add_ingredients_to_constructor(self, ingredients: Iterable[Ingredient]):
        """Добавляет набор ингредиентов в конструктор."""

        for ingredient in ingredients:
            self.add_ingredient_to_constructor(ingredient)
        return self

    @allure.step("Получить значение счётчика ингредиента")
    def get_ingredient_counter(self, ingredient: Ingredient) -> int:
        """Возвращает текущее значение счётчика ингредиента."""

        return int(self.get_text(ConstructorPageLocators.ingredient_counter(ingredient.identifier)))

    @allure.step("Получить значения счётчика ингредиента до и после добавления")
    def get_ingredient_counter_before_and_after_adding(
        self,
        ingredient: Ingredient,
    ) -> tuple[int, int]:
        """Возвращает значения счётчика ингредиента до и после добавления в конструктор."""

        initial_counter = self.get_ingredient_counter(ingredient)
        self.add_ingredient_to_constructor(ingredient)
        updated_counter = self.get_ingredient_counter(ingredient)
        return initial_counter, updated_counter

    @allure.step("Оформить заказ")
    def place_order(self):
        """Нажимает кнопку оформления заказа и ждёт модальное окно."""

        if self.ingredient_modal.is_opened():
            self.ingredient_modal.close()
        self.click(ConstructorPageLocators.ORDER_BUTTON)
        return self.order_modal.wait_until_opened()

    @allure.step("Оформить заказ из набора ингредиентов и получить его номер")
    def place_order_and_get_number(self, ingredients: Iterable[Ingredient]) -> int:
        """Добавляет ингредиенты, оформляет заказ и возвращает его номер."""

        self.add_ingredients_to_constructor(ingredients)
        return self.place_order().get_order_number()
