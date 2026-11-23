from pydantic import BaseModel

from app.entities.cart_item import CartItem


class CartItemDto(BaseModel):
    productCode: str
    name: str
    unitPrice: str
    currency: str
    quantity: int
    lineTotal: str

    @classmethod
    def from_entity(cls, item: CartItem) -> "CartItemDto":
        return cls(
            productCode=item.product.code,
            name=item.product.name,
            unitPrice=format(item.product.unit_price, ".2f"),
            currency=item.product.currency.code,
            quantity=item.quantity,
            lineTotal=format(item.product.unit_price * item.quantity, ".2f"),
        )
