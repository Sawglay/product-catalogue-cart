from pydantic import BaseModel


class CartCheckoutResponseDto(BaseModel):
    message: str
