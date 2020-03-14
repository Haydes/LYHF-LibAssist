CREATE TABLE IF NOT EXISTS users (
    username text PRIMARY KEY NOT NULL,
    password blob,
    isadmin integer,
    bookISBN integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS book (
    ISBN integer PRIMARY KEY NOT NULL,
    title text,
    author text,
    pubDate text,
    username text,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE
);

