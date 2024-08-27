-- schema.sql
CREATE TABLE IF NOT EXISTS slot_machine (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    balance INTEGER
);