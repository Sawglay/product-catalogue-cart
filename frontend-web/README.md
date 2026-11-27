# Frontend

Nginx serves one `index.html` page with a header, search bar, left menu, product view, and cart view. JavaScript and CSS live in `scripts/` and `assets/styles/`. The `pages/` directory remains part of the lesson-05 structure; the two shopping views switch within the index page so changing views does not reset the mock session.

The browser requests products and carts through the same-origin `/api/` proxy. It loads the three default groups (`month-offers`, `best-sellers`, `home`), provides category/tag/sort filters and search, displays products in a grid, and opens a detail dialog to select quantity. The cart view supports removal and checkout. On checkout, the backend deletes the cart and the browser creates a new one.

`X-Session-Code` is generated afresh in browser memory on each page load or reload. There is no sign-in or cross-reload cart persistence. Product images and the logo are placeholders; no real or generated image is required. The stylesheet uses the lesson's white background and blue/red branding.

Start the three services from the parent lesson-10 directory, then open <http://localhost:8080>. The proxied API schema is at <http://localhost:8080/api/openapi.json>.

## Cart updates

Real-time means updates on this page after a successful API response, without reloading. `cart-queue.js` serialises initial cart creation, reads, additions, removals and checkout so responses cannot overwrite newer cart state. After success, `index.js` renders the server's cart items, totals and count. Add to Cart is disabled while its operation is pending; its selected quantity is captured before queueing. A failed operation displays an error and releases the queue for later actions. No automatic mutation retries are performed.

See [requirements and exercises](../REQUIREMENTS.md) for the user stories and acceptance criteria. Other tabs and clients are not synchronised automatically.

Run the request-ordering and failure-recovery checks from this directory with `node --test tests/cart-queue.test.mjs` (Node.js required).
