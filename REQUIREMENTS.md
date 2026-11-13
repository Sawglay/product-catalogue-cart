# Lesson 10: shopping cart requirements and interactions

## Scope and user stories

The actor is a shopper using a mock browser session. Each page load creates a new session; navigating within the page preserves it. The session header scopes access to a cart and is not authentication. PostgreSQL stores carts, but this frontend does not recover a previous session after reload. Payment and order processing are outside scope.

| Story | Shopper need | API interaction |
| --- | --- | --- |
| US1 | As a shopper, I want to start and view my cart so I can inspect my selection. | `POST /api/carts`, then `GET /api/carts/{cart_code}` |
| US2 | As a shopper, I want to add a chosen quantity so I can buy several units. | `POST /api/carts/{cart_code}/items` with `productCode` and `quantity` |
| US3 | As a shopper, I want accurate totals so I can understand the cost. | Each cart response includes server-calculated `totals`. |
| US4 | As a shopper, I want to remove items so I can revise my selection. | `PUT /api/carts/{cart_code}/items/{product_code}` with `quantity: 0` |
| US5 | As a shopper, I want immediate, consistent feedback so I know whether an action succeeded. | Serialised cart requests; render the returned cart after success. |

All cart requests carry `X-Session-Code`. Read the [backend contract](backend-api/README.md) alongside these criteria.

## Acceptance criteria

These Gherkin scenarios are specifications for manual or future automated checks; no Gherkin runner is bundled.

```gherkin
Feature: Session-scoped shopping cart
  Scenario: US1 - Create and revisit an empty cart
    Given I have a new mock session
    When I create a cart using that session
    Then the API returns status 201 and a cart code
    And the cart has no items and no currency totals
    When I create a cart again using the same session
    Then the API returns status 200 and the same cart code
    When I open View Cart
    Then I see "Your cart is empty."

  Scenario: US1 - Keep another session's cart separate
    Given a cart belongs to session A
    When I request that cart with session B
    Then the API returns status 404 and error code "CART_NOT_FOUND"
    And no cart contents are disclosed

  Scenario: US2 and US3 - Add and accumulate quantities
    Given my cart is empty
    And a product costs 12.35 THB per unit
    When I add 2 units of that product
    Then my cart contains one line with quantity 2
    And the server returns a total of "24.70" for THB
    When I add 1 more unit of the same product
    Then my cart contains one line with quantity 3
    And the server returns a total of "37.05" for THB
    And the browser cart count shows 3 without a page reload

  Scenario: US2 - Reject an invalid addition
    Given I have a cart
    When I submit an add-item API request with quantity 0
    Then the API returns status 400 and error code "INVALID_REQUEST"
    And the cart is unchanged

  Scenario: US3 - Keep currency totals separate
    Given my cart contains 2 units priced at 12.35 THB each
    And my cart contains 1 unit priced at 5.00 USD
    When I view my cart
    Then the server returns a THB total of "24.70"
    And the server returns a USD total of "5.00"
    And the browser displays both totals without converting currencies

  Scenario: US4 - Remove the final cart line
    Given my cart contains only one product line
    When I choose Remove item
    Then the browser sends a quantity of 0 to the quantity endpoint
    And the returned cart has no items and no currency totals
    And the browser shows an empty cart and a count of 0 without reloading

  Scenario: US5 - Prevent duplicate additions while waiting
    Given the Add to Cart request is waiting for a response
    When I try to activate the same Add to Cart button again
    Then no second addition is submitted from that button
    And the button becomes available again after success or failure

  Scenario: US5 - Keep overlapping actions ordered
    Given an add-item request is waiting for a response
    When I open View Cart
    Then the cart read waits until the addition has completed
    And the displayed cart and count reflect the latest successful response

  Scenario: US5 - Continue after a failed request
    Given a cart request fails
    Then the browser displays an error message
    And it does not invent a successful cart update
    When I perform another cart action
    Then that action can still run
```

The multi-currency scenario needs additional API/database fixture data: the default catalogue uses THB. To inspect failures manually, use browser network throttling and request blocking. A network failure may occur after a server commit; open View Cart to fetch authoritative state before retrying an addition.

## Service interaction design

```mermaid
sequenceDiagram
    actor Shopper
    participant UI as Browser UI
    participant Queue as Cart request queue
    participant Proxy as Nginx
    participant API as Cart route / service
    participant Domain as Cart domain
    participant DB as Repository / PostgreSQL
    Shopper->>UI: Add product and quantity
    UI->>UI: Disable Add button; capture quantity
    UI->>Queue: Enqueue addition
    Note over Queue: Wait for earlier cart reads/writes, including creation
    Queue->>Proxy: POST /api/carts/{code}/items + session header
    Proxy->>API: Forward request
    API->>DB: Load session-owned cart and product
    API->>Domain: Validate addition
    API->>DB: Persist addition in transaction
    DB-->>API: Saved cart
    API->>Domain: Calculate totals per currency
    API-->>UI: Cart DTO through Nginx
    UI->>UI: Replace cart state; render count, items and totals
    UI->>UI: Re-enable Add button
```

Viewing uses a queued `GET`; removal uses a queued `PUT` with zero quantity. Both return the same cart representation. Checkout deletes the cart and creates its replacement within one queued operation. Product browsing requests can run independently.

## Meaning of real-time updates

For this lesson, real-time means the current page updates its cart count, items and totals immediately after a successful API response, without a page reload. The server is authoritative for prices and totals. Cart reads and writes run in browser action order, so an earlier response cannot overwrite a later operation's state. Failed operations release the queue for subsequent actions.

This design does not synchronise other tabs or clients automatically. Each page load has a different mock session; polling, WebSockets and shared-session persistence would require an additional requirement and design.

## Analysis exercises

1. Before reading the backend contract, derive the method, path, headers, body and response for US1, US2 and US4. Compare your proposal with the implementation and explain zero-quantity removal.
2. Trace US2 from the browser through Nginx, routes, service, domain and repository. Identify who validates quantities, enforces session ownership, persists changes and calculates totals.
3. Draw the removal interaction and its error branch. Explain what the UI should display if persistence fails.
4. Use throttling to add an item and immediately open View Cart. Inspect request order and verify US5. Repeat with one failed request and confirm a later action runs.
5. Explain why two tabs have different carts here. Propose the requirement changes needed for a shared cart with live updates, including how concurrent writes would be resolved.
