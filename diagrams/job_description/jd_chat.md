Below is a **normalized PostgreSQL schema (DDL)** for your ERD, plus **sample INSERT data**, and **triggers** that *enforce the business rules about contract duration vs. work mode*.
I chose to **avoid nullable / misused columns** by splitting duration and work‑mode into **separate child tables** of `job_description`.

---

## 1) DDL (PostgreSQL)

```sql
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
```

---

## 2) Triggers (business-rule enforcement)

**Rules we enforce:**

* If `job_description.type = 'CONTRACT'` → **must have** exactly **one** `contract_term`, and **must NOT** have a `job_description_mode`.
* If `job_description.type = 'WORK_MODE'` → **must have** exactly **one** `job_description_mode`, and **must NOT** have a `contract_term`.
* If `job_description.type = 'PERMANENT'` → **must NOT** have either `contract_term` or `job_description_mode`.

We’ll implement one **constraint trigger** (DEFERRABLE, so you can insert parent/child rows in any order within the same transaction).

```sql
-- =========================
-- TRIGGER FUNCTION
-- =========================
CREATE OR REPLACE FUNCTION check_job_description_parts()
RETURNS TRIGGER AS $$
DECLARE
    t job_description_type;
    c_count INT;
    m_count INT;
BEGIN
    SELECT type INTO t FROM job_description WHERE id = NEW.job_description_id;

    SELECT COUNT(*) INTO c_count FROM contract_term WHERE job_description_id = NEW.job_description_id;
    SELECT COUNT(*) INTO m_count FROM job_description_mode WHERE job_description_id = NEW.job_description_id;

    IF t = 'CONTRACT' THEN
        IF c_count <> 1 OR m_count <> 0 THEN
            RAISE EXCEPTION 'For CONTRACT job_description_id=%: need exactly 1 contract_term and 0 work_mode rows (found: % contract_term, % mode).',
                NEW.job_description_id, c_count, m_count;
        END IF;
    ELSIF t = 'WORK_MODE' THEN
        IF m_count <> 1 OR c_count <> 0 THEN
            RAISE EXCEPTION 'For WORK_MODE job_description_id=%: need exactly 1 work_mode and 0 contract_term rows (found: % mode, % contract_term).',
                NEW.job_description_id, m_count, c_count;
        END IF;
    ELSIF t = 'PERMANENT' THEN
        IF c_count <> 0 OR m_count <> 0 THEN
            RAISE EXCEPTION 'For PERMANENT job_description_id=%: must NOT have contract_term or work_mode rows (found: % contract_term, % mode).',
                NEW.job_description_id, c_count, m_count;
        END IF;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- =========================
-- CONSTRAINT TRIGGERS (DEFERRABLE)
-- =========================

-- Fire the check whenever any of the 3 tables change, but defer to end of transaction
DROP TRIGGER IF EXISTS trg_check_jd_on_jd ON job_description;
DROP TRIGGER IF EXISTS trg_check_jd_on_contract ON contract_term;
DROP TRIGGER IF EXISTS trg_check_jd_on_mode ON job_description_mode;

CREATE CONSTRAINT TRIGGER trg_check_jd_on_jd
AFTER INSERT OR UPDATE ON job_description
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_job_description_parts();

CREATE CONSTRAINT TRIGGER trg_check_jd_on_contract
AFTER INSERT OR UPDATE OR DELETE ON contract_term
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_job_description_parts();

CREATE CONSTRAINT TRIGGER trg_check_jd_on_mode
AFTER INSERT OR UPDATE OR DELETE ON job_description_mode
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION check_job_description_parts();
```

> Because these triggers are **DEFERRABLE INITIALLY DEFERRED**, you can insert the `job_description` first and the matching child row(s) in the same transaction, and the check will only run **at commit time**.

---

## 3) Sample data (INSERTs)

This creates:

* 1 **Society**
* 3 **JobDescriptions**:

  * **Permanent** (no duration, no mode)
  * **Contract** (with duration 1 year 6 months)
  * **Work-mode** (FULL\_TIME)
* 3 **Jobs** using those descriptions
* 2 **Candidates** and 3 **Applications**

```sql
BEGIN;

-- 1) Society
INSERT INTO society (id, name, url, logo)
VALUES
  (1, 'Acme Corp', 'https://acme.example.com', 'https://cdn.acme.example.com/logo.png');

-- 2) JobDescriptions
-- 2.1) Permanent
INSERT INTO job_description (id, type, details)
VALUES
  (1, 'PERMANENT', 'Senior role with long-term growth and benefits.');

-- 2.2) Contract
INSERT INTO job_description (id, type, details)
VALUES
  (2, 'CONTRACT', '6 to 18 month contract for project-based work.');

-- 2.3) Work-mode (full-time or part-time only)
INSERT INTO job_description (id, type, details)
VALUES
  (3, 'WORK_MODE', 'Flexible position with work mode specified.');

-- 3) Child tables for JobDescriptions
-- For CONTRACT (id=2) → contract_term required
INSERT INTO contract_term (job_description_id, duration_years, duration_months, duration_days)
VALUES
  (2, 1, 6, 0);  -- 1 year 6 months

-- For WORK_MODE (id=3) → mode required
INSERT INTO job_description_mode (job_description_id, mode)
VALUES
  (3, 'FULL_TIME');

-- 4) Jobs
INSERT INTO job (id, title, requirements, society_id, job_description_id, created_at)
VALUES
  (1, 'Senior Backend Engineer', '5+ years in Go/Java. Microservices, Kafka.', 1, 1, NOW()),  -- PERMANENT
  (2, 'Project Contract Engineer', 'Microservices project work', 1, 2, NOW()),              -- CONTRACT
  (3, 'Support Engineer (Flexible)', 'System support. Choose your mode.', 1, 3, NOW());      -- WORK_MODE

-- 5) Candidates
INSERT INTO candidate (id, name, email, phone, cv_url, address, other_details)
VALUES
  (1, 'Alice Smith', 'alice@example.com', '+1-202-555-0100', 'https://files.example.com/cv/alice.pdf', '123 Main St, City', '{"github":"https://github.com/alice"}'),
  (2, 'Bob Lee', 'bob@example.com', '+1-202-555-0199', 'https://files.example.com/cv/bob.pdf', '456 Second St, Town', '{"linkedin":"https://linkedin.com/in/bob"}');

-- 6) Applications
INSERT INTO application (id, job_id, candidate_id, applied_at, status)
VALUES
  (1, 1, 1, NOW(), 'PENDING'),   -- Alice -> Senior Backend Engineer
  (2, 2, 1, NOW(), 'REVIEWED'),  -- Alice -> Contract Engineer
  (3, 3, 2, NOW(), 'PENDING');   -- Bob   -> Support Engineer

COMMIT;
```

---