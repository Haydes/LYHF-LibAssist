CREATE TABLE IF NOT EXISTS users (
    username text PRIMARY KEY,
    password blob,
    isadmin integer
);
