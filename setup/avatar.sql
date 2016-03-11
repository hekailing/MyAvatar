CREATE DATABASE avatar_test;
USE avatar_test;
CREATE TABLE user_info(username VARCHAR(20) PRIMARY KEY,
                       password CHAR(64) NOT NULL,
                       salt CHAR(64) NOT NULL,
                       email VARCHAR(32) NOT NULL); 

CREATE TABLE email2user(email VARCHAR(32) PRIMARY KEY,
                       username VARCHAR(20) NOT NULL);
quit

