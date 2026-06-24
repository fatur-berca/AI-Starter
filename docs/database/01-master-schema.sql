-- ==========================================
-- MASTER DATABASE SCHEMA (CUSTOM AI STANDARDS)
-- Project: AI Starter Platform
-- Last Updated: 2026-06-24
-- Rules: No Physical Foreign Keys, Unique Indexes on all tables,
--        and Parent Unique Keys stored in Child tables.
-- ==========================================

-- 1. Roles Table
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX uidx_roles_name ON roles(name);

-- 2. Users Table (Child of roles)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    role_name VARCHAR(50) NOT NULL, -- Parent's Unique Key stored in Child
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    email_verified_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX uidx_users_username ON users(username);
CREATE UNIQUE INDEX uidx_users_email ON users(email);

-- 3. User Sessions Table (Child of users)
CREATE TABLE IF NOT EXISTS user_sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id INT NOT NULL,
    user_email VARCHAR(100) NOT NULL, -- Parent's Unique Key stored in Child
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    payload TEXT NOT NULL,
    last_activity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX uidx_user_sessions_id ON user_sessions(id);

-- 4. Wallets Table (Child of users)
CREATE TABLE IF NOT EXISTS wallets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    user_email VARCHAR(100) NOT NULL, -- Parent's Unique Key stored in Child
    balance DECIMAL(15, 2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'IDR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX uidx_wallets_user_id ON wallets(user_id);
CREATE UNIQUE INDEX uidx_wallets_user_email ON wallets(user_email);

-- 5. Transactions Table (Child of wallets)
CREATE TABLE IF NOT EXISTS transactions (
    id VARCHAR(100) PRIMARY KEY,
    wallet_id INT NOT NULL,
    user_email VARCHAR(100) NOT NULL, -- Parent's Unique Key (from users/wallets) stored in Child
    type ENUM('deposit', 'withdrawal', 'transfer', 'payment') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    description TEXT NULL,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX uidx_transactions_id ON transactions(id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
