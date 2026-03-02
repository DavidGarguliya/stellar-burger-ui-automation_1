"""Базовый класс для объектов страниц."""

import allure
from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Базовый объект страницы."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """Инициализирует драйвер и ожидания."""

        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу {url}")
    def open_url(self, url: str):
        """Открывает переданный URL."""

        self.driver.get(url)

    @allure.step("Обновить текущую страницу")
    def refresh_page(self):
        """Обновляет текущую страницу."""

        self.driver.refresh()

    @allure.step("Завершить браузер")
    def quit_browser(self):
        """Завершает сессию браузера."""

        self.driver.quit()

    @allure.step("Получить текущий URL страницы")
    def get_current_url(self) -> str:
        """Возвращает текущий URL."""

        return self.driver.current_url

    @allure.step("Дождаться видимости элемента")
    def wait_for_visibility(self, locator):
        """Ожидает видимость элемента и возвращает его."""

        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Дождаться кликабельности элемента")
    def wait_for_clickable(self, locator):
        """Ожидает кликабельность элемента и возвращает его."""

        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Нажать на элемент")
    def click(self, locator):
        """Кликает по элементу."""

        self.wait_for_clickable(locator).click()

    @allure.step("Нажать на элемент через JavaScript")
    def js_click(self, locator):
        """Кликает по элементу через JavaScript."""

        element = self.scroll_to_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Выполнить JavaScript в браузере")
    def execute_script(self, script: str, *args):
        """Выполняет JavaScript и возвращает результат."""

        return self.driver.execute_script(script, *args)

    @allure.step("Получить текст элемента")
    def get_text(self, locator) -> str:
        """Возвращает текст элемента без лишних пробелов."""

        return self.wait_for_visibility(locator).text.strip()

    @allure.step("Дождаться исчезновения элемента")
    def wait_for_invisibility(self, locator) -> bool:
        """Ожидает исчезновение элемента."""

        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Проверить наличие элемента")
    def is_element_visible(self, locator, timeout: int = 3) -> bool:
        """Проверяет, что элемент видим за ограниченное время."""

        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return False
        return True

    @allure.step("Проверить наличие текста в текущем URL")
    def wait_for_url_contains(self, value: str):
        """Ожидает, что URL содержит указанный фрагмент."""

        self.wait.until(EC.url_contains(value))

    @allure.step("Прокрутить страницу к элементу")
    def scroll_to_element(self, locator):
        """Прокручивает страницу к элементу."""

        element = self.wait_for_visibility(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )
        return element

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_and_drop(self, source_locator, target_locator):
        """Перетаскивает элемент через HTML5 Drag and Drop API."""

        source = self.scroll_to_element(source_locator)
        target = self.wait_for_visibility(target_locator)
        script = """
            const source = arguments[0];
            const target = arguments[1];
            const dataTransfer = new DataTransfer();
            source.dispatchEvent(new DragEvent('dragstart', {dataTransfer, bubbles: true}));
            target.dispatchEvent(new DragEvent('dragenter', {dataTransfer, bubbles: true}));
            target.dispatchEvent(new DragEvent('dragover', {dataTransfer, bubbles: true}));
            target.dispatchEvent(new DragEvent('drop', {dataTransfer, bubbles: true}));
            source.dispatchEvent(new DragEvent('dragend', {dataTransfer, bubbles: true}));
        """
        self.driver.execute_script(script, source, target)
