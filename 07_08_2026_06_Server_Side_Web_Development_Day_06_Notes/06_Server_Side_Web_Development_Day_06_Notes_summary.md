---
title: "Day 06 Deep-Dive Note: Express Middleware, Dotenv, MySQL Docker, Soft Delete & MongoDB Mongoose"
course_id: "06016418"
course_name: "Server-Side Web Development"
institution: "KMITL IT"
semester: "2026-Semester"
date: 2026-08-07
tags:
  - express
  - middleware
  - dotenv
  - mysql
  - docker
  - soft-delete
  - mongodb
  - mongoose
  - nodejs
---

# 📚 Day 06 Deep-Dive Academic Guide: Server-Side Web Development

> **Course:** 06016418 Server-Side Web Development  
> **Topic:** Custom Middleware, Environment Configurations (`dotenv`), Relational Database Integration (MySQL via Docker), Soft Delete Pattern, and Document Database Integration (MongoDB via Mongoose ODM).

---

## 🎯 Executive Summary & Learning Objectives

1. **Middleware Architecture:** Master the Express request-response lifecycle, custom middleware construction, logging, and `next()` propagation mechanics.
2. **Configuration Security:** Enforce the 12-Factor App methodology by decoupling secrets from source code using `dotenv` and `process.env`.
3. **Containerized Database Operations:** Provision a MySQL container via Docker Compose, establish database connection pools with `mysql2`, and parameterize queries to prevent SQL Injection.
4. **Data Integrity & Soft Delete Pattern:** Understand the architectural shift from destructive Hard Delete to audit-compliant Soft Delete (`deleted_at` timestamp strategy).
5. **NoSQL & Object-Document Mapping (ODM):** Understand Document Databases (MongoDB), establish Atlas/Local connections using Mongoose, construct structured Schemas/Models with validations, and execute asynchronous CRUD operations.

---

## 1. ⚙️ Module 1: Express.js Middleware Architecture

### 1.1 What is Middleware?
Middleware functions are functions that have access to the **Request object (`req`)**, the **Response object (`res`)**, and the **next middleware function (`next`)** in the application’s request-response cycle.

```
       Incoming HTTP Request
                 │
                 ▼
       ┌──────────────────┐
       │ Logger Middleware│ ──▶ Log timestamp, method, url
       └──────────────────┘
                 │ `next()`
                 ▼
       ┌──────────────────┐
       │ Body Parser      │ ──▶ Parse JSON body into `req.body`
       └──────────────────┘
                 │ `next()`
                 ▼
       ┌──────────────────┐
       │ Route Handler    │ ──▶ Execute business logic & SQL query
       └──────────────────┘
                 │
                 ▼
        HTTP Response Sent (200 / 201 / 400 / 500)
```

### 1.2 The Role of `next()`
- If the current middleware function does not end the request-response cycle (e.g., by calling `res.send()` or `res.json()`), it **MUST** call `next()` to pass control to the next middleware function.
- **DANGER:** Forgetting to call `next()` causes the request to hang indefinitely until client timeout.

### 1.3 Custom Request Logger Implementation
```javascript
// Custom Logger Middleware
const loggerMiddleware = (req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next(); // Pass control to the next handler
};

// Global Registration
app.use(loggerMiddleware);
```

---

## 2. 🔐 Module 2: Environment Variable Management (`dotenv`)

### 2.1 The 12-Factor App Methodology
Hardcoding database credentials, passwords, or secret API keys in code repository creates catastrophic security vulnerabilities. Environment variables decouple configuration from application logic across Development, Staging, and Production environments.

### 2.2 `.env` File Setup & Access
Store secrets in `.env` (never commit `.env` to Git!):

```env
PORT=3000
DB_HOST=localhost
DB_USER=myuser
DB_PASSWORD=mypassword
DB_NAME=mydatabase
DB_PORT=3307
MONGODB_URI=mongodb://localhost:27017/mydatabase
```

In Node.js, load configuration at the earliest entry point:
```javascript
require('dotenv').config();

const port = process.env.PORT || 3000;
const dbHost = process.env.DB_HOST;
```

---

## 3. 🐬 Module 3: Relational Database Integration (MySQL & Docker)

### 3.1 Containerization with Docker Compose
Using Docker eliminates local installation discrepancies and guarantees identical database environments.

