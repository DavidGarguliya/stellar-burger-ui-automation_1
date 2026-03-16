"""Вспомогательные функции для подробного Allure-отчёта."""

from __future__ import annotations

import json
import platform
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

import allure

from config.settings import BASE_URL


def encode_java_properties_value(value: str) -> str:
    """Кодирует строку в формат, совместимый с Java properties."""

    return value.encode("unicode_escape").decode("ascii")


def encode_java_properties_key(key: str) -> str:
    """Кодирует ключ для формата Java properties с сохранением пробелов."""

    return encode_java_properties_value(key).replace(" ", "\\ ")


def attach_text(name: str, content: str):
    """Прикладывает текстовое вложение в отчёт."""

    allure.attach(
        content,
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )


def attach_json(name: str, payload: Any):
    """Прикладывает JSON-вложение в отчёт."""

    allure.attach(
        json.dumps(payload, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_html(name: str, content: str):
    """Прикладывает HTML-вложение в отчёт."""

    allure.attach(
        content,
        name=name,
        attachment_type=allure.attachment_type.HTML,
    )


def mask_secret(value: str, visible: int = 8) -> str:
    """Маскирует секрет, оставляя только начало и конец."""

    if len(value) <= visible * 2:
        return "*" * len(value)
    return f"{value[:visible]}...{value[-visible:]}"


def build_browser_context(driver) -> dict[str, Any]:
    """Собирает контекст текущего браузера."""

    capabilities = driver.capabilities
    window_size = driver.get_window_size()
    return {
        "browserName": capabilities.get("browserName"),
        "browserVersion": capabilities.get("browserVersion"),
        "platformName": capabilities.get("platformName"),
        "currentUrl": driver.current_url,
        "windowSize": window_size,
        "sessionId": driver.session_id,
    }


def attach_browser_context(driver):
    """Прикладывает контекст браузера."""

    attach_json("Контекст браузера", build_browser_context(driver))


def build_storage_state(driver) -> dict[str, Any]:
    """Собирает состояние localStorage, sessionStorage и cookies."""

    local_storage = driver.execute_script(
        """
        const snapshot = {};
        for (let index = 0; index < window.localStorage.length; index += 1) {
            const key = window.localStorage.key(index);
            snapshot[key] = window.localStorage.getItem(key);
        }
        return snapshot;
        """
    )
    session_storage = driver.execute_script(
        """
        const snapshot = {};
        for (let index = 0; index < window.sessionStorage.length; index += 1) {
            const key = window.sessionStorage.key(index);
            snapshot[key] = window.sessionStorage.getItem(key);
        }
        return snapshot;
        """
    )
    return {
        "currentUrl": driver.current_url,
        "localStorage": local_storage,
        "sessionStorage": session_storage,
        "cookies": driver.get_cookies(),
    }


def attach_storage_state(driver):
    """Прикладывает состояние хранилищ браузера."""

    attach_json("Состояние браузерных хранилищ", build_storage_state(driver))


def attach_browser_console(driver):
    """Прикладывает консоль браузера, если браузер поддерживает логи."""

    try:
        console_logs = driver.get_log("browser")
    except Exception:
        return

    if console_logs:
        attach_json("Логи консоли браузера", console_logs)


def attach_failure_artifacts(driver):
    """Прикладывает полный набор артефактов при падении теста."""

    allure.attach(
        driver.get_screenshot_as_png(),
        name="Скриншот при падении",
        attachment_type=allure.attachment_type.PNG,
    )
    attach_text("Текущий URL при падении", driver.current_url)
    attach_browser_context(driver)
    attach_storage_state(driver)
    attach_browser_console(driver)
    attach_html("HTML страницы при падении", driver.page_source)


def attach_post_test_artifacts(driver):
    """Прикладывает артефакты после завершения теста."""

    attach_text("Текущий URL после теста", driver.current_url)
    attach_browser_context(driver)
    attach_storage_state(driver)
    attach_browser_console(driver)


def get_allure_results_dir(config) -> Path | None:
    """Возвращает директорию с результатами Allure."""

    allure_dir = config.getoption("--alluredir")
    if not allure_dir:
        return None
    return Path(allure_dir)


def write_allure_metadata_files(allure_dir: Path):
    """Создаёт служебные файлы Allure с метаданными запуска."""

    allure_dir.mkdir(parents=True, exist_ok=True)

    environment_values = {
        "Проект": "Stellar Burgers",
        "Задание": "Диплом. UI-автотесты",
        "Базовый URL": BASE_URL,
        "Python": sys.version.split()[0],
        "Pytest": version("pytest"),
        "Selenium": version("selenium"),
        "Allure Pytest": version("allure-pytest"),
        "Операционная система": platform.platform(),
    }
    environment_lines = [
        f"{encode_java_properties_key(key)}={encode_java_properties_value(value)}"
        for key, value in environment_values.items()
    ]
    (allure_dir / "environment.properties").write_text(
        "\n".join(environment_lines),
        encoding="ascii",
    )

    categories = [
        {
            "name": "Известное ограничение стенда",
            "matchedStatuses": ["skipped"],
            "messageRegex": ".*текущий стенд почти мгновенно переводит новый заказ.*",
        },
        {
            "name": "Падение UI-проверки",
            "matchedStatuses": ["failed"],
            "traceRegex": ".*selenium.*|.*AssertionError.*",
        },
    ]
    (allure_dir / "categories.json").write_text(
        json.dumps(categories, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    executor = {
        "name": "Локальный запуск тестов",
        "type": "local",
        "buildName": "Диплом. Задание 3",
        "buildUrl": BASE_URL,
        "reportName": "Подробный Allure-отчёт UI автотестов",
    }
    (allure_dir / "executor.json").write_text(
        json.dumps(executor, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
