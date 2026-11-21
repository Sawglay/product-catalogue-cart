"""Sanitised errors shared by persistence adapters."""


class DataLayerError(Exception):
    def __init__(self, message: str, error_code: str = "DATA_ERROR") -> None:
        super().__init__(message)
        self.error_code = error_code
