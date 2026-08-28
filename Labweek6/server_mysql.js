const express = require('express');
const mysql = require('mysql2');
require('dotenv').config();

const app = express();
app.use(express.json());

// Custom Logger Middleware
const loggerMiddleware = (req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
};
app.use(loggerMiddleware);

// MySQL Database Connection
const db = mysql.createConnection({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'myuser',
    password: process.env.DB_PASSWORD || 'mypassword',
    database: process.env.DB_NAME || 'mydatabase',
    port: process.env.DB_PORT || 3307
});

db.connect((err) => {
    if (err) {
        console.error('Database connection failed:', err);
    } else {
        console.log('Connected to MySQL database!');
    }
});

// ==========================================
// ROUTES (MySQL CRUD with Soft Delete)
// ==========================================

// 1. CREATE Route: Add a new user
app.post('/create', async (req, res) => {
    const { email, name, password } = req.body;
    try {
        db.query(
            "INSERT INTO users(email, fullname, password) VALUES(?, ?, ?)",
            [email, name, password],
            (err, results, fields) => {
                if (err) {
                    console.log(err);
                    return res.status(400).json({ error: err.message || "Database Query Error" });
                }
                res.status(201).json({ message: "User created successfully!", id: results.insertId });
            }
        );
    } catch (err) {
        console.log(err);
        return res.status(500).send();
    }
});

// 2. READ Route: Get all active users (Soft Delete aware)
app.get('/read', async (req, res) => {
    try {
        db.query("SELECT * FROM users WHERE deleted_at IS NULL", (err, results, fields) => {
            if (err) {
                console.log(err);
                return res.status(400).send();
            }
            res.status(200).json(results);
        });
    } catch (err) {
        console.log(err);
        return res.status(500).send();
    }
});

// 3. READ SINGLE Route: Get single active user by email
app.get('/read/single/:email', async (req, res) => {
    const email = req.params.email;
    try {
        db.query(
            "SELECT * FROM users WHERE email = ? AND deleted_at IS NULL",
            [email],
            (err, results, fields) => {
                if (err) {
                    console.log(err);
                    return res.status(400).send();
                }
                if (results.length === 0) {
                    return res.status(404).json({ message: "User not found or deleted" });
                }
                res.status(200).json(results[0]);
            }
        );
    } catch (err) {
        console.log(err);
        return res.status(500).send();
    }
});

// 4. UPDATE Route: Update user password (active users only)
app.patch('/update/:email', async (req, res) => {
    const email = req.params.email;
    const newPassword = req.body.newPassword;
    try {
        db.query(
            "UPDATE users SET password = ? WHERE email = ? AND deleted_at IS NULL",
            [newPassword, email],
            (err, results, fields) => {
                if (err) {
                    console.log(err);
                    return res.status(400).send();
                }
                if (results.affectedRows === 0) {
                    return res.status(404).json({ message: "User not found or deleted" });
                }
                res.status(200).json({ message: "User password updated successfully!" });
            }
        );
    } catch (err) {
        console.log(err);
        return res.status(500).send();
    }
});

// 5. SOFT DELETE Route: Set deleted_at timestamp instead of removing row
app.delete('/delete/:email', async (req, res) => {
    const email = req.params.email;
    try {
        db.query(
            "UPDATE users SET deleted_at = NOW() WHERE email = ? AND deleted_at IS NULL",
            [email],
            (err, results, fields) => {
                if (err) {
                    console.log(err);
                    return res.status(400).send();
                }
                if (results.affectedRows === 0) {
                    return res.status(404).json({ message: "No active user found with that email!" });
                }
                return res.status(200).json({ message: "User soft-deleted successfully!" });
            }
        );
    } catch (err) {
        console.log(err);
        return res.status(500).send();
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
