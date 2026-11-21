from typing import Annotated

from fastapi import APIRouter, Path, Query

from app.models.product_dto import ProductDto
from app.models.product_list_dto import ProductListDto
from app.services.product_service import ProductService


class ProductsRoutes:
    """Validate HTTP input and delegate catalogue use cases."""

    def __init__(self, service: ProductService):
        self.service = service
        self.router = APIRouter(prefix="/products", tags=["products"])
        self.router.add_api_route(
            "", self.list_products, methods=["GET"], response_model=ProductListDto
        )
        self.router.add_api_route(
            "/{product_code}",
            self.get_product,
            methods=["GET"],
            response_model=ProductDto,
        )

    def list_products(
        self,
        category: Annotated[
            str | None, Query(min_length=1, max_length=100, pattern=r"^\S+$")
        ] = None,
        tag: Annotated[
            str | None, Query(min_length=1, pattern=r"^[^\s:]{1,100}(:[^\s:]{1,100})*$")
        ] = None,
        name: Annotated[str | None, Query(min_length=1, max_length=255)] = None,
        sort: Annotated[str, Query(pattern=r"^(name|price):(asc|desc)$")] = "name:asc",
        block: Annotated[int, Query(ge=1, le=2147483647)] = 1,
        items: Annotated[int, Query(ge=1, le=2147483647)] = 20,
    ) -> ProductListDto:
        return self.service.list_products(category, tag, name, sort, block, items)

    def get_product(
        self,
        product_code: Annotated[
            str, Path(min_length=1, max_length=25, pattern=r"^\S+$")
        ],
    ) -> ProductDto:
        return self.service.get_product(product_code)
