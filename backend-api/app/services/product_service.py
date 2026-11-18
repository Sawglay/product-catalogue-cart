from app.errors import MyApplicationError
from app.models.product_dto import ProductDto
from app.models.product_list_dto import ProductListDto
from app.entities.product_repository_port import ProductRepositoryPort
from app.services.application_service import ApplicationService


class ProductService(ApplicationService):
    def __init__(self, product_repository: ProductRepositoryPort):
        super().__init__()
        self.product_repository = product_repository

    def list_products(
        self,
        category: str | None = None,
        tag: str | None = None,
        name: str | None = None,
        sort: str = "name:asc",
        block: int = 1,
        items: int = 20,
    ) -> ProductListDto:
        try:
            sort_field, sort_direction = sort.split(":")

            if sort_field not in ("name", "price") or sort_direction not in (
                "asc",
                "desc",
            ):
                raise MyApplicationError(400, "INVALID_SORT")

            tags = tag.split(":") if tag else []

            if (
                block < 1
                or items < 1
                or any(not value or len(value) > 100 for value in tags)
            ):
                raise MyApplicationError(400, "INVALID_REQUEST")

            products, total = self.product_repository.list_products(
                category,
                tags,
                name,
                sort_field,
                sort_direction,
                (block - 1) * items,
                items,
            )

            return ProductListDto(
                block=block,
                items=items,
                total=total,
                products=[ProductDto.from_entity(product) for product in products],
            )
        except Exception as exc:
            raise self.translate_error(exc) from exc

    def get_product(self, product_code: str) -> ProductDto:
        try:
            product = self.product_repository.get_by_code(product_code)
            if product is None:
                raise MyApplicationError(404, "PRODUCT_NOT_FOUND")
            return ProductDto.from_entity(product)
        except Exception as exc:
            raise self.translate_error(exc) from exc
