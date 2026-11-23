from pydantic import BaseModel

from app.entities.cart import Cart
from app.models.cart_item_dto import CartItemDto
from app.models.cart_total_dto import CartTotalDto


class CartDto(BaseModel):
    code: str
    items: list[CartItemDto]
    totals: list[CartTotalDto]

    @classmethod
    def from_entity(cls, cart: Cart) -> "CartDto":
        return cls(
            code=cart.code,
            items=[CartItemDto.from_entity(item) for item in cart.items],
            totals=[
                CartTotalDto(currency=currency, amount=format(amount, ".2f"))
                for currency, amount in sorted(cart.totals().items())
            ],
        )
