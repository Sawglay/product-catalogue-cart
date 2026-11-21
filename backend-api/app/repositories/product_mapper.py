"""Shared SQL projection and hydration for catalogue and cart reads."""

from app.entities.product import Product
from app.entities.category import Category
from app.entities.tag import Tag
from app.entities.currency import Currency
from datetime import datetime


class ProductMapper:
    def select_sql(self) -> str:
        return """
            SELECT p.id, p.code, p.name, p.description, p.unit_price,
                   p.created_timestamp, p.updated_timestamp,
                   c.id AS currency_id, c.code AS currency_code,
                   c.name AS currency_name, c.symbol AS currency_symbol,
                   c.created_timestamp AS currency_created_timestamp,
                   c.updated_timestamp AS currency_updated_timestamp,
                   ARRAY(SELECT jsonb_build_object('id', cat.id, 'code', cat.code,
                             'created_timestamp', cat.created_timestamp,
                             'updated_timestamp', cat.updated_timestamp)
                         FROM product_categories pc
                         JOIN categories cat ON cat.id = pc.category_id
                         WHERE pc.product_id = p.id ORDER BY cat.code) AS categories,
                   ARRAY(SELECT jsonb_build_object('id', tag.id, 'code', tag.code,
                             'created_timestamp', tag.created_timestamp,
                             'updated_timestamp', tag.updated_timestamp)
                         FROM product_tags pt
                         JOIN tags tag ON tag.id = pt.tag_id
                         WHERE pt.product_id = p.id ORDER BY tag.code) AS tags
            FROM products p JOIN currencies c ON c.id = p.currency_id
        """

    def from_row(self, row) -> Product:
        categories = [Category(**self._reference_fields(category)) for category in row["categories"]]
        tags = [Tag(**self._reference_fields(tag)) for tag in row["tags"]]
        currency = Currency(
            row["currency_id"], row["currency_code"], row["currency_name"], row["currency_symbol"],
            row["currency_created_timestamp"], row["currency_updated_timestamp"])
        return Product(
            **{field: row[field] for field in (
                "id", "code", "name", "description", "unit_price",
                "created_timestamp", "updated_timestamp")},
            categories=categories, tags=tags, currency=currency)

    def _reference_fields(self, row) -> dict:
        fields = dict(row)
        # PostgreSQL JSON timestamps decode as strings, unlike native timestamptz columns.
        for field in ("created_timestamp", "updated_timestamp"):
            if fields[field] is not None:
                fields[field] = datetime.fromisoformat(fields[field])
        return fields
