-- EVENTS
CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    category TEXT,
    format TEXT NOT NULL DEFAULT 'online',
    name TEXT NOT NULL,
    description TEXT,
    photo TEXT,
    banner TEXT,
    location TEXT,
    address TEXT,
    date TEXT NOT NULL,
    start_time TEXT,
    max_participants INTEGER,
    color TEXT,
    created_at TEXT NOT NULL
);

-- MEMBERS
CREATE TABLE IF NOT EXISTS member (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    role TEXT DEFAULT 'participant',
    UNIQUE(event_id, user_id)
);