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
