-- SQL ALTER statements for database migration
CREATE TABLE Logs (
  id SERIAL,
  currency INTEGER NOT NULL,
  amount REAL NOT NULL,
  description VARCHAR DEFAULT ' ',
  shop_order_id INTEGER NOT NULL,
  transfer_time TIMESTAMP NOT NULL,
  PRIMARY KEY (id),
  UNIQUE(shop_order_id)
);
