CREATE TABLE
IF NOT EXISTS Product (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  price DECIMAL(9,2) NOT NULL,
  provider TEXT NOT NULL,
  provider_contact TEXT
);

CREATE TABLE
IF NOT EXISTS "Order" (
  id INTEGER PRIMARY KEY,
  total DECIMAL(9,2) DEFAULT 0.00,
  date DATE default (date('now'))
);

CREATE TABLE
IF NOT EXISTS OrderLine (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER DEFAULT 1,
  price Decimal(9,2),
  cost Decimal (9,2),
  FOREIGN KEY (order_id) REFERENCES "Order" (id),
  FOREIGN KEY (product_id) REFERENCES Product (id)
);