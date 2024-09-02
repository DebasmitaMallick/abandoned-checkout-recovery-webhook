-- Create customers table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create abandoned_checkouts table
CREATE TABLE abandoned_checkouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_token TEXT NOT NULL,
    email TEXT NOT NULL,
    abandoned_at DATETIME NOT NULL,
    recovery_url TEXT NOT NULL,
    customer_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE scheduled_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checkout_id INTEGER,
    message TEXT NOT NULL,
    message_time DATETIME NOT NULL,
    FOREIGN KEY (checkout_id) REFERENCES abandoned_checkouts(id)
);

-- Create orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_token TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_token) REFERENCES abandoned_checkouts(cart_token)
);
