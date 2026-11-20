"""Nominal domain port for session-owned cart persistence."""

from abc import ABC, abstractmethod
from app.entities.cart import Cart


class CartRepositoryPort(ABC):
    @abstractmethod
    def get_by_session(self, session: str) -> Cart | None:
        pass

    @abstractmethod
    def get_by_code_for_session(self, code: str, session: str) -> Cart | None:
        pass

    @abstractmethod
    def create(self, code: str, session: str) -> Cart:
        pass

    @abstractmethod
    def add_item(self, code: str, session: str, product_id: int, quantity: int) -> Cart:
        pass

    @abstractmethod
    def set_quantity(self, code: str, session: str, product_code: str, quantity: int) -> Cart:
        pass

    @abstractmethod
    def delete(self, code: str, session: str) -> bool:
        pass
