-- DaVinci Resolve commands database
CREATE TABLE IF NOT EXISTS davinci_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    api_method TEXT NOT NULL,
    parameters TEXT,
    example_usage TEXT NOT NULL,
    python_code TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    safety_level TEXT DEFAULT 'safe',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS command_examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_id INTEGER NOT NULL,
    natural_language TEXT NOT NULL,
    expected_code TEXT NOT NULL,
    context_tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (command_id) REFERENCES davinci_commands (id)
);

CREATE TABLE IF NOT EXISTS user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT NOT NULL UNIQUE,
    setting_value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    generated_code TEXT,
    executed BOOLEAN DEFAULT FALSE,
    execution_result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
); 