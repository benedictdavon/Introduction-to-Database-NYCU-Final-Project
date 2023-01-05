require("dotenv").config();

const { Client } = require("pg");

const isProduction = process.env.NODE_ENV === "production";

const connectionString = `postgresql://${process.env.DB_USER}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_DATABASE}`;

const client = new Client({
  connectionString: isProduction ? process.env.DATABASE_URL : connectionString,
  ssl: isProduction
});

console.log("Database connected!")
module.exports = { client };

// const { Client } = require('pg')
// const client = new Client({
//     user: 'postgres',
//     host: 'dbfinal.c4szyxydtsuk.us-east-1.rds.amazonaws.com',
//     database: 'dbfinal',
//     password: 'mjJ7LO6uCJb9OBOiM9zu',
//     port: 5432,
// })