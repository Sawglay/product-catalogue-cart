from pydantic import BaseModel


class CartTotalDto(BaseModel):
    currency: str
    amount: str
