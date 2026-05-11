CREATE DATABASE IF NOT EXISTS depsolve;
USE depsolve;

CREATE TABLE packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL
);

CREATE TABLE dependencies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    dependency_id INT NOT NULL,
    min_version VARCHAR(20),
    FOREIGN KEY (package_id) REFERENCES packages(id) ON DELETE CASCADE,
    FOREIGN KEY (dependency_id) REFERENCES packages(id) ON DELETE CASCADE
);

CREATE TABLE installed_packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    install_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (package_id) REFERENCES packages(id) ON DELETE CASCADE
);