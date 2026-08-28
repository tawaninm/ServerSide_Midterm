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

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI, { dbName: 'mydatabase' })
    .then(() => console.log('MongoDB successfully connected to mydatabase!'))
    .catch((err) => console.error('MongoDB connection error:', err));

// ==========================================
// ROUTES (MongoDB / Mongoose CRUD)
// ==========================================

// 1. CREATE Route: Add a new user
app.post('/create', async (req, res) => {
    const { email, name, password } = req.body;
    try {
        const newUser = await User.create({
            email,
            fullname: name,
            password,
        });

        return res.status(201).json({
            message: 'New user successfully created!',
            user: newUser,
        });
    } catch (err) {
        console.error('Error while inserting a user into the database', err);
        return res.status(400).json({ error: err.message });
    }
});

// 2. READ Route: Get active users only (deleted_at is null)
app.get('/read', async (req, res) => {
    try {
        const users = await User.find({ deleted_at: null });
        return res.status(200).json(users);
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

// 3. READ SINGLE Route: Get single active user by email
app.get('/read/single/:email', async (req, res) => {
    const { email } = req.params;
    try {
        const user = await User.findOne({ email, deleted_at: null });
        if (!user) {
            return res.status(404).json({ message: 'User not found or deleted' });
        }
        return res.status(200).json(user);
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

// 4. UPDATE Route: Update password of active user
app.patch('/update/:email', async (req, res) => {
    const { email } = req.params;
    const { newPassword } = req.body;

    try {
        const updatedUser = await User.findOneAndUpdate(
            { email, deleted_at: null }, // search condition
            { password: newPassword },    // data to update
            { new: true }                 // return updated document
        );

        if (!updatedUser) {
            return res.status(404).json({ message: 'User not found or deleted' });
        }

        return res.status(200).json({
            message: 'User password updated successfully!',
            user: updatedUser,
        });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

// 5. SOFT DELETE Route: Set deleted_at timestamp
app.delete('/delete/:email', async (req, res) => {
    const { email } = req.params;
    try {
        const deletedUser = await User.findOneAndUpdate(
            { email, deleted_at: null },
            { deleted_at: new Date() },
            { new: true }
        );

        if (!deletedUser) {
            return res.status(404).json({ message: 'No active user found with that email!' });
        }

        return res.status(200).json({ message: 'User soft-deleted successfully!' });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`MongoDB Server is running on http://localhost:${PORT}`);
});
