"""Метаданные и справочники для структуры Allure-отчёта."""


TEST_SUITES = {
    "test_navigation": "Навигация",
    "test_ingredient_modal": "Модальное окно ингредиента",
    "test_constructor_counter": "Конструктор и счётчики",
    "test_order_feed": "Лента заказов",
}

BROWSER_SUITES = {
    "chrome": "Google Chrome",
    "firefox": "Mozilla Firefox",
}


def get_russian_suite_name(module_name: str) -> str:
    """Возвращает русское название suite по имени тестового модуля."""

    return TEST_SUITES.get(module_name, "UI автотесты")


def get_browser_suite_name(browser_name: str) -> str:
    """Возвращает человекочитаемое имя браузера для suite-уровня Allure."""

    return BROWSER_SUITES.get(browser_name, browser_name)
