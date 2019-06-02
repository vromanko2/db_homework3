CREATE DATABASE university;
ALTER DATABASE university CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'newuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON university.* TO 'newuser'@'%';
FLUSH PRIVILEGES;