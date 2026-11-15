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
