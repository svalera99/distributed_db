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
  PRIMARY KEY(category, price)
);

CREATE MATERIALIZED VIEW items_by_category_model AS
  SELECT category, model, producer, price
  FROM items
  WHERE category IS NOT NULL AND model IS NOT NULL AND price IS NOT NULL
  PRIMARY KEY (category, model, price);


COPY items(category, model, producer, price) FROM '/scripts/items.csv' WITH DELIMITER=',' AND HEADER = true;