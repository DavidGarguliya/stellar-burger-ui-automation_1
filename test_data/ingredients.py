"""Тестовые данные ингредиентов для UI-тестов."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Ingredient:
    """Модель ингредиента для автотестов."""

    identifier: str
    name: str


CRATER_BUN = Ingredient(
    identifier="61c0c5a71d1f82001bdaaa6c",
    name="Краторная булка N-200i",
)
SPICY_SAUCE = Ingredient(
    identifier="61c0c5a71d1f82001bdaaa72",
    name="Соус Spicy-X",
)
LUMINESCENT_FILLING = Ingredient(
    identifier="61c0c5a71d1f82001bdaaa6e",
    name="Филе Люминесцентного тетраодонтимформа",
)
