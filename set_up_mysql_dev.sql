CREATE DATABASE IF NOT EXISTS twittBuzz_dev_db;
CREATE USER IF NOT EXISTS 'twitt_dev'@'localhost' IDENTIFIED BY 'twitt_dev_pwd';
GRANT ALL PRIVILEGES ON `twittBuzz_dev_db`.* TO 'twitt_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'twitt_dev'@'localhost';
FLUSH PRIVILEGES;