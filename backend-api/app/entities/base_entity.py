"""Shared database identity and UTC timestamps."""

from datetime import datetime, timezone


class BaseEntity:
    def __init__(self, id: int, created_timestamp: datetime | None = None,
                 updated_timestamp: datetime | None = None) -> None:
        if isinstance(id, bool) or not isinstance(id, int) or id <= 0:
            raise ValueError("Entity identity must be a positive integer.")
        self.id = id
        self.created_timestamp = self._utc(created_timestamp or datetime.now(timezone.utc))
        self.updated_timestamp = self._utc(updated_timestamp) if updated_timestamp else None

    def _utc(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Timestamps must include a UTC offset.")
        return value.astimezone(timezone.utc)

    def touch(self) -> None:
        self.updated_timestamp = datetime.now(timezone.utc)
