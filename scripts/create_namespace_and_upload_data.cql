CREATE KEYSPACE IF NOT EXISTS items
WITH REPLICATION = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 1
};
USE items;


CREATE TABLE IF NOT EXISTS items(
  category text,
  model text,
  producer text,
  price float,
  characteristics map<text, text>,
  PRIMARY KEY(category, price)
);

CREATE INDEX characteristics_idx ON items (KEYS(characteristics));
CREATE INDEX characteristics_val ON items (ENTRIES(characteristics));

CREATE MATERIALIZED VIEW IF NOT EXISTS items_by_category_model AS
  SELECT category, model, producer, price, characteristics
  FROM items
  WHERE category IS NOT NULL AND model IS NOT NULL AND price IS NOT NULL
  PRIMARY KEY (category, model, price);


COPY items(category, model, producer, price, characteristics) FROM '/scripts/items.csv' WITH DELIMITER=',' AND HEADER = true;


CREATE TABLE IF NOT EXISTS orders(
  customer_name text,
  items_ids list<int>,
  order_price int,
  order_date date,
  PRIMARY KEY(customer_name, order_date)
);
CREATE INDEX items_ids_idx ON orders ( items_ids );

COPY orders(customer_name, items_ids, order_price, order_date) FROM '/scripts/orders.csv' WITH DELIMITER=',' AND HEADER = true;