require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('./database');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

// Serve static files from the current directory
app.use(express.static(__dirname));

// --- API Endpoints ---

// Register Endpoint
app.post('/api/register', async (req, res) => {
  const { fullName, email, password, age, country } = req.body;
  if (!fullName || !email || !password || !age || !country) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  try {
    // Check if user exists
    const userCheck = await db.query('SELECT * FROM users WHERE email = $1', [email]);
    if (userCheck.rows.length > 0) {
      return res.status(409).json({ error: 'Email already exists' });
    }

    // Hash password and save
    const hashedPassword = await bcrypt.hash(password, 10);
    await db.query(
      'INSERT INTO users (full_name, email, password, age, country) VALUES ($1, $2, $3, $4, $5)', 
      [fullName, email, hashedPassword, age, country]
    );
    
    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Login Endpoint
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  try {
    const result = await db.query('SELECT * FROM users WHERE email = $1', [email]);
    const user = result.rows[0];

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate JWT Token
    const token = jwt.sign({ id: user.id, email: user.email, name: user.full_name }, process.env.JWT_SECRET, { expiresIn: '24h' });
    
    res.json({ message: 'Login successful', token, name: user.full_name });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Delete Account Endpoint
app.delete('/api/user', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    await db.query('DELETE FROM users WHERE id = $1', [decoded.id]);
    res.json({ message: 'Account deleted successfully' });
  } catch (error) {
    console.error('Delete error:', error);
    res.status(401).json({ error: 'Invalid token' });
  }
});
// Delete Account Endpoint
app.delete('/api/user', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    await db.query('DELETE FROM users WHERE id = $1', [decoded.id]);
    res.json({ message: 'Account deleted successfully' });
  } catch (error) {
    console.error('Delete error:', error);
    res.status(401).json({ error: 'Invalid token' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
