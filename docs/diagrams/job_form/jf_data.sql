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
