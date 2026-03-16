"""Локаторы страницы конструктора."""

from selenium.webdriver.common.by import By


class ConstructorPageLocators:
    """Локаторы страницы конструктора бургеров."""

    PAGE_HEADING = (By.XPATH, "//h1[normalize-space()='Соберите бургер']")
    CONSTRUCTOR_BASKET = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket']")
    ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='Оформить заказ']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Войти в аккаунт']")

    @staticmethod
    def ingredient_card(ingredient_id: str):
        """Возвращает локатор карточки ингредиента по идентификатору."""

        return By.CSS_SELECTOR, f"a[href='/ingredient/{ingredient_id}']"

    @staticmethod
    def ingredient_counter(ingredient_id: str):
        """Возвращает локатор счётчика ингредиента по идентификатору."""

        return (
            By.CSS_SELECTOR,
            f"a[href='/ingredient/{ingredient_id}'] .counter_counter__num__3nue1",
        )
