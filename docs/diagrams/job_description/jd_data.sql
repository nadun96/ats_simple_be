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
