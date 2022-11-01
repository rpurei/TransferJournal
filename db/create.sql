# INSERT INTO user_roles(`name`) VALUES (N'Администратор'),(N'Курьер'),(N'Делопроизводитель')
#
# CREATE TABLE `privileges` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`name` VARCHAR(255) NOT NULL,
# 	`description` TEXT,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`active` BOOLEAN NOT NULL DEFAULT TRUE,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `user_privileges` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`user_id` INT NOT NULL,
# 	`privilege_id` INT NOT NULL,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`active` BOOLEAN NOT NULL DEFAULT TRUE,
# 	PRIMARY KEY (`id`)
# );

# INSERT INTO `privileges`(`name`) VALUES ('admin'),('courier'),('clerk')
# INSERT INTO `user_privileges`(`user_id`,`privilege_id`) VALUES ('1', '1')

###########################
# CREATE TABLE `users` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`login` VARCHAR(255) NOT NULL,
# 	`token` VARCHAR(128),
# 	`role_id` INT NOT NULL,
# 	`name` VARCHAR(255) NOT NULL,
# 	`email` VARCHAR(255) NOT NULL,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`active` BOOLEAN NOT NULL,
# 	PRIMARY KEY (`id`)
# );

# CREATE TABLE `user_roles` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`name` VARCHAR(255) NOT NULL,
# 	`description` TEXT,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	`updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
# 	`active` BOOLEAN NOT NULL DEFAULT TRUE,
# 	PRIMARY KEY (`id`)
# );
#
# INSERT INTO user_roles(`name`) VALUES (N'Администратор'),(N'Пользователь')

# CREATE TABLE `docs_statuses` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`login` VARCHAR(255) NOT NULL,
#     `directum_paper_id` VARCHAR(32) NOT NULL,
# 	`operation` VARCHAR(128),
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `docs_contents` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
#     `directum_paper_id` VARCHAR(32) NOT NULL,
# 	`directum_name` VARCHAR(512),
# 	`directum_id` INTEGER,
# 	`created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	PRIMARY KEY (`id`)
# );
#
# CREATE TABLE `docs_transactions` (
# 	`id` INT NOT NULL AUTO_INCREMENT,
# 	`login` VARCHAR(255) NOT NULL,
# 	`transaction_id` VARCHAR(64) NOT NULL,
#     `directum_paper_id` VARCHAR(32) NOT NULL,
#     `created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
# 	PRIMARY KEY (`id`)
# );