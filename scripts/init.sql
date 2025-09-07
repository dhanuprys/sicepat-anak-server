-- Database initialization script for Stunting Checking App
-- This script will be run when MySQL container starts

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS stunting_db;
USE stunting_db;

-- Create user if not exists
CREATE USER IF NOT EXISTS 'stunting_user'@'%' IDENTIFIED BY 'stunting_password';
GRANT ALL PRIVILEGES ON stunting_db.* TO 'stunting_user'@'%';
FLUSH PRIVILEGES;

-- Note: Tables will be created by Alembic migrations
-- This script just ensures the database and user exist