#### `docker-compose.yaml`
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: lab6_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: myuser
      MYSQL_PASSWORD: mypassword
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### 3.2 SQL Schema Design
```sql
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    fullname VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    deleted_at DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 3.3 Prepared Statements & SQL Injection Prevention
Always use parameterized queries (`?`) rather than string concatenation:
- ❌ **Insecure:** `db.query("SELECT * FROM users WHERE email = '" + req.params.email + "'")` (Vulnerable to SQL Injection `' OR '1'='1`)
- ✅ **Secure:** `db.query("SELECT * FROM users WHERE email = ?", [email], callback)`

---

## 4. 🗑️ Module 4: Soft Delete Pattern vs. Hard Delete

### 4.1 Theoretical Framework: Hard vs. Soft Delete

| Feature | Hard Delete (`DELETE FROM`) | Soft Delete (`UPDATE ... SET deleted_at`) |
| :--- | :--- | :--- |
| **Physical Data State** | Permanently removed from storage disk | Retained in storage table |
| **Data Recoverability** | Impossible without database backups | Trivial (`UPDATE users SET deleted_at = NULL`) |
| **Audit & Compliance** | Violates financial / regulatory audit trails | Full audit trail preserved |
| **Foreign Key Impact** | Cascades or breaks relational constraints | Maintains relational integrity across tables |
| **Query Complexity** | Standard queries | Must explicitly filter `WHERE deleted_at IS NULL` |

### 4.2 Query Transformation Rules for Soft Delete

1. **READ (All Users):**
   ```sql
   SELECT * FROM users WHERE deleted_at IS NULL;
   ```
2. **READ SINGLE (By Email):**
   ```sql
   SELECT * FROM users WHERE email = ? AND deleted_at IS NULL;
   ```
3. **UPDATE (Password):**
   ```sql
   UPDATE users SET password = ? WHERE email = ? AND deleted_at IS NULL;
   ```
4. **SOFT DELETE Execution:**
   ```sql
   UPDATE users SET deleted_at = NOW() WHERE email = ? AND deleted_at IS NULL;
   ```

---

## 5. 🍃 Module 5: NoSQL & MongoDB Mongoose ODM

### 5.1 Relational (SQL) vs Document (NoSQL) Terminology

| Relational Concept (MySQL) | Document Concept (MongoDB) |
| :--- | :--- |
| Database | Database |
| Table | Collection |
| Row / Record | Document (JSON / BSON format) |
| Column | Field |
| Primary Key (`id`) | Primary Key (`_id` - ObjectId) |

### 5.2 Mongoose Schema & Model Architecture
Mongoose provides a straight-forward, schema-based solution to model application data.

#### `models/User.js`
```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema(
    {
        email: {
            type: String,
            required: true,
            unique: true,
            trim: true,
            lowercase: true,
        },
        fullname: {
            type: String,
            required: true,
        },
        password: {
            type: String,
            required: true,
        },
        deleted_at: {
            type: Date,
            default: null, // Default null for Soft Delete
        },
    },
    {
        timestamps: true, // Automatically manages createdAt & updatedAt fields
    }
);

module.exports = mongoose.model('User', userSchema);
```

### 5.3 Mongoose Asynchronous CRUD Operations

- **Create:** `await User.create({ email, fullname: name, password })`
- **Read All (Active):** `await User.find({ deleted_at: null })`
- **Read Single (Active):** `await User.findOne({ email, deleted_at: null })`
- **Update:** `await User.findOneAndUpdate({ email, deleted_at: null }, { password: newPassword }, { new: true })`
- **Soft Delete:** `await User.findOneAndUpdate({ email, deleted_at: null }, { deleted_at: new Date() }, { new: true })`

---

## 6. 🛠️ Comprehensive Implementation Source Code

### 6.1 `server_mysql.js` (Complete MySQL Implementation)
```javascript
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

// MySQL Database Connection Pool / Connection
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

// 1. CREATE Route
app.post('/create', async (req, res) => {
    const { email, name, password } = req.body;
    try {
        db.query(
            "INSERT INTO users(email, fullname, password) VALUES(?, ?, ?)",
            [email, name, password],
            (err, results, fields) => {
                if (err) {
                    console.log(err);
                    return res.status(400).send();
                }
                res.status(201).json({ message: "User created successfully!", id: results.insertId });
            }
        );
    } catch (err) {
        console.log(err);
        return res.status(500).send();
    }
});

// 2. READ Route (Soft Delete Filtered)
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

// 3. READ SINGLE Route
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

// 4. UPDATE Route
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

