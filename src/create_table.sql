DROP DATABASE IF EXISTS `social_media`;

CREATE DATABASE IF NOT EXISTS `social_media`;

USE `social_media`;

CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `gender` ENUM('male', 'female', 'other') NOT NULL,
    `date_of_birth` DATE
);

CREATE TABLE IF NOT EXISTS `admins` (
    `admin_id` INT AUTO_INCREMENT PRIMARY KEY,
    `password` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `friends` (
    `user_id` INT,
    `friend_id` INT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`, `friend_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`friend_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
    CHECK (`user_id` != `friend_id`)
);

CREATE TABLE IF NOT EXISTS `friend_groups` (
    `group_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT,
    `group_name` VARCHAR(50) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
    UNIQUE KEY (`user_id`, `group_name`)
);

CREATE TABLE IF NOT EXISTS `friend_group_members` (
    `group_id` INT,
    `friend_id` INT,
    `added_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`group_id`, `friend_id`),
    FOREIGN KEY (`group_id`) REFERENCES `friend_groups`(`group_id`) ON DELETE CASCADE,
    FOREIGN KEY (`friend_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `posts` (
    `post_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT,
    `content` VARCHAR(200) NOT NULL,
    `visibility` ENUM('public', 'friends', 'private') NOT NULL DEFAULT 'public',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
    CHECK (CHAR_LENGTH(`content`) <= 200)
);

CREATE TABLE IF NOT EXISTS `comments` (
    `comment_id` INT AUTO_INCREMENT PRIMARY KEY,
    `post_id` INT,
    `user_id` INT,
    `content` VARCHAR(200) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`post_id`) REFERENCES `posts`(`post_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`) ON DELETE CASCADE,
    CHECK (CHAR_LENGTH(`content`) <= 200)
);

DROP TRIGGER IF EXISTS after_friend_delete;

DROP USER IF EXISTS 'app_user' @'localhost';

DROP USER IF EXISTS 'app_admin' @'localhost';

CREATE USER 'app_user' @'localhost' IDENTIFIED BY '0123456789';

GRANT SELECT,INSERT,UPDATE,DELETE ON `social_media`.* TO 'app_user' @'localhost';

CREATE USER 'app_admin' @'localhost' IDENTIFIED BY '9876543210';

GRANT ALL PRIVILEGES ON `social_media`.* TO 'app_admin' @'localhost' WITH GRANT OPTION;

INSERT INTO
    `admins` (password)
VALUES
    ('9876543210');

INSERT INTO
    `users` (username, password, gender)
VALUES
    ('aaa', 'aaaaaaaa', 'male'),
    ('bbb', 'bbbbbbbb', 'female'),
    ('ccc', 'cccccccc', 'other');