CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    birthdate DATE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at DATETIME
);


CREATE TABLE tokens (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    balance INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE slot_machine (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    balance INT NOT NULL,
    status VARCHAR(255)
);


INSERT INTO slot_machine (id, name, balance, status) VALUES
('machine1', 'Slot Machine 1', 100, 'AVAILABLE'),
('machine2', 'Slot Machine 2', 100, 'AVAILABLE'),
('machine3', 'Slot Machine 3', 100, 'AVAILABLE');
