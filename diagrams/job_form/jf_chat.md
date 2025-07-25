Below is a **normalized PostgreSQL schema (DDL)** for your ER diagram, followed by a **compact sample dataset** (INSERTs) that covers text, single-option, and multi-option questions and their answers.

> I kept the structure faithful to your diagram.
> JSON fields are `jsonb`. If you want *fully* 3NF for multi‑select answers, replace `Answer.option_ids` JSON with a junction table (I can show that variant too).

---

## ✅ PostgreSQL DDL

```sql
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
```

---

## 🧪 Sample data (INSERTs)

This sample creates:

* **1 FormTemplate** (`Software Engineer Application v1`)
* **1 Job** using that template (1–1)
* **4 Questions** (TEXT, SINGLE\_OPTION, MULTIPLE\_OPTIONS, CUSTOM)
* **Options** for SINGLE\_OPTION and MULTIPLE\_OPTIONS questions
* **1 Submission** with **answers** for all questions

```sql
BEGIN;

-- 1) Form Template
INSERT INTO form_template (id, name, version, is_active, created_at)
VALUES
(1, 'Software Engineer Application v1', 1, TRUE, NOW());

-- 2) Job (1:1 with template via UNIQUE constraint)
INSERT INTO job (id, title, description, form_template_id, created_at)
VALUES
(1, 'Software Engineer', 'Work on scalable backend systems.', 1, NOW());

-- 3) Questions
-- Q1: TEXT
INSERT INTO question
(id, template_id, order_index, label, help_text, type, is_required, validation_rules, custom_schema)
VALUES
(1, 1, 1, 'Full Name', 'Enter your legal full name', 'TEXT', TRUE, '{"min_length": 2}'::jsonb, NULL);

-- Q2: SINGLE_OPTION
INSERT INTO question
(id, template_id, order_index, label, help_text, type, is_required, validation_rules, custom_schema)
VALUES
(2, 1, 2, 'Preferred Employment Type', 'Choose one', 'SINGLE_OPTION', TRUE, NULL, NULL);

-- Q3: MULTIPLE_OPTIONS
INSERT INTO question
(id, template_id, order_index, label, help_text, type, is_required, validation_rules, custom_schema)
VALUES
(3, 1, 3, 'Technologies You Use', 'You can select multiple', 'MULTIPLE_OPTIONS', TRUE, NULL, NULL);

-- Q4: CUSTOM
INSERT INTO question
(id, template_id, order_index, label, help_text, type, is_required, validation_rules, custom_schema)
VALUES
(4, 1, 4, 'Portfolio Links', 'Provide any relevant URLs', 'CUSTOM', FALSE, NULL,
 '{"fields":[{"name":"github","type":"url"},{"name":"website","type":"url"}]}'::jsonb);

-- 4) Options (for Q2 and Q3)
-- Q2 options
INSERT INTO question_option (id, question_id, label, value, order_index)
VALUES
(1, 2, 'Full-time', 'FULL_TIME', 1),
(2, 2, 'Part-time', 'PART_TIME', 2),
(3, 2, 'Contract',  'CONTRACT',  3);

-- Q3 options
INSERT INTO question_option (id, question_id, label, value, order_index)
VALUES
(4, 3, 'Python', 'python', 1),
(5, 3, 'Go',     'go',     2),
(6, 3, 'Java',   'java',   3),
(7, 3, 'Rust',   'rust',   4);

-- 5) A Submission
INSERT INTO form_submission (id, job_id, template_id, applicant_id, submitted_at, status)
VALUES
(1, 1, 1, 101, NOW(), 'SUBMITTED');

-- 6) Answers for that submission
-- Q1 (TEXT)
INSERT INTO answer (id, submission_id, question_id, value_text)
VALUES
(1, 1, 1, 'Nadun Udaraka');

-- Q2 (SINGLE_OPTION) -> option_id = 1 (Full-time)
INSERT INTO answer (id, submission_id, question_id, option_id)
VALUES
(2, 1, 2, 1);

-- Q3 (MULTIPLE_OPTIONS) -> option_ids = [4, 5] (Python, Go)
INSERT INTO answer (id, submission_id, question_id, option_ids)
VALUES
(3, 1, 3, '[4,5]'::jsonb);

-- Q4 (CUSTOM) -> value_text stores a JSON string or text blob; you could also extend the schema to store JSON natively
INSERT INTO answer (id, submission_id, question_id, value_text)
VALUES
(4, 1, 4, '{"github":"https://github.com/nadun","website":"https://nadun.dev"}');

COMMIT;
```

