-- EVENTS
CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    photo VARCHAR(255),
    location VARCHAR(255),
    date VARCHAR(255) NOT NULL,
    -- ends_at TIMESTAMP NOT NULL,
    max_participants INTEGER,
    color VARCHAR(16),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MEMBERS
CREATE TABLE IF NOT EXISTS member (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'participant',
    UNIQUE(event_id, user_id)
);