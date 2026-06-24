// ==========================================
// USER MODEL (TEMPLATE - CUSTOM STANDARDS)
// Project: AI Starter Platform
// References: docs/database/01-master-schema.sql
// ==========================================

class User {
    constructor(id, roleId, roleName, username, email, passwordHash, status = 'active') {
        this.id = id;
        this.roleId = roleId;
        this.roleName = roleName; // Storing parent unique key
        this.username = username;
        this.email = email;
        this.passwordHash = passwordHash;
        this.status = status;
    }

    /**
     * Finds a user by email in database.
     * Stub implementation: references users table columns.
     */
    static async findByEmail(dbConnection, email) {
        // SELECT * FROM users WHERE email = ? LIMIT 1
        return null; 
    }

    /**
     * Creates a new user record in database.
     */
    static async create(dbConnection, { roleId, roleName, username, email, passwordHash }) {
        // INSERT INTO users (role_id, role_name, username, email, password_hash) VALUES (?, ?, ?, ?, ?)
        return new User(99, roleId, roleName, username, email, passwordHash, 'active');
    }
}

module.exports = User;
