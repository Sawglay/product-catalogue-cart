# Product Catalogue & Shopping Cart

A school-provided full-stack learning project for browsing products and managing a shopping cart. It combines a vanilla JavaScript frontend, a layered FastAPI backend, and PostgreSQL, with Docker Compose running the application locally.

This repository is based on the **Lesson 10 starter project** supplied by the school. It is maintained for coursework, practice, and further development; the original starter implementation is credited to the school/course instructors.

## Features

- Browse products in Month Offers, Best Sellers, and Home groups.
- Search by product name and filter by category or tag.
- Sort by name or price and navigate paginated results.
- Open product details and select a quantity before adding to the cart.
- View cart items, quantities, item count, and totals grouped by currency.
- Remove items through the interface; set item quantities through the API.
- Complete a demonstration checkout that deletes the cart and starts a fresh one.
- Update the current page after successful API responses without a page reload.
- Process cart operations sequentially to preserve request order.
- Explore interactive API documentation and health-check endpoints.

## Technology Stack

| Component | Technology |
| --- | --- |
| Frontend | HTML, CSS, vanilla JavaScript ES modules |
| Web server and reverse proxy | Nginx |
| Backend | Python, FastAPI, Uvicorn |
| Database | PostgreSQL |
| Database access | Psycopg with parameterized SQL |
| Local orchestration | Docker Compose |
| Frontend queue tests | Node.js built-in test runner |

The supplied files pin Python to `3.14.7`, PostgreSQL to `18.6`, and Nginx to `stable-alpine`. These are the starter's configured versions, not a claim that the container images were verified or launched.

## Architecture

Docker Compose runs three services:

| Service | Role | Local port |
| --- | --- | --- |
| `frontend-web` | Serves the frontend and forwards `/api/` requests to FastAPI | `8080` |
| `backend-api` | Handles product, cart, and health-check requests | `8000` |
| `postgres-db` | Stores catalogue and cart data | `5432` |

The browser calls the same-origin `/api/` routes through Nginx. The backend separates HTTP routes, application services, domain entities, data-transfer models, and database repositories. Product and cart functionality live within **one backend application**.

## Project Structure

Upload the contents of the extracted `lesson-10` folder to the repository root. The main paths are:

| Path | Purpose |
| --- | --- |
| `README.md` | Project overview and setup instructions |
| `REQUIREMENTS.md` | User stories, acceptance criteria, and design exercises |
| `docker-compose.yml` | Default local service configuration |
| `docker-compose.mac.yml` | macOS service configuration |
| `backend-api/pyproject.toml` | Python package configuration and dependencies |
| `backend-api/app/Dockerfile` | Backend container build |
| `backend-api/app/main.py` | FastAPI application and error handling |
| `backend-api/app/routes/` | HTTP endpoints |
| `backend-api/app/services/` | Application use cases |
| `backend-api/app/entities/` | Domain objects and repository interfaces |
| `backend-api/app/models/` | Request and response models |
| `backend-api/app/repositories/` | Database access and mapping |
| `backend-api/app/errors/` | Application error definitions |
| `backend-api/app/configurations/` | Configuration package |
| `backend-api/database/` | Schema and sample-data SQL scripts |
| `frontend-web/index.html` | Main page with product and cart views |
| `frontend-web/assets/styles/` | CSS styles |
| `frontend-web/scripts/` | API requests, rendering, and cart queue |
| `frontend-web/tests/` | Cart queue tests |
| `frontend-web/nginx.conf` | Static hosting and API proxy configuration |
| `frontend-web/pages/` | Placeholder directory retained from the starter |

## Getting Started

### Prerequisites

- Docker with Docker Compose available and the Docker engine running.
- A modern web browser.
- Git if cloning the repository, or download and extract the repository ZIP.
- Node.js with ES module support if running the queue tests.

Python and PostgreSQL run inside containers; a separate local installation is not required for the Docker setup.

### Start the application

Open a terminal in the project root, where `docker-compose.yml` is located:

