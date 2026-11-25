"""Nominal domain port for catalogue persistence."""

from abc import ABC, abstractmethod
from app.entities.product import Product


class ProductRepositoryPort(ABC):
    @abstractmethod
    def list_products(self, category, tags, name, sort_field, sort_direction, offset, limit) -> tuple[list[Product], int]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Product | None:
        pass
