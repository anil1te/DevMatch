CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    photo_url VARCHAR(255),
    descrip TEXT,
    skills TEXT,
    stack VARCHAR(255),
    banned INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
