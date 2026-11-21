"""Parameterised catalogue reads with an allowlist for sort identifiers."""

from psycopg.rows import dict_row
from app.entities.product import Product
from app.entities.product_repository_port import ProductRepositoryPort
from app.repositories.base_repository import BaseRepository
from app.repositories.data_layer_error import DataLayerError
from app.repositories.product_mapper import ProductMapper


class ProductRepository(BaseRepository, ProductRepositoryPort):
    def list_products(self, category, tags, name, sort_field, sort_direction, offset, limit) -> tuple[list[Product], int]:
        if sort_field not in ("name", "price") or sort_direction not in ("asc", "desc"):
            raise DataLayerError("Invalid catalogue sort.", "INVALID_INPUT")
        if offset < 0 or limit < 1:
            raise DataLayerError("Invalid catalogue pagination.", "INVALID_INPUT")
        filters, parameters = [], []
        if category:
            filters.append("EXISTS (SELECT 1 FROM product_categories pc JOIN categories cat ON cat.id=pc.category_id WHERE pc.product_id=p.id AND cat.code=%s)")
            parameters.append(category)
        if tags:
            filters.append("EXISTS (SELECT 1 FROM product_tags pt JOIN tags tag ON tag.id=pt.tag_id WHERE pt.product_id=p.id AND tag.code=ANY(%s))")
            parameters.append(list(tags))
        if name:
            # strpos treats '%' and '_' literally: this is substring search, not a wildcard API.
            filters.append("strpos(lower(p.name), lower(%s)) > 0")
            parameters.append(name)
        where = " WHERE " + " AND ".join(filters) if filters else ""
        field = "p.name" if sort_field == "name" else "p.unit_price"
        direction = "ASC" if sort_direction == "asc" else "DESC"
        mapper = ProductMapper()
        try:
            with self.pool.connection() as connection:
                with connection.transaction():
                    # Both the count and block describe the same snapshot.
                    connection.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
                    with connection.cursor(row_factory=dict_row) as cursor:
                        cursor.execute("SELECT COUNT(*) AS total FROM products p" + where, parameters)
                        total = cursor.fetchone()["total"]
                        cursor.execute(mapper.select_sql() + where + f" ORDER BY {field} {direction}, p.code ASC LIMIT %s OFFSET %s", parameters + [limit, offset])
                        return [mapper.from_row(row) for row in cursor.fetchall()], total
        except Exception as exc:
            raise DataLayerError("Could not load products.") from exc

    def get_by_code(self, code: str) -> Product | None:
        mapper = ProductMapper()
        try:
            with self.pool.connection() as connection:
                with connection.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(mapper.select_sql() + " WHERE p.code=%s", (code,))
                    row = cursor.fetchone()
                    return mapper.from_row(row) if row else None
        except Exception as exc:
            raise DataLayerError("Could not load product.") from exc
