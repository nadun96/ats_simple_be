CREATE OR REPLACE VIEW vw_job_details AS
SELECT
    j.id AS job_id,
    j.title AS job_title,
    j.requirements AS job_requirements,
    j.created_at AS job_created_at,

    -- Society info
    s.id AS society_id,
    s.name AS society_name,
    s.url AS society_url,
    s.logo AS society_logo,

    -- Job description
    jd.id AS job_description_id,
    jd.type AS job_type,
    jd.details AS job_details,

    -- Contract term (if applicable)
    ct.duration_years,
    ct.duration_months,
    ct.duration_days,

    -- Work mode (if applicable)
    jm.mode AS work_mode,

    -- A combined "description" column for convenience
    CASE
        WHEN jd.type = 'CONTRACT' THEN
            CONCAT('Contract for ', 
                   COALESCE(ct.duration_years, 0), ' years, ',
                   COALESCE(ct.duration_months, 0), ' months, ',
                   COALESCE(ct.duration_days, 0), ' days')
        WHEN jd.type = 'WORK_MODE' THEN
            CONCAT('Work mode: ', jm.mode)
        ELSE
            'Permanent Position'
    END AS job_summary

FROM job j
JOIN society s ON j.society_id = s.id
JOIN job_description jd ON j.job_description_id = jd.id
LEFT JOIN contract_term ct ON jd.id = ct.job_description_id
LEFT JOIN job_description_mode jm ON jd.id = jm.job_description_id;
