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