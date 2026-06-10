const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

// Create tables if they don't exist
const initializeDatabase = async () => {
  const createUsersTableQuery = `
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      full_name VARCHAR(100) NOT NULL,
      email VARCHAR(100) UNIQUE NOT NULL,
      password VARCHAR(255) NOT NULL,
      age INTEGER,
      country VARCHAR(100),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;
  try {
    await pool.query(createUsersTableQuery);
    console.log("Database initialized (users table dropped and recreated with new fields).");
  } catch (err) {
    console.error("Error initializing database:", err);
  }
};

initializeDatabase();

module.exports = {
  query: (text, params) => pool.query(text, params),
};
