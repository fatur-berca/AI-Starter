// ==========================================
// AUTHENTICATION CONTROLLER (TEMPLATE - CUSTOM STANDARDS)
// Project: AI Starter Platform
// References: docs/features/F01-manajemen-user.md
// ==========================================

const bcrypt = require('bcrypt');
const User = require('../models/User');

class AuthController {
    /**
     * POST /api/auth/register
     * Aligns with F01 Dev Spec Scenario 1
     */
    async register(req, res) {
        const { username, email, password } = req.body;

        if (!username || !email || !password) {
            return res.status(400).json({ error: 'All fields are required' });
        }

        try {
            // Password security: 10 rounds bcrypt salt
            const saltRounds = 10;
            const passwordHash = await bcrypt.hash(password, saltRounds);

            // Default role is Customer (role_id = 3, role_name = 'customer' based on 02-seed-data.sql)
            const defaultCustomerRoleId = 3; 
            const defaultCustomerRoleName = 'customer';
            
            const newUser = await User.create(null, {
                roleId: defaultCustomerRoleId,
                roleName: defaultCustomerRoleName, // Passing parent's unique key
                username,
                email,
                passwordHash
            });

            return res.status(201).json({
                message: 'User registered successfully',
                user: {
                    id: newUser.id,
                    username: newUser.username,
                    email: newUser.email,
                    roleName: newUser.roleName
                }
            });
        } catch (error) {
            return res.status(500).json({ error: 'Server error during registration' });
        }
    }

    /**
     * POST /api/auth/login
     * Aligns with F01 Dev Spec Scenario 2
     */
    async login(req, res) {
        // Implementation here will check credentials and create session in user_sessions
    }
}

module.exports = new AuthController();
