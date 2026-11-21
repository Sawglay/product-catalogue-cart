"""Connection lifecycle shared by PostgreSQL persistence adapters."""

from psycopg_pool import ConnectionPool
from app.repositories.data_layer_error import DataLayerError


class BaseRepository:
    def __init__(self, connection_string: str) -> None:
        self.pool = ConnectionPool(conninfo=connection_string, min_size=1, max_size=5)

    def check_connection(self) -> bool:
        try:
            with self.pool.connection() as connection:
                return connection.execute("SELECT 1").fetchone() == (1,)
        except Exception:
            return False

    def close(self) -> None:
        self.pool.close()
