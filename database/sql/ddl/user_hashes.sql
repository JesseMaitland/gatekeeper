CREATE TABLE gatekeeper.user_hashes
(
    id INT IDENTITY (1, 1) PRIMARY KEY,
    user_name VARCHAR(50),
    user_hash VARCHAR(100),
    user_state VARCHAR(20),
    is_current BOOLEAN,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
