-- USERS
CREATE TABLE IF NOT EXISTS user_ (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_spbsu_student BOOLEAN NOT NULL DEFAULT FALSE,
    university TEXT,
    faculty TEXT,
    speciality TEXT,
    course INTEGER,
    photo TEXT,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TEXT
);

-- REFRESH TOKENS
CREATE TABLE IF NOT EXISTS refresh_token (
    id SERIAL PRIMARY KEY,
    token TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (user_id) REFERENCES user_(id) ON DELETE CASCADE
);
