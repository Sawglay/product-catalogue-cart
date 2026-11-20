"""A cart line and its quantity invariant."""

from datetime import datetime
from app.entities.base_entity import BaseEntity
from app.entities.product import Product


class CartItem(BaseEntity):
    def __init__(self, id: int, product: Product, quantity: int,
                 created_timestamp: datetime | None = None,
                 updated_timestamp: datetime | None = None) -> None:
        super().__init__(id, created_timestamp, updated_timestamp)
        self.product = product
        self.validate_quantity(quantity)
        self.quantity = quantity

    def validate_quantity(self, quantity: int, allow_zero: bool = False) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < (0 if allow_zero else 1):
            raise ValueError("Quantity must be a positive integer (or zero for removal).")

    def set_quantity(self, quantity: int) -> None:
        self.validate_quantity(quantity)
        self.quantity = quantity
        self.touch()

    def line_total(self):
        return self.product.unit_price * self.quantity
