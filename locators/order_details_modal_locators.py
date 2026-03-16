"""Локаторы модального окна оформленного заказа."""

from selenium.webdriver.common.by import By


class OrderDetailsModalLocators:
    """Локаторы модального окна с номером заказа."""

    MODAL = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]"
        "[.//p[normalize-space()='идентификатор заказа']]",
    )
    ORDER_NUMBER = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]//h2",
    )
    CLOSE_BUTTON = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal_opened')]//button[contains(@class, 'Modal_modal__close')]",
    )
