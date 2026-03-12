-- FitCoach AI  —  MySQL Schema
-- Run this script to initialise the database:
--   mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS fitcoach
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE fitcoach;

-- -----------------------------------------------
-- Users
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
) ENGINE=InnoDB;

-- -----------------------------------------------
-- Profiles
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS profiles (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    user_id  INT          NOT NULL UNIQUE,
    name     VARCHAR(100) NOT NULL,
    age      INT          NOT NULL,
    sex      VARCHAR(10)  NOT NULL,
    height   FLOAT        NOT NULL,
    weight   FLOAT        NOT NULL,
    body_fat FLOAT        NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------
-- Goals
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS goals (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT         NOT NULL UNIQUE,
    goal_type      VARCHAR(50) NOT NULL,
    activity_level VARCHAR(50) NOT NULL,
    calorie_target FLOAT       NULL,
    protein        FLOAT       NULL,
    carbs          FLOAT       NULL,
    fat            FLOAT       NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------
-- Progress Logs
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS progress_logs (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    user_id  INT   NOT NULL,
    weight   FLOAT NOT NULL,
    body_fat FLOAT NULL,
    date     DATE  DEFAULT (CURRENT_DATE),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_progress_user_date (user_id, date)
) ENGINE=InnoDB;
