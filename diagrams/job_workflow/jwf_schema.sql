
-- ======================
-- 1. JOB TABLE
-- ======================
CREATE TABLE job (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    workflow_template_id BIGINT REFERENCES workflow_template(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- 2. WORKFLOW TEMPLATE
-- ======================
CREATE TABLE workflow_template (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- 3. WORKFLOW STAGE TEMPLATE
-- ======================
CREATE TABLE workflow_stage_template (
    id BIGSERIAL PRIMARY KEY,
    template_id BIGINT NOT NULL REFERENCES workflow_template(id) ON DELETE CASCADE,
    order_index INT NOT NULL,
    stage_name VARCHAR(255) NOT NULL,
    UNIQUE (template_id, order_index)  -- Ensures stage order uniqueness per template
);

-- ======================
-- 4. JOB WORKFLOW (custom per job)
-- ======================
CREATE TABLE job_workflow (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES job(id) ON DELETE CASCADE,
    stage_order INT NOT NULL,
    stage_name VARCHAR(255) NOT NULL,
    UNIQUE (job_id, stage_order)  -- Each stage order must be unique for a job
);

-- ======================
-- 5. STAGE TASK
-- ======================
CREATE TABLE stage_task (
    id BIGSERIAL PRIMARY KEY,
    job_workflow_id BIGINT NOT NULL REFERENCES job_workflow(id) ON DELETE CASCADE,
    task_type VARCHAR(100) NOT NULL,   -- E.g., EVALUATOR_TASK, DOCUMENT_REVIEW
    description TEXT,
    assignee_role VARCHAR(100)         -- E.g., HR, TECH_LEAD
);

-- ======================
-- 6. STAGE NOTIFICATION
-- ======================
CREATE TABLE stage_notification (
    id BIGSERIAL PRIMARY KEY,
    job_workflow_id BIGINT NOT NULL REFERENCES job_workflow(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL CHECK (notification_type IN ('EMAIL', 'SMS')),
    recipient VARCHAR(50) NOT NULL CHECK (recipient IN ('CANDIDATE', 'EVALUATOR')),
    message_template TEXT NOT NULL,
    send_time TIMESTAMP NOT NULL
);

-- ======================
-- 7. CELERY TASK QUEUE (for scheduling notifications)
-- ======================
CREATE TABLE celery_task_queue (
    id BIGSERIAL PRIMARY KEY,
    notification_id BIGINT NOT NULL REFERENCES stage_notification(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDING', 'SENT', 'FAILED')),
    scheduled_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP
);
