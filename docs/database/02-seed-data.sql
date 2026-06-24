-- ==========================================
-- MASTER SEED DATA (UPDATED FOR CUSTOM AI STANDARDS)
-- Project: AI Starter Platform
-- Last Updated: 2026-06-24
-- ==========================================

-- Populate Roles
INSERT INTO roles (name, description) VALUES
('administrator', 'Super user with access to all parts of the system'),
('developer', 'Internal technical user with read/write database access'),
('customer', 'End-user client of the application');

-- Populate Initial Administrator
INSERT INTO users (role_id, role_name, username, email, password_hash, status, email_verified_at) VALUES
(1, 'administrator', 'superadmin', 'admin@aistarter.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'active', NOW());

-- Populate Test Customers
INSERT INTO users (role_id, role_name, username, email, password_hash, status, email_verified_at) VALUES
(3, 'customer', 'johndoe', 'john.doe@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'active', NOW()),
(3, 'customer', 'janedoe', 'jane.doe@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'active', NULL);

-- Create Initial Wallets for Customers (including parent's unique key user_email)
INSERT INTO wallets (user_id, user_email, balance, currency) VALUES
(2, 'john.doe@example.com', 500000.00, 'IDR'),
(3, 'jane.doe@example.com', 0.00, 'IDR');
