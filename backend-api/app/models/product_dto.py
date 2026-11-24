from pydantic import BaseModel

from app.entities.product import Product
from app.models.currency_dto import CurrencyDto


class ProductDto(BaseModel):
    code: str
    name: str
    description: str
    categories: list[str]
    tags: list[str]
    unitPrice: str
    currency: CurrencyDto

    @classmethod
    def from_entity(cls, product: Product) -> "ProductDto":
        return cls(
            code=product.code,
            name=product.name,
            description=product.description,
            categories=[category.code for category in product.categories],
            tags=[tag.code for tag in product.tags],
            unitPrice=format(product.unit_price, ".2f"),
            currency=CurrencyDto(
                code=product.currency.code,
                name=product.currency.name,
                symbol=product.currency.symbol,
            ),
        )
