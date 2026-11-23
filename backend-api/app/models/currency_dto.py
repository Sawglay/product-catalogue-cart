from pydantic import BaseModel


class CurrencyDto(BaseModel):
    code: str
    name: str
    symbol: str
