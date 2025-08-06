-- =========
-- ENUMs
-- =========
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'question_type') THEN
        CREATE TYPE question_type AS ENUM ('TEXT', 'MCQ', 'SINGLE_OPTION', 'MULTIPLE_OPTIONS', 'CUSTOM');
    END IF;
END$$;

-- =========
-- TABLES
-- =========

CREATE TABLE form_template (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    version         INT NOT NULL DEFAULT 1,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE job (
    id                  BIGSERIAL PRIMARY KEY,
    title               VARCHAR(255) NOT NULL,
    description         TEXT,
    form_template_id    BIGINT UNIQUE REFERENCES form_template(id) ON DELETE SET NULL,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE question (
    id                  BIGSERIAL PRIMARY KEY,
    template_id         BIGINT NOT NULL REFERENCES form_template(id) ON DELETE CASCADE,
    order_index         INT NOT NULL,
    label               VARCHAR(255) NOT NULL,
    help_text           TEXT,
    type                question_type NOT NULL,
    is_required         BOOLEAN NOT NULL DEFAULT FALSE,
    validation_rules    JSONB,          -- e.g., {"regex":"...", "min": 3, "max": 50}
    custom_schema       JSONB,          -- used when type = CUSTOM
    CONSTRAINT uq_question_template_order UNIQUE (template_id, order_index)
);

CREATE TABLE question_option (
    id              BIGSERIAL PRIMARY KEY,
    question_id     BIGINT NOT NULL REFERENCES question(id) ON DELETE CASCADE,
    label           VARCHAR(255) NOT NULL,
    value           VARCHAR(255) NOT NULL,
    order_index     INT NOT NULL,
    CONSTRAINT uq_option_question_order UNIQUE (question_id, order_index)
);

CREATE TABLE form_submission (
    id              BIGSERIAL PRIMARY KEY,
    job_id          BIGINT NOT NULL REFERENCES job(id) ON DELETE CASCADE,
    template_id     BIGINT NOT NULL REFERENCES form_template(id) ON DELETE RESTRICT,
    applicant_id    BIGINT NOT NULL,  -- Link to your applicants/users table if you have one
    submitted_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status          VARCHAR(50) NOT NULL DEFAULT 'SUBMITTED'
);

CREATE TABLE answer (
    id              BIGSERIAL PRIMARY KEY,
    submission_id   BIGINT NOT NULL REFERENCES form_submission(id) ON DELETE CASCADE,
    question_id     BIGINT NOT NULL REFERENCES question(id) ON DELETE CASCADE,
    value_text      TEXT,               -- used for TEXT / CUSTOM
    option_id       BIGINT REFERENCES question_option(id) ON DELETE SET NULL, -- for SINGLE_OPTION / MCQ (single select)
    option_ids      JSONB,              -- for MULTIPLE_OPTIONS (array of option IDs)
    CONSTRAINT uq_answer_submission_question UNIQUE (submission_id, question_id),
    CONSTRAINT ck_answer_has_some_value CHECK (
        value_text IS NOT NULL OR option_id IS NOT NULL OR option_ids IS NOT NULL
    )
);

-- Helpful indexes
CREATE INDEX idx_job_form_template_id ON job(form_template_id);
CREATE INDEX idx_question_template_id ON question(template_id);
CREATE INDEX idx_question_option_question_id ON question_option(question_id);
CREATE INDEX idx_form_submission_job_id ON form_submission(job_id);
CREATE INDEX idx_form_submission_template_id ON form_submission(template_id);
CREATE INDEX idx_answer_submission_id ON answer(submission_id);
CREATE INDEX idx_answer_question_id ON answer(question_id);
