CREATE DATABASE IF NOT EXISTS mapua_findr;
USE mapua_findr;

CREATE TABLE IF NOT EXISTS items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    public_description TEXT NOT NULL,
    campus VARCHAR(50) DEFAULT 'Intramuros',
    building VARCHAR(50) NOT NULL,
    room VARCHAR(50),
    storage_bin VARCHAR(50) NOT NULL,
    status VARCHAR(30) DEFAULT 'Surrendered',
    hidden_specifications TEXT NOT NULL,
    date_found DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ALTER TABLE items ADD COLUMN image_path VARCHAR(255) NULL AFTER hidden_specifications;
);