-- =========================
-- ENUM TYPES
-- =========================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'job_description_type') THEN
        CREATE TYPE job_description_type AS ENUM ('PERMANENT', 'CONTRACT', 'WORK_MODE');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'employment_mode') THEN
        CREATE TYPE employment_mode AS ENUM ('FULL_TIME', 'PART_TIME');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'application_status') THEN
        CREATE TYPE application_status AS ENUM ('PENDING', 'REVIEWED', 'REJECTED', 'HIRED');
    END IF;
END$$;

-- =========================
-- TABLES
-- =========================

CREATE TABLE society (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    url         VARCHAR(512),
    logo        VARCHAR(512)
);

CREATE TABLE job_description (
    id          BIGSERIAL PRIMARY KEY,
    type        job_description_type NOT NULL,
    details     TEXT
);

-- Only for CONTRACT type
CREATE TABLE contract_term (
    id                  BIGSERIAL PRIMARY KEY,
    job_description_id  BIGINT NOT NULL UNIQUE
        REFERENCES job_description(id) ON DELETE CASCADE,
    duration_years      INT NOT NULL DEFAULT 0,
    duration_months     INT NOT NULL DEFAULT 0,
    duration_days       INT NOT NULL DEFAULT 0,
    CHECK (duration_years >= 0 AND duration_months >= 0 AND duration_days >= 0),
    CHECK (duration_years + duration_months + duration_days > 0)
);

-- Only for WORK_MODE type
CREATE TABLE job_description_mode (
    id                  BIGSERIAL PRIMARY KEY,
    job_description_id  BIGINT NOT NULL UNIQUE
        REFERENCES job_description(id) ON DELETE CASCADE,
    mode                employment_mode NOT NULL
);

CREATE TABLE job (
    id                  BIGSERIAL PRIMARY KEY,
    title               VARCHAR(255) NOT NULL,
    requirements        TEXT,
    society_id          BIGINT NOT NULL REFERENCES society(id) ON DELETE RESTRICT,
    job_description_id  BIGINT NOT NULL REFERENCES job_description(id) ON DELETE RESTRICT,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidate (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    email           VARCHAR(255) NOT NULL,
    phone           VARCHAR(50),
    cv_url          VARCHAR(512),
    address         VARCHAR(512),
    other_details   JSONB
);

CREATE TABLE application (
    id              BIGSERIAL PRIMARY KEY,
    job_id          BIGINT NOT NULL REFERENCES job(id) ON DELETE CASCADE,
    candidate_id    BIGINT NOT NULL REFERENCES candidate(id) ON DELETE CASCADE,
    applied_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status          application_status NOT NULL DEFAULT 'PENDING',
    UNIQUE (job_id, candidate_id)  -- Prevent duplicate applications to the same job by the same candidate
);

-- Helpful indexes
CREATE INDEX idx_job_society_id ON job(society_id);
CREATE INDEX idx_job_job_description_id ON job(job_description_id);
CREATE INDEX idx_application_job_id ON application(job_id);
CREATE INDEX idx_application_candidate_id ON application(candidate_id);
