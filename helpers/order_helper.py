"""Вспомогательные функции для тестов заказов без прямого взаимодействия со страницами."""

import allure

from reporting.allure_reporter import attach_text


@allure.step("Привести номер заказа к формату ленты")
def format_order_number(order_number: int) -> str:
    """Приводит номер заказа к формату, который отображается в ленте."""

    return f"{order_number:07d}"


@allure.step("Сохранить номер созданного заказа в отчёт")
def attach_created_order_number(order_number: int):
    """Прикладывает номер созданного заказа в Allure."""

    attach_text("Номер созданного заказа", str(order_number))


@allure.step("Сохранить форматированный номер заказа в отчёт")
def attach_formatted_order_number(formatted_order_number: str):
    """Прикладывает форматированный номер заказа в Allure."""

    attach_text("Форматированный номер заказа для ленты", formatted_order_number)


@allure.step("Сохранить значение счётчика заказов в отчёт")
def attach_order_counter_value(counter_name: str, value: int, stage: str):
    """Прикладывает значение счётчика заказов в Allure."""

    attach_text(f"{counter_name} {stage}", str(value))