---

## 🔧 (Optional) Fully-normalized multi-select answers

If you want to avoid `option_ids JSONB`, create a junction table:

```sql
CREATE TABLE answer_option (
    answer_id   BIGINT NOT NULL REFERENCES answer(id) ON DELETE CASCADE,
    option_id   BIGINT NOT NULL REFERENCES question_option(id) ON DELETE CASCADE,
    PRIMARY KEY (answer_id, option_id)
);
```

Then, for multi-select questions, store one row per selected option in `answer_option` instead of using `answer.option_ids`.

---
Below is a **PostgreSQL trigger setup** to ensure that each **Answer** row has the correct value column populated depending on its **Question type**:

---

# **Trigger Logic**

1. **TEXT / CUSTOM Questions**

   * Must have `value_text` (not NULL).
   * `option_id` and `option_ids` must be NULL.

2. **SINGLE\_OPTION Questions**

   * Must have `option_id` (not NULL).
   * `value_text` and `option_ids` must be NULL.

3. **MULTIPLE\_OPTIONS / MCQ Questions**

   * Must have `option_ids` (JSON array, not NULL or empty).
   * `value_text` and `option_id` must be NULL.

4. **If conditions are not met**, the trigger will raise an error.

---

## **SQL Code**

```sql
-- 1) Create the trigger function
CREATE OR REPLACE FUNCTION check_answer_consistency()
RETURNS TRIGGER AS $$
DECLARE
    qtype question_type;
BEGIN
    -- Get the question type
    SELECT type INTO qtype
    FROM question
    WHERE id = NEW.question_id;

    -- Validate based on type
    IF qtype = 'TEXT' OR qtype = 'CUSTOM' THEN
        IF NEW.value_text IS NULL THEN
            RAISE EXCEPTION 'TEXT/CUSTOM answer must have value_text';
        END IF;
        IF NEW.option_id IS NOT NULL OR NEW.option_ids IS NOT NULL THEN
            RAISE EXCEPTION 'TEXT/CUSTOM answer cannot have option_id or option_ids';
        END IF;

    ELSIF qtype = 'SINGLE_OPTION' THEN
        IF NEW.option_id IS NULL THEN
            RAISE EXCEPTION 'SINGLE_OPTION answer must have option_id';
        END IF;
        IF NEW.value_text IS NOT NULL OR NEW.option_ids IS NOT NULL THEN
            RAISE EXCEPTION 'SINGLE_OPTION answer cannot have value_text or option_ids';
        END IF;

    ELSIF qtype = 'MULTIPLE_OPTIONS' OR qtype = 'MCQ' THEN
        IF NEW.option_ids IS NULL OR jsonb_array_length(NEW.option_ids) = 0 THEN
            RAISE EXCEPTION 'MULTIPLE_OPTIONS/MCQ answer must have option_ids array';
        END IF;
        IF NEW.value_text IS NOT NULL OR NEW.option_id IS NOT NULL THEN
            RAISE EXCEPTION 'MULTIPLE_OPTIONS/MCQ answer cannot have value_text or option_id';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2) Attach the trigger to the answer table
DROP TRIGGER IF EXISTS trg_check_answer_consistency ON answer;

CREATE TRIGGER trg_check_answer_consistency
BEFORE INSERT OR UPDATE ON answer
FOR EACH ROW
EXECUTE FUNCTION check_answer_consistency();
```

---

# **How it Works**

* Any `INSERT` or `UPDATE` on `answer` will check the associated `question.type`.
* If data doesn't match the expected pattern, a `RAISE EXCEPTION` stops the operation.

---

## **Test Example**

```sql
-- This will fail because SINGLE_OPTION requires option_id, not value_text
INSERT INTO answer (submission_id, question_id, value_text)
VALUES (1, 2, 'Full-time');

-- This will succeed
INSERT INTO answer (submission_id, question_id, option_id)
VALUES (1, 2, 1);
```

---
