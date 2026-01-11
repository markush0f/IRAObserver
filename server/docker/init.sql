-- ==================================================
-- EXTENSIONS
-- ==================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==================================================
-- USERS
-- Global identity inside the instance
-- ==================================================
CREATE TABLE
    users (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        display_name TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL, -- 'admin', 'all', 'writer', 'reader'
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );

-- ==================================================
-- USER PREFERENCES
-- Personal configuration shared across devices
-- ==================================================
CREATE TABLE
    user_preferences (
        user_id UUID PRIMARY KEY REFERENCES users (id) ON DELETE CASCADE,
        theme TEXT DEFAULT 'dark',
        default_project_id UUID,
        ui_density TEXT DEFAULT 'comfortable',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );

-- ==================================================
-- PROJECTS
-- Observed projects inside the instance
-- ==================================================
CREATE TABLE
    projects (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        name TEXT NOT NULL,
        description TEXT,
        source_type TEXT NOT NULL, -- 'github', 'gitlab', 'local'
        source_ref TEXT NOT NULL, -- repo url or local path
        created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
        last_analysis_at TIMESTAMPTZ
    );

-- ==================================================
-- MEMBERSHIPS
-- Access control: user <-> project
-- ==================================================
CREATE TABLE
    memberships (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        user_id UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        project_id UUID NOT NULL REFERENCES projects (id) ON DELETE CASCADE,
        role TEXT NOT NULL, -- 'admin', 'member', 'viewer'
        created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
        revoked_at TIMESTAMPTZ,
        UNIQUE (user_id, project_id)
    );

-- ==================================================
-- INVITE CODES
-- Temporary access gate controlled by admins
-- ==================================================
CREATE TABLE
    invite_codes (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        code TEXT NOT NULL UNIQUE,
        created_by_user_id UUID REFERENCES users (id) ON DELETE SET NULL,
        project_id UUID REFERENCES projects (id) ON DELETE CASCADE,
        role_granted TEXT NOT NULL, -- role assigned on accept
        max_uses INTEGER DEFAULT 1,
        used_count INTEGER NOT NULL DEFAULT 0,
        expires_at TIMESTAMPTZ NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );

-- ==================================================
-- SESSIONS
-- Server-side sessions (multi-device support)
-- ==================================================
CREATE TABLE
    sessions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        user_id UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
        expires_at TIMESTAMPTZ NOT NULL,
        last_seen_at TIMESTAMPTZ,
        revoked_at TIMESTAMPTZ
    );

-- ==================================================
-- SNAPSHOTS
-- State of a project at a given point in time
-- ==================================================
CREATE TABLE
    snapshots (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        project_id UUID NOT NULL REFERENCES projects (id) ON DELETE CASCADE,
        commit_hash TEXT,
        summary_json JSONB NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );

-- ==================================================
-- TIMELINE EVENTS
-- Changes detected between snapshots
-- ==================================================
CREATE TABLE
    timeline_events (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        project_id UUID NOT NULL REFERENCES projects (id) ON DELETE CASCADE,
        snapshot_id UUID REFERENCES snapshots (id) ON DELETE CASCADE,
        event_type TEXT NOT NULL, -- 'endpoint_added', 'endpoint_changed', etc.
        severity TEXT NOT NULL, -- 'low', 'medium', 'high', 'critical'
        payload_json JSONB NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );

-- ==================================================
-- INSIGHTS
-- AI / heuristic observations
-- ==================================================
CREATE TABLE
    insights (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        project_id UUID NOT NULL REFERENCES projects (id) ON DELETE CASCADE,
        snapshot_id UUID REFERENCES snapshots (id) ON DELETE CASCADE,
        level TEXT NOT NULL, -- 'info', 'warning', 'critical'
        message TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );

-- ==================================================
-- SNAPSHOT LANGUAGES
-- Detected languages for a snapshot
-- ==================================================
CREATE TABLE
    snapshot_languages (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
        snapshot_id UUID NOT NULL REFERENCES snapshots (id) ON DELETE CASCADE,
        language TEXT NOT NULL,
        weight INTEGER NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
        UNIQUE (snapshot_id, language)
    );

-- ==================================================
-- ANALYSIS IGNORED FOR DIRECTORY
-- ==================================================
CREATE TABLE
    analysis_ignored_directory (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        name TEXT NOT NULL UNIQUE,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now ()
    );

INSERT INTO
    analysis_ignored_directory (name)
VALUES
    ('__pycache__'),
    ('.git'),
    ('.idea'),
    ('.vscode'),
    ('node_modules'),
    ('.venv'),
    ('venv'),
    ('dist'),
    ('build');

-- ==================================================
-- RULES FOR DETECT LANGUAGES
-- ==================================================
CREATE TABLE
    analysis_language_rule (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        extension TEXT NOT NULL,
        language TEXT NOT NULL,
        weight INTEGER NOT NULL DEFAULT 1,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now (),
        UNIQUE (extension, language)
    );

INSERT INTO
    analysis_language_rule (extension, language, weight)
VALUES
    ('.py', 'Python', 10),
    ('.pyi', 'Python', 3),
    ('.js', 'JavaScript', 8),
    ('.ts', 'TypeScript', 9),
    ('.java', 'Java', 9),
    ('.go', 'Go', 9),
    ('.rs', 'Rust', 9),
    ('.cs', 'C#', 8),
    ('.php', 'PHP', 7),
    ('.rb', 'Ruby', 7);

-- ==================================================
-- INDEXES (performance-critical)
-- ==================================================
CREATE INDEX idx_users_role ON users (role);

CREATE INDEX idx_users_is_active ON users (is_active);

CREATE INDEX idx_memberships_user_id ON memberships (user_id);

CREATE INDEX idx_memberships_project_id ON memberships (project_id);

CREATE INDEX idx_sessions_user_id ON sessions (user_id);

CREATE INDEX idx_sessions_expires_at ON sessions (expires_at);

CREATE INDEX idx_snapshots_project_id ON snapshots (project_id);

CREATE INDEX idx_timeline_events_project_id ON timeline_events (project_id);

CREATE INDEX idx_timeline_events_severity ON timeline_events (severity);

CREATE INDEX idx_insights_project_id ON insights (project_id);

CREATE INDEX idx_insights_level ON insights (level);