// 5. SOFT DELETE Route
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
app.listen(PORT, () => console.log(`Server is running on http://localhost:${PORT}`));
```

### 6.2 `server_mongodb.js` (Complete MongoDB Implementation)
```javascript
const express = require('express');
const mongoose = require('mongoose');
require('dotenv').config();

const User = require('./models/User');

const app = express();
app.use(express.json());

// Custom Logger Middleware
const loggerMiddleware = (req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
};
app.use(loggerMiddleware);

// Database Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/mydatabase')
    .then(() => console.log('MongoDB successfully connected!'))
    .catch((err) => console.error('MongoDB connection error:', err));

// 1. CREATE Route
app.post('/create', async (req, res) => {
    const { email, name, password } = req.body;
    try {
        const newUser = await User.create({ email, fullname: name, password });
        return res.status(201).json({ message: 'New user successfully created!', user: newUser });
    } catch (err) {
        return res.status(400).json({ error: err.message });
    }
});

// 2. READ Route
app.get('/read', async (req, res) => {
    try {
        const users = await User.find({ deleted_at: null });
        return res.status(200).json(users);
    } catch (err) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

// 3. READ SINGLE Route
app.get('/read/single/:email', async (req, res) => {
    const { email } = req.params;
    try {
        const user = await User.findOne({ email, deleted_at: null });
        if (!user) return res.status(404).json({ message: 'User not found or deleted' });
        return res.status(200).json(user);
    } catch (err) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

// 4. UPDATE Route
app.patch('/update/:email', async (req, res) => {
    const { email } = req.params;
    const { newPassword } = req.body;
    try {
        const updatedUser = await User.findOneAndUpdate(
            { email, deleted_at: null },
            { password: newPassword },
            { new: true }
        );
        if (!updatedUser) return res.status(404).json({ message: 'User not found or deleted' });
        return res.status(200).json({ message: 'User password updated successfully!', user: updatedUser });
    } catch (err) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

// 5. SOFT DELETE Route
app.delete('/delete/:email', async (req, res) => {
    const { email } = req.params;
    try {
        const deletedUser = await User.findOneAndUpdate(
            { email, deleted_at: null },
            { deleted_at: new Date() },
            { new: true }
        );
        if (!deletedUser) return res.status(404).json({ message: 'No active user found with that email!' });
        return res.status(200).json({ message: 'User soft-deleted successfully!' });
    } catch (err) {
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`MongoDB Server is running on http://localhost:${PORT}`));
```

---

## 7. 🧪 API Testing & Verification Commands

### Test 1: Create User
```bash
curl -X POST http://localhost:3000/create \
  -H "Content-Type: application/json" \
  -d '{"email": "tawan@kmitl.ac.th", "name": "Tawan Student", "password": "securepassword123"}'
```

### Test 2: Read All Active Users
```bash
curl -X GET http://localhost:3000/read
```

### Test 3: Read Single User
```bash
curl -X GET http://localhost:3000/read/single/tawan@kmitl.ac.th
```

### Test 4: Update Password
```bash
curl -X PATCH http://localhost:3000/update/tawan@kmitl.ac.th \
  -H "Content-Type: application/json" \
  -d '{"newPassword": "newSecretPassword456"}'
```

### Test 5: Soft Delete User
```bash
curl -X DELETE http://localhost:3000/delete/tawan@kmitl.ac.th
```

### Test 6: Verify User is Hidden Post Soft-Delete
```bash
curl -X GET http://localhost:3000/read/single/tawan@kmitl.ac.th
# Expected output: HTTP 404 {"message": "User not found or deleted"}
```

---

## 💡 Key Exam & Quiz Takeaways

1. **Middleware Pipeline:** Middleware executes in strict registration order (`app.use()`). If `next()` is omitted and no response is sent, the request hangs.
2. **Prepared Statements:** Using `?` placeholders prevents SQL injection vulnerabilities by separating SQL instructions from untrusted data parameters.
3. **Soft Delete Mechanics:** Instead of `DELETE FROM table WHERE id = x`, Soft Delete updates a timestamp column (`deleted_at = CURRENT_TIMESTAMP`). All subsequent `SELECT`, `UPDATE`, and `DELETE` queries MUST append `WHERE deleted_at IS NULL`.
4. **Mongoose `new: true` Option:** `findOneAndUpdate()` returns the **old** document before update by default. Passing `{ new: true }` instructs Mongoose to return the **newly updated** document.
5. **NoSQL vs SQL Identity:** SQL uses Tables/Rows/Columns; MongoDB uses Collections/Documents/Fields with auto-generated `_id` primary keys.
