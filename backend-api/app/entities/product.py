"""Product aggregate with categories, tags and currency value semantics."""

from datetime import datetime
from decimal import Decimal
from app.entities.base_entity import BaseEntity
from app.entities.category import Category
from app.entities.tag import Tag
from app.entities.currency import Currency


class Product(BaseEntity):
    def __init__(self, id: int, code: str, name: str, description: str,
                 categories: list[Category], tags: list[Tag], unit_price: Decimal,
                 currency: Currency,
                 created_timestamp: datetime | None = None,
                 updated_timestamp: datetime | None = None) -> None:
        super().__init__(id, created_timestamp, updated_timestamp)
        if not code or len(code) > 25 or not name or len(name) > 255:
            raise ValueError("Product code or name is invalid.")
        if not isinstance(description, str) or not categories or not tags:
            raise ValueError("Product description, categories and tags are required.")
        if not all(isinstance(category, Category) for category in categories):
            raise ValueError("Product categories must be Category objects.")
        if not all(isinstance(tag, Tag) for tag in tags):
            raise ValueError("Product tags must be Tag objects.")
        if not isinstance(unit_price, Decimal) or not unit_price.is_finite():
            raise ValueError("Price must be a finite Decimal.")
        if unit_price < 0 or unit_price != unit_price.quantize(Decimal("0.01")):
            raise ValueError("Price must be non-negative with at most two decimal places.")
        if not isinstance(currency, Currency):
            raise ValueError("Currency is required.")
        self.code = code
        self.name = name
        self.description = description
        self.categories = list(categories)
        self.tags = list(tags)
        self.unit_price = unit_price.quantize(Decimal("0.01"))
        self.currency = currency
