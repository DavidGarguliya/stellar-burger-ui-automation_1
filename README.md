# Diplom_3

UI-автотесты для веб-приложения Stellar Burgers: <https://stellarburgers.education-services.ru/>

Проект реализован в рамках дипломного задания по автоматизации UI. Тесты покрывают основную функциональность конструктора бургеров и раздела «Лента заказов», построены по паттерну Page Object, запускаются в `Google Chrome` и `Mozilla Firefox`, а результаты выполнения оформляются в подробный `Allure`-отчёт на русском языке.

## Что проверяется

- переход по клику на раздел «Конструктор»;
- переход по клику на раздел «Лента заказов»;
- открытие модального окна ингредиента;
- закрытие модального окна по крестику;
- увеличение счётчика ингредиента после добавления в заказ;
- увеличение счётчика «Выполнено за всё время» после оформления заказа;
- увеличение счётчика «Выполнено за сегодня» после оформления заказа;
- появление номера нового заказа в блоке «В работе».

## Стек

- `Python`
- `pytest`
- `selenium`
- `requests`
- `allure-pytest`

## Структура проекта

```text
Diplom_3/
├── api/             # API-клиент для подготовки тестовых пользователей
├── browser/         # Фабрика браузеров и настройки WebDriver
├── config/          # Базовые настройки проекта
├── helpers/         # Вспомогательные функции без page interactions
├── locators/        # Локаторы страниц и модальных окон
├── pages/           # Page Object классы
├── reporting/       # Логика формирования Allure-артефактов
├── test_data/       # Тестовые данные и модели ингредиентов
├── tests/           # UI-тесты и pytest-фикстуры
├── allure_results/  # Результаты выполнения для Allure
├── pytest.ini       # Конфигурация pytest
├── requirements.txt # Зависимости проекта
└── README.md
```

## Назначение каталогов

### `tests`

Содержит только тестовые сценарии и общий файл фикстур [tests/conftest.py](tests/conftest.py).

- [tests/test_navigation.py](tests/test_navigation.py) — проверки навигации между разделами.
- [tests/test_ingredient_modal.py](tests/test_ingredient_modal.py) — проверки модального окна ингредиента.
- [tests/test_constructor_counter.py](tests/test_constructor_counter.py) — проверка счётчика ингредиента.
- [tests/test_order_feed.py](tests/test_order_feed.py) — проверки ленты заказов и счётчиков.

### `pages`

Page Object классы для страниц и модальных окон.

- [pages/base_page.py](pages/base_page.py)
- [pages/constructor_page.py](pages/constructor_page.py)
- [pages/feed_page.py](pages/feed_page.py)
- [pages/header_page.py](pages/header_page.py)
- [pages/ingredient_details_modal_page.py](pages/ingredient_details_modal_page.py)
- [pages/order_details_modal_page.py](pages/order_details_modal_page.py)

### `locators`

Отдельные файлы с локаторами, используемыми Page Object классами.

### `helpers`

Вспомогательные функции для форматирования и вложений в отчёт.

- [helpers/order_helper.py](helpers/order_helper.py)

### `api`

- [api/api_client.py](api/api_client.py) — создание и удаление тестовых пользователей через API.

### `browser`

- [browser/browser_factory.py](browser/browser_factory.py) — создание драйверов `Chrome` и `Firefox`.

### `config`

- [config/settings.py](config/settings.py) — URL стенда, параметры окна браузера и имена переменных окружения для бинарников браузеров.

### `reporting`

- [reporting/allure_reporter.py](reporting/allure_reporter.py) — вложения, environment, executor и диагностические артефакты Allure.
- [reporting/suite_metadata.py](reporting/suite_metadata.py) — русские имена suite-уровней в отчёте.

### `test_data`

- [test_data/ingredients.py](test_data/ingredients.py) — тестовые ингредиенты и связанные модели данных.

## Требования

- `Python 3.12+` или совместимая версия;
- установленный `Google Chrome`;
- установленный `Mozilla Firefox`;
- доступ к интернету для работы со стендом и API;
- установленный `Allure CLI`, если нужен HTML-отчёт через `allure serve` или `allure generate`.

## Установка

### 1. Клонирование репозитория

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd Diplom_3
```

### 2. Создание виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск тестов

По умолчанию тесты параметризованы по двум браузерам: `chrome` и `firefox`.

### Запуск всего набора

```bash
pytest
```

### Запуск одного файла

```bash
pytest tests/test_navigation.py
```

### Запуск отдельного сценария по маске

```bash
pytest tests/test_order_feed.py -k in_progress
```

### Тихий запуск

```bash
pytest -q
```

## Настройка браузеров

Драйверы поднимаются через `Selenium Manager`, поэтому жёсткие пути к браузерам не требуются.

Если браузер установлен в нестандартное место, можно передать путь через переменные окружения:

- `CHROME_BINARY`
- `FIREFOX_BINARY`

Пример для macOS/Linux:

```bash
export CHROME_BINARY="/path/to/chrome"
export FIREFOX_BINARY="/path/to/firefox"
pytest
```

## Allure-отчёт

В [pytest.ini](pytest.ini) уже настроен вывод результатов в каталог `allure_results`.

### Открыть отчёт после прогона

```bash
allure serve allure_results
```

### Сгенерировать статический отчёт

```bash
allure generate allure_results -o allure-report --clean
```

### Открыть статический отчёт

```bash
allure open allure-report
```

## Особенности реализации

- используется паттерн `Page Object`;
- для каждой страницы и модального окна создан отдельный класс;
- методы взаимодействия со страницами размещены внутри Page Object классов в пакете `pages`;
- локаторы вынесены в отдельный пакет;
- тесты разделены по функциональности;
- тесты независимы друг от друга;
- тестовые пользователи создаются через API перед тестом и удаляются после выполнения;
- авторизация подготавливается через `localStorage`, без прохождения UI-формы логина;
- Allure-отчёт включает шаги, вложения, browser context, storage, консоль и артефакты падения;
- результаты в Allure дополнительно разнесены по отдельным suite для `Google Chrome` и `Mozilla Firefox`;
- названия тестов, suite-уровней и описаний оформлены на русском языке.

## Полезные команды

### Проверка импорта и компиляции модулей

```bash
python3 -m compileall api browser config helpers reporting test_data tests pages locators
```

### Просмотр содержимого каталога с результатами Allure

```bash
ls allure_results
```

## Конфигурация pytest

Файл [pytest.ini](pytest.ini) содержит:

- `testpaths = tests`
- `python_files = test_*.py`
- `addopts = -ra --alluredir=allure_results`
- `pythonpath = .`
