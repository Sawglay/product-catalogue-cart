-- TIMESTAMPTZ stores instants; the application normalises them to UTC.
SET TIME ZONE 'UTC';

CREATE TABLE currencies (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
    code varchar(4) NOT NULL UNIQUE CHECK (length(trim(code)) > 0),
    name varchar(150) NOT NULL UNIQUE,
    symbol varchar(1) NOT NULL UNIQUE,
    created_timestamp timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamptz
);

CREATE TABLE categories (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
    code varchar(100) NOT NULL UNIQUE CHECK (length(trim(code)) > 0),
    created_timestamp timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamptz
);

CREATE TABLE tags (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
    code varchar(100) NOT NULL UNIQUE CHECK (length(trim(code)) > 0),
    created_timestamp timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamptz
);

CREATE TABLE products (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
    code varchar(25) NOT NULL UNIQUE CHECK (length(trim(code)) > 0),
    name varchar(255) NOT NULL CHECK (length(trim(name)) > 0),
    description text NOT NULL,
    unit_price numeric(12,2) NOT NULL CHECK (unit_price >= 0),
    currency_id bigint NOT NULL REFERENCES currencies(id),
    created_timestamp timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamptz
);

CREATE TABLE product_categories (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
    product_id bigint NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    category_id bigint NOT NULL REFERENCES categories(id),
    created_timestamp timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamptz,
    UNIQUE (product_id, category_id)
);

CREATE TABLE product_tags (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
    product_id bigint NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    tag_id bigint NOT NULL REFERENCES tags(id),
    created_timestamp timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamptz,
    UNIQUE (product_id, tag_id)
);

CREATE TABLE carts (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
    code varchar(36) NOT NULL UNIQUE
        CHECK (code ~ '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'),
    session text NOT NULL UNIQUE CHECK (length(trim(session)) > 0),
    created_timestamp timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamptz
);

CREATE TABLE cart_items (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY CHECK (id > 0),
    cart_id bigint NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id bigint NOT NULL REFERENCES products(id),
    quantity integer NOT NULL CHECK (quantity > 0),
    created_timestamp timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamptz,
    UNIQUE (cart_id, product_id)
);

CREATE INDEX product_categories_category_idx ON product_categories(category_id, product_id);
CREATE INDEX product_tags_tag_idx ON product_tags(tag_id, product_id);
CREATE INDEX products_name_idx ON products(name, code);
CREATE INDEX products_price_idx ON products(unit_price, code);
