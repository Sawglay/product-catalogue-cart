"""Compose the layered API and its common HTTP error handling."""

import logging
import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.errors import MyApplicationError
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.routes.carts import CartsRoutes
from app.routes.health_checks import HealthChecksRoutes
from app.routes.products import ProductsRoutes
from app.services.cart_service import CartService
from app.services.health_check_service import HealthCheckService
from app.services.product_service import ProductService


class Application:
    """Own the API's repositories, use cases, routes, and error handlers."""

    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)

        # Environment variables
        connection_string = os.environ["DATABASE_URL"]

        # Class configuration
        product_repository = ProductRepository(connection_string)
        cart_repository = CartRepository(connection_string)

        # Backend configuration
        self.app = FastAPI(
            title="Lesson 09 Product Catalogue and Cart Management",
            version="0.1.0",
            description="Database-backed catalogue and session-scoped cart API.",
            openapi_url="/api/openapi.json",
            docs_url="/api/docs",
            redoc_url="/api/redoc",
        )

        # Error management
        self.app.add_exception_handler(MyApplicationError, self.handle_application_error)
        self.app.add_exception_handler(RequestValidationError, self.handle_validation_error)
        self.app.add_exception_handler(StarletteHTTPException, self.handle_http_error)

        # Route / Presentation layer configuration
        self.app.include_router(ProductsRoutes(ProductService(product_repository)).router, prefix="/api")
        self.app.include_router(CartsRoutes(CartService(cart_repository, product_repository)).router, prefix="/api")
        self.app.include_router(HealthChecksRoutes(HealthCheckService(product_repository)).router, prefix="/api")

    def handle_application_error(self, request: Request, exc: MyApplicationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_response_code,
            content={"error_code": exc.error_code, "path": request.url.path},
        )

    def handle_validation_error(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error_code": "INVALID_REQUEST", "path": request.url.path},
        )

    def handle_http_error(self, request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": "HTTP_ERROR", "path": request.url.path},
        )


app = Application().app
