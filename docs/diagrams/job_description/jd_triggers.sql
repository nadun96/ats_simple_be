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
