-- Creates table users with id email and name if not exist
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT,
    email varchar(255) NOT NULL UNIQUE,
    name varchar(255),
    PRIMARY KEY (id)
);
