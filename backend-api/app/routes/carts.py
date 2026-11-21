from typing import Annotated

from fastapi import APIRouter, Header, Path, Response

from app.models.add_cart_item_request_dto import AddCartItemRequestDto
from app.models.cart_dto import CartDto
from app.models.cart_checkout_response_dto import CartCheckoutResponseDto
from app.models.set_cart_quantity_request_dto import SetCartQuantityRequestDto
from app.services.cart_service import CartService


class CartsRoutes:
    """Session-scoped cart routes; services enforce cart ownership."""

    def __init__(self, service: CartService):
        self.service = service
        self.router = APIRouter(prefix="/carts", tags=["carts"])
        self.router.add_api_route(
            "",
            self.create_cart,
            methods=["POST"],
            response_model=CartDto,
            status_code=201,
            responses={200: {"model": CartDto, "description": "Existing session cart"}},
        )

        self.router.add_api_route(
            "/{cart_code}", self.get_cart, methods=["GET"], response_model=CartDto
        )

        self.router.add_api_route(
            "/{cart_code}/items",
            self.add_item,
            methods=["POST"],
            response_model=CartDto,
        )

        self.router.add_api_route(
            "/{cart_code}/items/{product_code}",
            self.set_quantity,
            methods=["PUT"],
            response_model=CartDto,
        )
        
        self.router.add_api_route(
            "/{cart_code}/checkout",
            self.checkout,
            methods=["POST"],
            response_model=CartCheckoutResponseDto,
        )

    def create_cart(
        self,
        response: Response,
        session: Annotated[
            str, Header(alias="X-Session-Code", min_length=1, pattern=r"^.*\S.*$")
        ],
    ) -> CartDto:
        cart, created = self.service.create_cart(session)
        response.status_code = 201 if created else 200
        return cart

    def get_cart(
        self,
        cart_code: Annotated[
            str,
            Path(
                min_length=36,
                max_length=36,
                pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-7[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
            ),
        ],
        session: Annotated[
            str, Header(alias="X-Session-Code", min_length=1, pattern=r"^.*\S.*$")
        ],
    ) -> CartDto:
        return self.service.get_cart(cart_code, session)

    def add_item(
        self,
        request: AddCartItemRequestDto,
        cart_code: Annotated[
            str,
            Path(
                min_length=36,
                max_length=36,
                pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-7[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
            ),
        ],
        session: Annotated[
            str, Header(alias="X-Session-Code", min_length=1, pattern=r"^.*\S.*$")
        ],
    ) -> CartDto:
        return self.service.add_item(
            cart_code, session, request.productCode, request.quantity
        )

    def set_quantity(
        self,
        request: SetCartQuantityRequestDto,
        cart_code: Annotated[
            str,
            Path(
                min_length=36,
                max_length=36,
                pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-7[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
            ),
        ],
        product_code: Annotated[
            str, Path(min_length=1, max_length=25, pattern=r"^\S+$")
        ],
        session: Annotated[
            str, Header(alias="X-Session-Code", min_length=1, pattern=r"^.*\S.*$")
        ],
    ) -> CartDto:
        return self.service.set_quantity(
            cart_code, session, product_code, request.quantity
        )

    def checkout(
        self,
        cart_code: Annotated[
            str,
            Path(
                min_length=36,
                max_length=36,
                pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-7[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
            ),
        ],
        session: Annotated[
            str, Header(alias="X-Session-Code", min_length=1, pattern=r"^.*\S.*$")
        ],
    ) -> CartCheckoutResponseDto:
        return self.service.checkout(cart_code, session)
