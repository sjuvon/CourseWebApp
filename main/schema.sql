DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS welcome;
DROP TABLE IF EXISTS announcement;
DROP TABLE IF EXISTS homework;
DROP TABLE IF EXISTS lecture;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL DEFAULT 1 );


CREATE TABLE role (
    id INTEGER PRIMARY KEY,
    role_name TEXT UNIQUE NOT NULL DEFAULT 'student',
    CHECK (id >= 1 AND id <= 4),
    FOREIGN KEY (id) REFERENCES user (role_id) );
        /*
            'student'   <~~~>   1
            'grader'    <~~~>   2
            'TA'        <~~~>   3
            'professor' <~~~>   4
        */


CREATE TABLE welcome (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    greeting TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id) );


CREATE TABLE announcement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_text TEXT NOT NULL,
    updated_text TEXT,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id) );


CREATE TABLE homework (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Zahl INTEGER NOT NULL,
    due TEXT NOT NULL,
    title TEXT NOT NULL,
    keywords TEXT NOT NULL,
    file_homework TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id) );


CREATE TABLE lecture (
    id INTEGER PRIMARY KEY NOT NULL,
    Zahl INTEGER NOT NULL,
    week INTEGER NOT NULL,
    day TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    file_lecture TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id) );