```bash
docker compose up --build -d
docker compose ps
```

On macOS, use:

```bash
docker compose -f docker-compose.mac.yml up --build -d
docker compose -f docker-compose.mac.yml ps
```

Use the same `-f docker-compose.mac.yml` option for subsequent macOS Compose commands.

### Open the application

| Resource | URL |
| --- | --- |
| Shop | http://localhost:8080 |
| Swagger UI | http://localhost:8000/api/docs |
| ReDoc | http://localhost:8000/api/redoc |
| OpenAPI schema | http://localhost:8000/api/openapi.json |
| API liveness | http://localhost:8080/api/health/live |
| Database readiness | http://localhost:8080/api/health/ready |

The API documentation and schema also work through port `8080`, using the same `/api/` paths.

### Database initialization

On the first creation of the database volume, PostgreSQL runs:

1. `backend-api/database/001-database-creation.sql` to create the tables.
2. `backend-api/database/002-seed-data.sql` to load sample products, categories, tags, and THB currency data.

Carts are created through browser interactions. Database data remains in the named volume when containers are stopped or removed with `docker compose down`. Editing the SQL files does not rerun initialization against an existing volume.

## API Endpoints

All cart requests require the `X-Session-Code` header. Reuse the same header value when creating and accessing a cart.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/products` | List, search, filter, sort, and paginate products |
| `GET` | `/api/products/{product_code}` | Retrieve a product |
| `POST` | `/api/carts` | Create a session cart or return its existing cart |
| `GET` | `/api/carts/{cart_code}` | Retrieve the session's cart |
| `POST` | `/api/carts/{cart_code}/items` | Add a product or increase its quantity |
| `PUT` | `/api/carts/{cart_code}/items/{product_code}` | Set quantity; zero removes the item |
| `POST` | `/api/carts/{cart_code}/checkout` | Log demonstration checkout and delete the cart |
| `GET` | `/api/health/live` | Check API liveness |
| `GET` | `/api/health/ready` | Check database readiness |

Product listing accepts `category`, `tag`, `name`, `sort`, `block`, and `items`. Defaults are `sort=name:asc`, `block=1`, and `items=20`. Tags may be colon-separated; sort supports `name:asc`, `name:desc`, `price:asc`, and `price:desc`.


Example product query:

```text
http://localhost:8080/api/products?name=notebook&sort=price:asc&block=1&items=20
```

For adding an item, use a product code returned by the catalogue:

```json
{
  "productCode": "<product code returned by the API>",
  "quantity": 2
}
```

To set an existing item's quantity:

```json
{
  "quantity": 3
}
```

## Checks and Tests

Run the supplied cart queue tests from the repository root:

```bash
node --test frontend-web/tests/cart-queue.test.mjs
```

These two tests check operation ordering when a response is delayed and queue recovery after a rejected request. They do not cover the full application or database integration.

For a manual check, browse products, add an item, open the cart, remove an item, and try demonstration checkout. Check the readiness endpoint if requests fail.

View service logs:

```bash
docker compose logs backend-api
docker compose logs postgres-db
```

Stop the services while retaining database data:

```bash
docker compose down
```

## Current Scope and Limitations

- The browser generates a new mock session on each page load. Reloading does not restore the previous browser cart, even though database rows may remain.
- `X-Session-Code` is a demonstration session identifier, not user authentication.
- Checkout does not process payments or create orders.
- Page updates happen after API responses; there is no automatic synchronization across tabs or clients.
- Product images and the logo are placeholders.
- The Compose files contain local demonstration database credentials.
- Some backend metadata and documentation still refer to Lesson 09, inherited from the starter.

## Further Documentation

- [Requirements and service interaction design](REQUIREMENTS.md)
- [Backend API documentation](backend-api/README.md)
- [Frontend documentation](frontend-web/README.md)

## Acknowledgements

The original Lesson 10 starter code and teaching materials were provided by the school/course instructors. This repository documents that coursework foundation; any future student modifications should be identified separately.
