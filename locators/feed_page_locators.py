"""Локаторы страницы ленты заказов."""

from selenium.webdriver.common.by import By


class FeedPageLocators:
    """Локаторы страницы ленты заказов."""

    PAGE_HEADING = (By.XPATH, "//h1[normalize-space()='Лента заказов']")
    ORDER_FEED_LIST = (By.CSS_SELECTOR, "ul[class*='OrderFeed_list']")
    ALL_TIME_TOTAL = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за все время:']/following-sibling::p[1]",
    )
    TODAY_TOTAL = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за сегодня:']/following-sibling::p[1]",
    )
    READY_ORDERS_LIST = (
        By.XPATH,
        "//p[normalize-space()='Готовы:']/following-sibling::ul[1]",
    )
    IN_PROGRESS_ORDERS_LIST = (
        By.XPATH,
        "//p[normalize-space()='В работе:']/following-sibling::ul[1]",
    )

    @staticmethod
    def order_card(order_number: str):
        """Возвращает локатор карточки заказа по его номеру."""

        return (
            By.XPATH,
            f"//a[contains(@href, '/feed/') and .//p[contains(normalize-space(), '#{order_number}')]]",
        )

    @staticmethod
    def order_in_ready_list(order_number: str):
        """Возвращает локатор номера заказа в списке готовых."""

        return (
            By.XPATH,
            f"//p[normalize-space()='Готовы:']/following-sibling::ul[1]/li[normalize-space()='{order_number}']",
        )

    @staticmethod
    def order_in_progress_list(order_number: str):
        """Возвращает локатор номера заказа в списке в работе."""

        return (
            By.XPATH,
            f"//p[normalize-space()='В работе:']/following-sibling::ul[1]/li[normalize-space()='{order_number}']",
        )
