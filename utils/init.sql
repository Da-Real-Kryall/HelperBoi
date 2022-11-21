CREATE TABLE IF NOT EXISTS `users` (
    `discord_id` INT NOT NULL,
    `balance` INT NOT NULL,
    `coolness` INT NOT NULL,
    `slaps` INT NOT NULL,
    `permission_level` INT NOT NULL,
    `blocked` INT NOT NULL,
    PRIMARY KEY (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `suggestions` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INT NOT NULL,
    `content` TEXT NOT NULL,
    `timestamp` INT NOT NULL,
    CONSTRAINT `user_id`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `bugreports` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INT NOT NULL,
    `content` TEXT NOT NULL,
    `timestamp` INT NOT NULL,
    CONSTRAINT `user_id`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `cards_against_humanity` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INT NOT NULL,
    `content` TEXT NOT NULL,
    `type` INT NOT NULL, -- 0 = white, 1 = black
    CONSTRAINT `user_id`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `reminders` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` INT NOT NULL,
    `content` TEXT NOT NULL,
    `timestamp` INT NOT NULL,
    `channel_id` INT NOT NULL,
    CONSTRAINT `user_id`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `inventory` (
    `user_id` INT NOT NULL,
    `item_name` TEXT NOT NULL,
    `quantity` INT NOT NULL,
    CONSTRAINT `user_id`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `cooldowns` (
    `user_id` INT NOT NULL,
    `name` TEXT NOT NULL,
    `timestamp` INT NOT NULL,
    CONSTRAINT `user_id`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `user_settings` (
    `user_id` INT NOT NULL,
    `option` TEXT NOT NULL,
    `value` INT NOT NULL,
    CONSTRAINT `user_id`
        FOREIGN KEY (`user_id`)
        REFERENCES `users` (`discord_id`)
);

CREATE TABLE IF NOT EXISTS `guild_settings` (
    `guild_id` INT NOT NULL,
    `option` TEXT NOT NULL,
    `value` INT NOT NULL,
    PRIMARY KEY (`guild_id`, `option`)
);
