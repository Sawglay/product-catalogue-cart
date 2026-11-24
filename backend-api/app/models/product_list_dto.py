from pydantic import BaseModel

from app.models.product_dto import ProductDto


class ProductListDto(BaseModel):
    block: int
    items: int
    total: int
    products: list[ProductDto]
