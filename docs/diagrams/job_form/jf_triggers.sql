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


DROP TRIGGER IF EXISTS trg_check_answer_consistency ON answer;

CREATE TRIGGER trg_check_answer_consistency
BEFORE INSERT OR UPDATE ON answer
FOR EACH ROW
EXECUTE FUNCTION check_answer_consistency();