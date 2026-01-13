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

-- Snapshot results
CREATE INDEX idx_snapshot_languages_snapshot_id ON snapshot_languages (snapshot_id);

CREATE INDEX idx_snapshot_frameworks_snapshot_id ON snapshot_frameworks (snapshot_id);

-- Analysis config lookups
CREATE INDEX idx_analysis_ignored_directory_is_active ON analysis_ignored_directory (is_active);

CREATE INDEX idx_analysis_language_rule_is_active ON analysis_language_rule (is_active);

CREATE INDEX idx_analysis_framework_is_active ON analysis_framework (is_active);

CREATE INDEX idx_analysis_framework_rule_is_active ON analysis_framework_rule (is_active);

CREATE INDEX idx_analysis_framework_rule_signal ON analysis_framework_rule (signal_type, signal_value);

-- ==================================================
-- INFRASTRUCTURE INDEXES
-- ==================================================
CREATE INDEX idx_analysis_infra_component_is_active ON analysis_infra_component (is_active);

CREATE INDEX idx_analysis_infra_rule_is_active ON analysis_infra_rule (is_active);

CREATE INDEX idx_analysis_infra_rule_signal ON analysis_infra_rule (signal_type, signal_value);

CREATE INDEX idx_snapshot_infrastructure_snapshot_id ON snapshot_infrastructure (snapshot_id);

-- ==================================================
-- API ENDPOINTS INDEXES
-- ==================================================
CREATE INDEX idx_api_endpoints_snapshot ON api_endpoints (snapshot_id);
CREATE INDEX idx_api_endpoints_signature
ON api_endpoints (http_method, path);
