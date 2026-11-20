"""Session-owned cart domain entity."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.entities.base_entity import BaseEntity
from app.entities.cart_item import CartItem
from app.entities.product import Product


class Cart(BaseEntity):
    def __init__(self, id: int, code: str, session: str, items: list[CartItem],
                 created_timestamp: datetime | None = None,
                 updated_timestamp: datetime | None = None) -> None:
        super().__init__(id, created_timestamp, updated_timestamp)
        if UUID(code).version != 7 or len(code) != 36:
            raise ValueError("Cart code must be a UUIDv7.")
        if not session or not session.strip():
            raise ValueError("A session is required.")
        self.code = code
        self.session = session
        self.items = list(items)

    def add_item(self, product: Product, quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise ValueError("Quantity must be a positive integer.")
        for item in self.items:
            if item.product.code == product.code:
                item.set_quantity(item.quantity + quantity)
                break
        else:
            # This identity is transient; persistence assigns the saved line's identity.
            transient_id = max((item.id for item in self.items), default=0) + 1
            self.items.append(CartItem(transient_id, product, quantity))
        self.touch()

    def set_quantity(self, product_code: str, quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")
        for item in self.items:
            if item.product.code == product_code:
                if quantity == 0:
                    self.items.remove(item)
                else:
                    item.set_quantity(quantity)
                self.touch()
                return
        raise ValueError("Cart item not found.")

    def totals(self) -> dict[str, Decimal]:
        totals = {}
        for item in self.items:
            currency = item.product.currency.code
            totals[currency] = totals.get(currency, Decimal("0.00")) + item.line_total()
        return totals
