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
            default: null, // default null for Soft Delete
        },
    },
    {
        timestamps: true, // auto generates createdAt and updatedAt
    }
);

module.exports = mongoose.model('User', userSchema);
