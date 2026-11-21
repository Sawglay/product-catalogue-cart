"""Session-scoped cart transactions; cart row locks serialise mutations."""

from psycopg import IntegrityError
from psycopg.rows import dict_row
from app.entities.cart import Cart
from app.entities.cart_item import CartItem
from app.entities.cart_repository_port import CartRepositoryPort
from app.repositories.base_repository import BaseRepository
from app.repositories.data_layer_error import DataLayerError
from app.repositories.product_mapper import ProductMapper


class CartRepository(BaseRepository, CartRepositoryPort):
    def _load(self, connection, session: str, code: str | None = None, lock: bool = False) -> Cart | None:
        with connection.cursor(row_factory=dict_row) as cursor:
            query = "SELECT * FROM carts WHERE session=%s"
            parameters = [session]
            if code is not None:
                query += " AND code=%s"
                parameters.append(code)
            cursor.execute(query + (" FOR UPDATE" if lock else ""), parameters)
            row = cursor.fetchone()
            if row is None:
                return None
            mapper = ProductMapper()
            cursor.execute("""SELECT ci.id AS item_id, ci.quantity,
                    ci.created_timestamp AS item_created, ci.updated_timestamp AS item_updated,
                    product.* FROM cart_items ci
                JOIN carts cart ON cart.id=ci.cart_id
                JOIN LATERAL (""" + mapper.select_sql() + """ WHERE p.id=ci.product_id) product ON true
                WHERE cart.code=%s AND cart.session=%s ORDER BY product.code""", (row["code"], session))
            items = [CartItem(item["item_id"], mapper.from_row(item), item["quantity"],
                              item["item_created"], item["item_updated"]) for item in cursor.fetchall()]
            return Cart(row["id"], row["code"], row["session"], items,
                        row["created_timestamp"], row["updated_timestamp"])

    def get_by_session(self, session: str) -> Cart | None:
        try:
            with self.pool.connection() as connection:
                return self._load(connection, session, lock=True)
        except Exception as exc:
            raise DataLayerError("Could not load cart.") from exc

    def get_by_code_for_session(self, code: str, session: str) -> Cart | None:
        try:
            with self.pool.connection() as connection:
                return self._load(connection, session, code, lock=True)
        except Exception as exc:
            raise DataLayerError("Could not load cart.") from exc

    def create(self, code: str, session: str) -> Cart:
        # Validate even before writing; the database independently checks UUIDv7.
        Cart(1, code, session, [])
        try:
            with self.pool.connection() as connection:
                with connection.transaction():
                    connection.execute("INSERT INTO carts(code, session) VALUES (%s,%s) ON CONFLICT(session) DO NOTHING", (code, session))
                    return self._load(connection, session, lock=True)
        except IntegrityError as exc:
            raise DataLayerError("Cart conflicts with stored data.", "DATA_CONFLICT") from exc
        except Exception as exc:
            raise DataLayerError("Could not create cart.") from exc

    def add_item(self, code: str, session: str, product_id: int, quantity: int) -> Cart:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
            raise DataLayerError("Quantity must be positive.", "INVALID_INPUT")
        try:
            with self.pool.connection() as connection:
                with connection.transaction():
                    cart = self._load(connection, session, code, lock=True)
                    if cart is None:
                        raise DataLayerError("Cart not found.", "CART_NOT_FOUND")
                    connection.execute("""INSERT INTO cart_items(cart_id, product_id, quantity)
                        SELECT id,%s,%s FROM carts WHERE code=%s AND session=%s
                        ON CONFLICT(cart_id,product_id) DO UPDATE
                        SET quantity=cart_items.quantity+EXCLUDED.quantity, updated_timestamp=CURRENT_TIMESTAMP""", (product_id, quantity, code, session))
                    connection.execute("UPDATE carts SET updated_timestamp=CURRENT_TIMESTAMP WHERE code=%s AND session=%s", (code, session))
                    return self._load(connection, session, code)
        except DataLayerError:
            raise
        except IntegrityError as exc:
            raise DataLayerError("Cart item conflicts with stored data.", "DATA_CONFLICT") from exc
        except Exception as exc:
            raise DataLayerError("Could not add cart item.") from exc

    def set_quantity(self, code: str, session: str, product_code: str, quantity: int) -> Cart:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            raise DataLayerError("Quantity cannot be negative.", "INVALID_INPUT")
        try:
            with self.pool.connection() as connection:
                with connection.transaction():
                    cart = self._load(connection, session, code, lock=True)
                    if cart is None:
                        raise DataLayerError("Cart not found.", "CART_NOT_FOUND")
                    if quantity == 0:
                        result = connection.execute("""DELETE FROM cart_items ci USING carts c, products p
                            WHERE ci.cart_id=c.id AND ci.product_id=p.id
                            AND c.code=%s AND c.session=%s AND p.code=%s""", (code, session, product_code))
                    else:
                        result = connection.execute("""UPDATE cart_items ci SET quantity=%s, updated_timestamp=CURRENT_TIMESTAMP
                            FROM carts c, products p WHERE ci.cart_id=c.id AND ci.product_id=p.id
                            AND c.code=%s AND c.session=%s AND p.code=%s""", (quantity, code, session, product_code))
                    if result.rowcount == 0:
                        raise DataLayerError("Cart item not found.", "CART_ITEM_NOT_FOUND")
                    connection.execute("UPDATE carts SET updated_timestamp=CURRENT_TIMESTAMP WHERE code=%s AND session=%s", (code, session))
                    return self._load(connection, session, code)
        except DataLayerError:
            raise
        except IntegrityError as exc:
            raise DataLayerError("Cart item conflicts with stored data.", "DATA_CONFLICT") from exc
        except Exception as exc:
            raise DataLayerError("Could not update cart item.") from exc

    def delete(self, code: str, session: str) -> bool:
        try:
            with self.pool.connection() as connection:
                with connection.transaction():
                    return connection.execute("DELETE FROM carts WHERE code=%s AND session=%s", (code, session)).rowcount > 0
        except Exception as exc:
            raise DataLayerError("Could not delete cart.") from exc
