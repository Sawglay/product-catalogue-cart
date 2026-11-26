class MyApplicationError(Exception):
    """Safe error shared by the application and presentation layers."""

    def __init__(self, http_response_code: int, error_code: str):
        super().__init__(error_code)
        self.http_response_code = http_response_code
        self.error_code = error_code
