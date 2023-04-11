PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS cookies;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipe_lines;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_rows;
DROP TABLE IF EXISTS pallets;
DROP TRIGGER IF EXISTS update_ingredient_total_amount;
DROP TRIGGER IF EXISTS add_cookie_name;
DROP TRIGGER IF EXISTS bake_cookies;

PRAGMA foreign_keys=ON;

CREATE TABLE cookies (
    product_name            TEXT NOT NULL,
    PRIMARY KEY             (product_name)
);

CREATE TABLE ingredients (
    ingredient_name         TEXT NOT NULL,
    unit                    TEXT NOT NULL,
    total_amount            INTEGER NOT NULL DEFAULT (0),
    delivery_datetime       DATETIME,
    delivery_amount         INTEGER,
    PRIMARY KEY             (ingredient_name)
    CONSTRAINT non_negative CHECK (total_amount >= 0)
                            ON CONFLICT ROLLBACK
);

CREATE TABLE recipe_lines (
    product_name            TEXT NOT NULL,
    ingredient_name         TEXT NOT NULL,
    amount                  INTEGER NOT NULL CHECK (amount > 0),
    PRIMARY KEY             (product_name, ingredient_name),
    FOREIGN KEY             (product_name) REFERENCES cookies(product_name),
    FOREIGN KEY             (ingredient_name) REFERENCES ingredients(ingredient_name)
);

CREATE TABLE customers (
    customer_name           TEXT NOT NULL,
    address                 TEXT NOT NULL,
    PRIMARY KEY             (customer_name)
);

CREATE TABLE orders (
    order_id                TEXT NOT NULL DEFAULT (lower(hex(randomblob(16)))),
    customer_name           TEXT NOT NULL,
    delivery_date           DATE NOT NULL,
    PRIMARY KEY             (order_id),
    FOREIGN KEY             (customer_name) REFERENCES customers(customer_name)
);

CREATE TABLE order_rows (
    order_id                TEXT NOT NULL DEFAULT (lower(hex(randomblob(16)))),
    product_name            TEXT NOT NULL,
    amount                  INTEGER NOT NULL CHECK (amount > 0),
    PRIMARY KEY             (order_id, product_name),
    FOREIGN KEY             (product_name) REFERENCES cookies(product_name),
    FOREIGN KEY             (order_id) REFERENCES orders(order_id)
);

CREATE TABLE pallets (
    pallet_number           TEXT NOT NULL DEFAULT (lower(hex(randomblob(16)))),
    product_name            TEXT NOT NULL,
    order_id                TEXT,
    production_datetime     DATETIME NOT NULL,
    is_blocked              INTEGER NOT NULL DEFAULT FALSE,
    PRIMARY KEY             (pallet_number),
    FOREIGN KEY             (product_name) REFERENCES cookies(product_name),
    FOREIGN KEY             (order_id) REFERENCES orders(order_id)
);

CREATE TRIGGER update_ingredient_total_amount
    BEFORE UPDATE
    OF delivery_datetime
    ON ingredients
BEGIN
    UPDATE ingredients
    SET total_amount = total_amount + NEW.delivery_amount
    WHERE ingredient_name = NEW.ingredient_name;
END;

CREATE TRIGGER add_cookie_name
    AFTER INSERT
    ON recipe_lines
    WHEN NEW.product_name NOT IN cookies
BEGIN
    INSERT
    INTO cookies(product_name)
    VALUES (NEW.product_name);
END;

CREATE TRIGGER bake_cookies
    BEFORE INSERT
    ON pallets
BEGIN
    UPDATE ingredients
    SET total_amount = total_amount - 54 * (
        SELECT amount
        FROM recipe_lines
        WHERE product_name = NEW.product_name
            AND ingredient_name = ingredients.ingredient_name
    )
    WHERE ingredient_name IN (
        SELECT ingredient_name
        FROM recipe_lines
        WHERE product_name = NEW.product_name
    );
END;