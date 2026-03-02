"""Общие фикстуры и хуки для UI-тестов."""

import allure
import pytest

from api.api_client import ApiClient
from browser.browser_factory import create_driver
from config.settings import BASE_URL
from pages.base_page import BasePage
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from reporting.allure_reporter import (
    attach_failure_artifacts,
    attach_post_test_artifacts,
    get_allure_results_dir,
    write_allure_metadata_files,
)
from reporting.suite_metadata import get_browser_suite_name, get_russian_suite_name


@pytest.fixture(params=["chrome", "firefox"], ids=["chrome", "firefox"])
def browser_name(request):
    """Возвращает имя браузера для параметризации тестов."""

    return request.param


def pytest_configure(config):
    """Подготавливает служебные файлы Allure перед запуском тестов."""

    allure_dir = get_allure_results_dir(config)
    if allure_dir:
        write_allure_metadata_files(allure_dir)


@pytest.fixture
def driver(browser_name):
    """Создаёт и завершает браузер для теста."""

    with allure.step(f"Запустить браузер {browser_name}"):
        driver_instance = create_driver(browser_name)
    yield driver_instance
    with allure.step(f"Завершить браузер {browser_name}"):
        BasePage(driver_instance).quit_browser()


@pytest.fixture
def api_client():
    """Возвращает API-клиент для работы с тестовыми данными."""

    return ApiClient()


@pytest.fixture
def test_user(api_client):
    """Создаёт и удаляет тестового пользователя через API."""

    user = api_client.create_user()
    allure.dynamic.parameter("Тестовый пользователь", user.email)
    yield user
    api_client.delete_user(user)


@pytest.fixture
def authorized_driver(driver, test_user):
    """Авторизует пользователя в браузере через localStorage."""

    constructor_page = ConstructorPage(driver)
    constructor_page.authorize_user(test_user)
    return constructor_page.driver


@pytest.fixture
def constructor_page(driver):
    """Открывает страницу конструктора."""

    return ConstructorPage(driver).open()


@pytest.fixture
def authorized_constructor_page(authorized_driver):
    """Открывает авторизованный конструктор."""

    return ConstructorPage(authorized_driver).open()


@pytest.fixture
def feed_page(driver):
    """Открывает страницу ленты заказов."""

    return FeedPage(driver).open()


@pytest.fixture
def active_driver(request):
    """Возвращает активный браузерный драйвер для вложений Allure."""

    if "authorized_driver" in request.fixturenames:
        return request.getfixturevalue("authorized_driver")
    if "driver" in request.fixturenames:
        return request.getfixturevalue("driver")
    return None


@pytest.fixture(autouse=True)
def configure_allure_context(request, browser_name):
    """Настраивает подробную иерархию и параметры Allure для каждого теста."""

    module_name = request.node.module.__name__.split(".")[-1]

    allure.dynamic.parent_suite("Диплом. Задание 3")
    allure.dynamic.suite(get_browser_suite_name(browser_name))
    allure.dynamic.sub_suite(get_russian_suite_name(module_name))
    allure.dynamic.epic("Stellar Burgers")
    allure.dynamic.tag("UI", "Selenium", "Allure", browser_name)
    allure.dynamic.link(BASE_URL, link_type="custom", name="Тестируемый стенд")
    allure.dynamic.parameter("Браузер", browser_name)


@pytest.fixture(autouse=True)
def attach_test_artifacts(request, active_driver):
    """Прикладывает диагностические вложения после завершения теста."""

    yield
    if active_driver:
        try:
            attach_post_test_artifacts(active_driver)
        except Exception:
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результат этапа выполнения теста."""

    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver") or item.funcargs.get("authorized_driver")
    if not driver:
        return

    try:
        attach_failure_artifacts(driver)
    except Exception:
        pass
