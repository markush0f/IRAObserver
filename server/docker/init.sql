-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--------------------------------------------------
-- USERS
-- Persistent identity, created after accepting an invite
--------------------------------------------------
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    display_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

--------------------------------------------------
-- USER PREFERENCES
-- Personal configuration, shared across devices
--------------------------------------------------
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    theme TEXT DEFAULT 'dark',
    default_project_id UUID,
    ui_density TEXT DEFAULT 'comfortable',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

--------------------------------------------------
-- PROJECTS
-- Observed projects inside the instance
--------------------------------------------------
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    source_type TEXT NOT NULL, -- 'github', 'local'
    source_ref TEXT NOT NULL,  -- repo url or local path
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_analysis_at TIMESTAMPTZ
);

--------------------------------------------------
-- MEMBERSHIPS
-- Access control: user <-> project
--------------------------------------------------
CREATE TABLE memberships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    role TEXT NOT NULL, -- 'admin', 'member', 'viewer'
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    revoked_at TIMESTAMPTZ,
    UNIQUE (user_id, project_id)
);

--------------------------------------------------
-- INVITE CODES
-- Temporary access gate controlled by admin
--------------------------------------------------
CREATE TABLE invite_codes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code TEXT NOT NULL UNIQUE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    role_granted TEXT NOT NULL, -- role assigned on accept
    max_uses INTEGER DEFAULT 1,
    used_count INTEGER NOT NULL DEFAULT 0,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

--------------------------------------------------
-- SESSIONS
-- Server-side sessions (multi-device support)
--------------------------------------------------
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    last_seen_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);

--------------------------------------------------
-- SNAPSHOTS
-- State of a project at a given point in time
--------------------------------------------------
CREATE TABLE snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    commit_hash TEXT,
    summary_json JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

--------------------------------------------------
-- TIMELINE EVENTS
-- Changes detected between snapshots
--------------------------------------------------
CREATE TABLE timeline_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    snapshot_id UUID REFERENCES snapshots(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL, -- e.g. 'endpoint_added', 'endpoint_changed'
    severity TEXT NOT NULL,   -- 'low', 'medium', 'high', 'critical'
    payload_json JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

--------------------------------------------------
-- INSIGHTS
-- AI / heuristic observations
--------------------------------------------------
CREATE TABLE insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    snapshot_id UUID REFERENCES snapshots(id) ON DELETE CASCADE,
    level TEXT NOT NULL, -- 'info', 'warning', 'critical'
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

--------------------------------------------------
-- INDEXES (important for performance)
--------------------------------------------------
CREATE INDEX idx_memberships_user_id ON memberships(user_id);
CREATE INDEX idx_memberships_project_id ON memberships(project_id);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_snapshots_project_id ON snapshots(project_id);
CREATE INDEX idx_timeline_project_id ON timeline_events(project_id);
CREATE INDEX idx_insights_project_id ON insights(project_id);
