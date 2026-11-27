# Product Catalogue Cart

FastAPI serves product catalogue and cart management routes under `/api/`. The `/api/openapi.json` schema and `/api/docs` documentation are available directly on port 8000 and through Nginx on port 8080.

## Product catalogue

- `GET /api/products` supports `category`, colon-separated `tag`, partial `name`, `sort=name|price:asc|desc`, `block`, and `items`. Defaults are `sort=name:asc`, `block=1`, `items=20`.
- `GET /api/products/{product_code}` returns one product. Public responses use the product `code`, not the database ID. Prices are two-decimal strings.

## Cart management

Supply the `X-Session-Code` header to every cart request. The browser creates a mock value with `crypto.randomUUID()` on each page load; it is not user authentication.

- `POST /api/carts` creates one cart for a session, or returns its existing cart.
- `GET /api/carts/{cart_code}` returns that session's cart.
- `POST /api/carts/{cart_code}/items` accepts `{"productCode":"HOME-ABC-001","quantity":1}`. Repeated additions increase the quantity.
- `PUT /api/carts/{cart_code}/items/{product_code}` accepts `{"quantity":2}`; zero removes the item.
- `POST /api/carts/{cart_code}/checkout` logs checkout and deletes the cart. The browser then creates a new cart. Orders and payment are not implemented.

The API returns `error_code` and `path` on errors. Its `MyApplicationError` carries the HTTP response code and error code; the frontend maps error codes to readable messages. Cart totals are grouped by currency; seeded products use THB, so the normal lesson cart has one total. SQL queries are parameterised.

## Local runtime

Run from the parent lesson-09 directory with `docker compose up --build -d`. The database connection comes from `DATABASE_URL`; Compose supplies it. Health endpoints are `/api/health/live` and `/api/health/ready` on both ports.
