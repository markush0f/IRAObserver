-- ==================================================
-- ANALYSIS IGNORED DIRECTORIES
-- ==================================================
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
-- LANGUAGE DETECTION RULES
-- ==================================================
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
-- FRAMEWORK CATALOG
-- ==================================================
INSERT INTO
    analysis_framework (name, category, website)
VALUES
    (
        'FastAPI',
        'backend',
        'https://fastapi.tiangolo.com'
    ),
    (
        'Django',
        'backend',
        'https://www.djangoproject.com'
    ),
    (
        'Flask',
        'backend',
        'https://flask.palletsprojects.com'
    ),
    (
        'Spring Boot',
        'backend',
        'https://spring.io/projects/spring-boot'
    ),
    ('React', 'frontend', 'https://react.dev'),
    ('Vue', 'frontend', 'https://vuejs.org'),
    ('Angular', 'frontend', 'https://angular.io'),
    ('Next.js', 'fullstack', 'https://nextjs.org'),
    ('Astro', 'frontend', 'https://astro.build');

-- ==================================================
-- FRAMEWORK DETECTION RULES
-- ==================================================
-- FastAPI
INSERT INTO
    analysis_framework_rule (framework_id, signal_type, signal_value, weight)
SELECT
    id,
    'python_dependency',
    'fastapi',
    10
FROM
    analysis_framework
WHERE
    name = 'FastAPI';

-- Django
INSERT INTO
    analysis_framework_rule (framework_id, signal_type, signal_value, weight)
SELECT
    id,
    'python_dependency',
    'django',
    10
FROM
    analysis_framework
WHERE
    name = 'Django';

-- React
INSERT INTO
    analysis_framework_rule (framework_id, signal_type, signal_value, weight)
SELECT
    id,
    'node_dependency',
    'react',
    10
FROM
    analysis_framework
WHERE
    name = 'React';

-- Next.js
INSERT INTO
    analysis_framework_rule (framework_id, signal_type, signal_value, weight)
SELECT
    id,
    'node_dependency',
    'next',
    10
FROM
    analysis_framework
WHERE
    name = 'Next.js';

-- Astro
INSERT INTO
    analysis_framework_rule (framework_id, signal_type, signal_value, weight)
SELECT
    id,
    'node_dependency',
    'astro',
    10
FROM
    analysis_framework
WHERE
    name = 'Astro';

-- Spring Boot
INSERT INTO
    analysis_framework_rule (framework_id, signal_type, signal_value, weight)
SELECT
    id,
    'java_dependency',
    'spring-boot-starter-web',
    10
FROM
    analysis_framework
WHERE
    name = 'Spring Boot';

-- ==================================================
-- INFRASTRUCTURE COMPONENTS
-- ==================================================
INSERT INTO
    analysis_infra_component (name, category)
VALUES
    ('Docker', 'container'),
    ('Docker Compose', 'container'),
    ('GitHub Actions', 'ci_cd'),
    ('GitLab CI', 'ci_cd'),
    ('Kubernetes', 'orchestration'),
    ('Helm', 'orchestration'),
    ('Terraform', 'iac'),
    ('Ansible', 'iac'),
    ('Prometheus', 'observability'),
    ('Grafana', 'observability');

-- ==================================================
-- INFRASTRUCTURE DETECTION RULES
-- ==================================================
-- Docker
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'file',
    'Dockerfile'
FROM
    analysis_infra_component
WHERE
    name = 'Docker';

-- Docker Compose
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'file',
    'docker-compose.yml'
FROM
    analysis_infra_component
WHERE
    name = 'Docker Compose';

INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'file',
    'docker-compose.yaml'
FROM
    analysis_infra_component
WHERE
    name = 'Docker Compose';

-- GitHub Actions
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'directory',
    '.github/workflows'
FROM
    analysis_infra_component
WHERE
    name = 'GitHub Actions';

-- GitLab CI
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'file',
    '.gitlab-ci.yml'
FROM
    analysis_infra_component
WHERE
    name = 'GitLab CI';

-- Kubernetes
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'directory',
    'k8s'
FROM
    analysis_infra_component
WHERE
    name = 'Kubernetes';

INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'directory',
    'kubernetes'
FROM
    analysis_infra_component
WHERE
    name = 'Kubernetes';

-- Helm
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'file',
    'Chart.yaml'
FROM
    analysis_infra_component
WHERE
    name = 'Helm';

-- Terraform
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'glob',
    '*.tf'
FROM
    analysis_infra_component
WHERE
    name = 'Terraform';

-- Ansible
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'directory',
    'ansible'
FROM
    analysis_infra_component
WHERE
    name = 'Ansible';

-- Prometheus
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'file',
    'prometheus.yml'
FROM
    analysis_infra_component
WHERE
    name = 'Prometheus';

-- Grafana
INSERT INTO
    analysis_infra_rule (infra_component_id, signal_type, signal_value)
SELECT
    id,
    'directory',
    'grafana'
FROM
    analysis_infra_component
WHERE
    name = 'Grafana';
