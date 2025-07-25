
CREATE OR REPLACE FUNCTION copy_workflow_from_template(_job_id BIGINT, _template_id BIGINT)
RETURNS void AS $$
BEGIN
    -- If the job already has stages, do nothing (avoid duplicates).
    IF EXISTS (SELECT 1 FROM job_workflow jw WHERE jw.job_id = _job_id) THEN
        RETURN;
    END IF;

    INSERT INTO job_workflow (job_id, stage_order, stage_name)
    SELECT _job_id, wst.order_index, wst.stage_name
    FROM workflow_stage_template wst
    WHERE wst.template_id = _template_id
    ORDER BY wst.order_index;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION trg_job_copy_template_fn()
RETURNS TRIGGER AS $$
BEGIN
    -- On INSERT: if a template is set, copy it.
    IF TG_OP = 'INSERT' THEN
        IF NEW.workflow_template_id IS NOT NULL THEN
            PERFORM copy_workflow_from_template(NEW.id, NEW.workflow_template_id);
        END IF;
        RETURN NEW;
    END IF;

    -- On UPDATE: if workflow_template_id changed from NULL to some value,
    -- and the job has no stages yet, copy it.
    IF TG_OP = 'UPDATE' THEN
        IF (OLD.workflow_template_id IS DISTINCT FROM NEW.workflow_template_id)
           AND NEW.workflow_template_id IS NOT NULL THEN
            PERFORM copy_workflow_from_template(NEW.id, NEW.workflow_template_id);
        END IF;
        RETURN NEW;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_job_copy_template_ins ON job;
CREATE TRIGGER trg_job_copy_template_ins
AFTER INSERT ON job
FOR EACH ROW
EXECUTE FUNCTION trg_job_copy_template_fn();

DROP TRIGGER IF EXISTS trg_job_copy_template_upd ON job;
CREATE TRIGGER trg_job_copy_template_upd
AFTER UPDATE OF workflow_template_id ON job
FOR EACH ROW
EXECUTE FUNCTION trg_job_copy_template_fn();


CREATE OR REPLACE FUNCTION trg_stage_notification_enqueue_fn()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO celery_task_queue (notification_id, status, scheduled_at)
        VALUES (NEW.id, 'PENDING', NEW.send_time);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        -- If send_time changed, update scheduled time for still-pending tasks
        IF NEW.send_time IS DISTINCT FROM OLD.send_time THEN
            UPDATE celery_task_queue
            SET scheduled_at = NEW.send_time
            WHERE notification_id = NEW.id
              AND status = 'PENDING';
        END IF;
        RETURN NEW;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_stage_notification_enqueue_ins ON stage_notification;
CREATE TRIGGER trg_stage_notification_enqueue_ins
AFTER INSERT ON stage_notification
FOR EACH ROW
EXECUTE FUNCTION trg_stage_notification_enqueue_fn();

DROP TRIGGER IF EXISTS trg_stage_notification_enqueue_upd ON stage_notification;
CREATE TRIGGER trg_stage_notification_enqueue_upd
AFTER UPDATE OF send_time ON stage_notification
FOR EACH ROW
EXECUTE FUNCTION trg_stage_notification_enqueue_fn();


CREATE OR REPLACE FUNCTION trg_stage_notification_validate_fn()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.send_time <= NOW() THEN
        RAISE EXCEPTION 'send_time (%) must be in the future', NEW.send_time;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_stage_notification_validate ON stage_notification;
CREATE TRIGGER trg_stage_notification_validate
BEFORE INSERT OR UPDATE ON stage_notification
FOR EACH ROW
EXECUTE FUNCTION trg_stage_notification_validate_fn();


CREATE OR REPLACE FUNCTION trg_celery_status_guard_fn()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        IF OLD.status = 'SENT' AND NEW.status <> 'SENT' THEN
            RAISE EXCEPTION 'Cannot change status from SENT to %', NEW.status;
        END IF;

        IF OLD.status <> 'PENDING' AND NEW.status = 'PENDING' THEN
            RAISE EXCEPTION 'Cannot revert status back to PENDING from %', OLD.status;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_celery_status_guard ON celery_task_queue;
CREATE TRIGGER trg_celery_status_guard
BEFORE UPDATE ON celery_task_queue
FOR EACH ROW
EXECUTE FUNCTION trg_celery_status_guard_fn();

