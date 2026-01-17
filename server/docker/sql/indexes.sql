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
CREATE INDEX idx_snapshots_project_type ON snapshots (project_id, analysis_type, created_at);

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

CREATE INDEX idx_api_endpoints_signature ON api_endpoints (http_method, path);

-- ==================================================
-- PROJECT DEPENDENCIES INDEXES
-- ==================================================
CREATE INDEX idx_project_dependencies_snapshot ON project_dependencies (snapshot_id);

CREATE INDEX idx_project_dependencies_signature ON project_dependencies (name, ecosystem);

CREATE INDEX idx_project_dependencies_ecosystem ON project_dependencies (ecosystem);

-- ==================================================
-- OBSERVATION AI INDEXES
-- ==================================================

CREATE INDEX idx_observation_session_project
    ON observation_session(project_id);

CREATE INDEX idx_observation_question_session
    ON observation_question(session_id);

CREATE INDEX idx_observation_tool_call_question
    ON observation_tool_call(question_id);

CREATE INDEX idx_observation_tool_call_tool_name
    ON observation_tool_call(tool_name);

CREATE INDEX idx_observation_tool_call_result_gin
    ON observation_tool_call
    USING GIN (tool_result);

CREATE INDEX idx_observation_tool_call_args_gin
    ON observation_tool_call
    USING GIN (tool_arguments);
