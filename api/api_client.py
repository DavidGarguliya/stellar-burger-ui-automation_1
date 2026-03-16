"""API-клиент для подготовки тестовых данных."""

from dataclasses import dataclass
from uuid import uuid4

import allure
import requests

from config.settings import BASE_URL
from reporting.allure_reporter import attach_json, mask_secret


@dataclass(frozen=True, slots=True)
class TestUser:
    """Модель тестового пользователя."""

    email: str
    password: str
    name: str
    access_token: str
    refresh_token: str


class ApiClient:
    """Клиент для работы с API Stellar Burgers."""

    def __init__(self):
        """Инициализирует клиент и базовый URL."""

        self.base_api_url = f"{BASE_URL}/api"

    @allure.step("Создать тестового пользователя через API")
    def create_user(self) -> TestUser:
        """Создаёт тестового пользователя через API."""

        email = f"ui_autotest_{uuid4().hex[:12]}@example.com"
        password = "Password123!"
        payload = {
            "email": email,
            "password": password,
            "name": "UI Autotest",
        }
        request_data = {
            "url": f"{self.base_api_url}/auth/register",
            "payload": payload,
        }
        attach_json("Запрос на создание пользователя", request_data)
        response = requests.post(request_data["url"], json=payload, timeout=10)
        response.raise_for_status()
        body = response.json()
        attach_json(
            "Ответ API на создание пользователя",
            {
                "status_code": response.status_code,
                "body": {
                    "success": body["success"],
                    "user": body["user"],
                    "accessToken": mask_secret(body["accessToken"]),
                    "refreshToken": mask_secret(body["refreshToken"]),
                },
            },
        )
        return TestUser(
            email=email,
            password=password,
            name=payload["name"],
            access_token=body["accessToken"],
            refresh_token=body["refreshToken"],
        )

    @allure.step("Удалить тестового пользователя через API")
    def delete_user(self, user: TestUser):
        """Удаляет тестового пользователя через API."""

        request_data = {
            "url": f"{self.base_api_url}/auth/user",
            "headers": {"Authorization": mask_secret(user.access_token)},
            "email": user.email,
        }
        attach_json("Запрос на удаление пользователя", request_data)
        response = requests.delete(
            request_data["url"],
            headers={"Authorization": user.access_token},
            timeout=10,
        )
        response.raise_for_status()
        attach_json(
            "Ответ API на удаление пользователя",
            {
                "status_code": response.status_code,
                "body": response.json(),
            },
        )
