"""Tag entity identified publicly by its code."""

from datetime import datetime
from app.entities.base_entity import BaseEntity


class Tag(BaseEntity):
    def __init__(self, id: int, code: str, created_timestamp: datetime | None = None,
                 updated_timestamp: datetime | None = None) -> None:
        super().__init__(id, created_timestamp, updated_timestamp)
        if not code or not code.strip() or len(code) > 100:
            raise ValueError("Tag code is required and must not exceed 100 characters.")
        self.code = code
