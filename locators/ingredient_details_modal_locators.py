"""Локаторы модального окна с деталями ингредиента."""

from selenium.webdriver.common.by import By


class IngredientDetailsModalLocators:
    """Локаторы модального окна ингредиента."""

    MODAL = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]"
        "[.//h2[normalize-space()='Детали ингредиента']]",
    )
    TITLE = (By.XPATH, "//section[contains(@class, 'Modal_modal_opened')]//h2")
    INGREDIENT_NAME = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]//p[contains(@class, 'text_type_main-medium')]",
    )
    CLOSE_BUTTON = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]//button[contains(@class, 'Modal_modal__close')]",
    )
