BEGIN;

-- ============================
-- 1) WORKFLOW TEMPLATE
-- ============================
INSERT INTO workflow_template (id, name, description, created_at)
VALUES
  (1, 'Standard Hiring Pipeline', 'Default hiring workflow with interviews and offer', NOW());

-- ============================
-- 2) WORKFLOW STAGE TEMPLATES
-- ============================
INSERT INTO workflow_stage_template (id, template_id, order_index, stage_name)
VALUES
  (1,  1,  1, 'New Applicant'),
  (2,  1,  2, 'CV Selected'),
  (3,  1,  3, 'Phone Call'),
  (4,  1,  4, 'Video Call Interview'),
  (5,  1,  5, 'HR Interview'),
  (6,  1,  6, 'Technical Interview'),
  (7,  1,  7, 'Tech Lead Interview'),
  (8,  1,  8, 'Manager Interview'),
  (9,  1,  9, 'Offer Made'),
  (10, 1, 10, 'Hiring');

-- ============================
-- 3) JOB USING THAT TEMPLATE
-- ============================
INSERT INTO job (id, title, description, workflow_template_id, created_at)
VALUES
  (1, 'Senior Backend Engineer', 'Backend role focusing on services and scalability', 1, NOW());

-- ============================
-- 4) JOB WORKFLOW (custom per job)
--    (adds an extra "Coding Challenge" stage)
-- ============================
INSERT INTO job_workflow (id, job_id, stage_order, stage_name)
VALUES
  (1,  1,  1,  'New Applicant'),
  (2,  1,  2,  'CV Selected'),
  (3,  1,  3,  'Phone Call'),
  (4,  1,  4,  'Video Call Interview'),
  (5,  1,  5,  'HR Interview'),
  (6,  1,  6,  'Technical Interview'),
  (7,  1,  7,  'Coding Challenge'),        -- custom addition
  (8,  1,  8,  'Tech Lead Interview'),
  (9,  1,  9,  'Manager Interview'),
  (10, 1, 10, 'Offer Made'),
  (11, 1, 11, 'Hiring');

-- ============================
-- 5) STAGE TASKS
-- ============================
INSERT INTO stage_task (id, job_workflow_id, task_type, description, assignee_role)
VALUES
  (1,  2, 'EVALUATOR_TASK', 'Review candidate CV and shortlist', 'HR'),
  (2,  4, 'EVALUATOR_TASK', 'Prepare video call link', 'HR'),
  (3,  4, 'EVALUATOR_TASK', 'Conduct video interview', 'TECH_LEAD'),
  (4,  6, 'EVALUATOR_TASK', 'Run technical deep-dive', 'ENGINEERING_MANAGER'),
  (5,  7, 'EVALUATOR_TASK', 'Evaluate coding challenge submission', 'TECH_LEAD'),
  (6, 10, 'EVALUATOR_TASK', 'Prepare and send offer letter', 'HR');

-- ============================
-- 6) STAGE NOTIFICATIONS
-- (Emails/SMS to candidate/evaluator)
-- ============================
-- Video Call Interview stage notifications
INSERT INTO stage_notification
(id, job_workflow_id, notification_type, recipient, message_template, send_time)
VALUES
  (1, 4, 'EMAIL', 'CANDIDATE',
     'Dear {{candidate_name}}, your video interview is scheduled. Link: {{video_link}}',
     '2025-07-26 10:00:00+05:30'),
  (2, 4, 'EMAIL', 'EVALUATOR',
     'You have a video interview with {{candidate_name}}. Link: {{video_link}}',
     '2025-07-26 10:00:00+05:30'),
  (3, 4, 'SMS', 'CANDIDATE',
     'Reminder: Your video interview at 10:00. Link: {{video_link}}',
     '2025-07-26 09:30:00+05:30');

-- Offer Made stage notification
INSERT INTO stage_notification
(id, job_workflow_id, notification_type, recipient, message_template, send_time)
VALUES
  (4, 10, 'EMAIL', 'CANDIDATE',
     'Congratulations {{candidate_name}}, we are pleased to make you an offer!',
     '2025-07-30 09:00:00+05:30');

-- ============================
-- 7) CELERY TASK QUEUE (scheduled sends)
-- ============================
INSERT INTO celery_task_queue (id, notification_id, status, scheduled_at, sent_at)
VALUES
  (1, 1, 'PENDING', '2025-07-26 10:00:00+05:30', NULL),
  (2, 2, 'PENDING', '2025-07-26 10:00:00+05:30', NULL),
  (3, 3, 'PENDING', '2025-07-26 09:30:00+05:30', NULL),
  (4, 4, 'PENDING', '2025-07-30 09:00:00+05:30', NULL);

COMMIT;
