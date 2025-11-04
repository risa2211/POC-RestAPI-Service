-- The users table for profile data.
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(100) NOT NULL,
    flat_no VARCHAR(50),
    area VARCHAR(100),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    pin_code VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- The sports table for the list of sports.
CREATE TABLE sports (
    sport_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- The sports statistic table to store teh metrics.
-- I have included a foreign key relationship to the sports table.
CREATE TABLE sport_statistics (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    sport_id INT NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value VARCHAR(255) NOT NULL,
    source VARCHAR(255),
    last_updated DATE,
    FOREIGN KEY (sport_id) REFERENCES sports(sport_id)
);
