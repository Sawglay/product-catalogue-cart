"""Currency value semantics with inherited persistence metadata."""

from datetime import datetime
from app.entities.base_entity import BaseEntity


class Currency(BaseEntity):
    def __init__(self, id: int, code: str, name: str, symbol: str,
                 created_timestamp: datetime | None = None,
                 updated_timestamp: datetime | None = None) -> None:
        super().__init__(id, created_timestamp, updated_timestamp)
        if not code or len(code) > 4 or not name or len(name) > 150 or len(symbol) != 1:
            raise ValueError("Currency code, name and single-character symbol are required.")
        self._code = code
        self._name = name
        self._symbol = symbol

    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def symbol(self) -> str:
        return self._symbol

    def __eq__(self, other: object) -> bool:
        """Compare currency values independently of persistence identity."""
        if not isinstance(other, Currency):
            return NotImplemented
        return (self.code, self.name, self.symbol) == (other.code, other.name, other.symbol)
