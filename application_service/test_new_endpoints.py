#!/usr/bin/env python3
"""
Test script for the new Application and Candidate endpoints
This script demonstrates the structure and usage of the enhanced ATS system
"""

import json

# Sample data structures for testing the new API endpoints

# Sample candidate data with enhanced fields
sample_candidate_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "address": "123 Main St, Anytown, CA 90210",
    "city": "Anytown",
    "country": "USA",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "portfolio_url": "https://johndoe.dev",
    "cover_letter": "I am very interested in this position and believe my skills align well with your requirements.",
    "skills": ["Python", "Django", "React", "PostgreSQL", "AWS"],
    "experience_years": 5,
    "education": [
        {
            "degree": "Bachelor of Science",
            "field": "Computer Science",
            "school": "University of California",
            "year": 2019,
        }
    ],
    "work_experience": [
        {
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "duration": "2021-2024",
            "description": "Led development of microservices architecture",
        },
        {
            "title": "Software Engineer",
            "company": "StartupXYZ",
            "duration": "2019-2021",
            "description": "Full-stack development using Django and React",
        },
    ],
    "certifications": [
        {
            "name": "AWS Solutions Architect",
            "issuer": "Amazon Web Services",
            "year": 2022,
        }
    ],
    "languages": [
        {"language": "English", "level": "Native"},
        {"language": "Spanish", "level": "Intermediate"},
    ],
}

# Sample application data with form answers
sample_application_data = {
    "job": 1,  # Job ID
    "candidate_data": sample_candidate_data,
    "form_answers": {
        "why_interested": "I'm passionate about building scalable systems and your company's mission aligns with my values.",
        "salary_expectation": "120000",
        "availability": "2 weeks notice",
        "remote_preference": "hybrid",
        "years_experience": "5",
        "portfolio_projects": "Built a microservices platform handling 1M+ requests/day",
    },
    "notes": "Strong candidate with relevant experience",
    "source": "LinkedIn",
    "tags": ["senior-level", "full-stack", "experienced"],
}

# Sample application data using existing candidate
sample_application_existing_candidate = {
    "job": 1,  # Job ID
    "candidate_id": 1,  # Existing candidate ID
    "form_answers": {
        "why_interested": "Looking for new challenges in a growth-oriented company",
        "salary_expectation": "110000",
        "availability": "immediate",
        "remote_preference": "full-remote",
    },
    "notes": "Referred by current employee",
    "source": "Employee Referral",
    "tags": ["referral", "immediate-start"],
}

# Sample data for moving application to different stage
sample_stage_move_data = {
    "stage_id": 2,  # Target workflow stage ID
    "notes": "Candidate passed initial screening, moving to technical interview",
}

# Sample application update data
sample_application_update = {
    "status": "Interview",
    "rating": 4,
    "internal_notes": "Strong technical skills, good communication",
    "is_starred": True,
    "tags": ["high-priority", "technical-strong"],
}


def print_endpoint_examples():
    """Print examples of how to use the new endpoints"""

    print("=== NEW APPLICATION & CANDIDATE ENDPOINTS ===\n")

    print("1. CREATE CANDIDATE")
    print("POST /api/candidates/")
    print("Content-Type: application/json")
    print(json.dumps(sample_candidate_data, indent=2))
    print("\n" + "=" * 50 + "\n")

    print("2. GET ALL CANDIDATES")
    print("GET /api/candidates/")
    print("Response: List of candidates with pagination")
    print("\n" + "=" * 50 + "\n")

    print("3. GET CANDIDATE BY ID")
    print("GET /api/candidates/{candidate_id}/")
    print("Response: Detailed candidate information")
    print("\n" + "=" * 50 + "\n")

    print("4. CREATE APPLICATION WITH NEW CANDIDATE")
    print("POST /api/v2/applications/")
    print("Content-Type: application/json")
    print(json.dumps(sample_application_data, indent=2))
    print("\n" + "=" * 50 + "\n")

    print("5. CREATE APPLICATION WITH EXISTING CANDIDATE")
    print("POST /api/v2/applications/")
    print("Content-Type: application/json")
    print(json.dumps(sample_application_existing_candidate, indent=2))
    print("\n" + "=" * 50 + "\n")

    print("6. GET ALL APPLICATIONS (Enhanced)")
    print("GET /api/v2/applications/")
    print("Response: Detailed applications with candidate info, stage history, etc.")
    print("\n" + "=" * 50 + "\n")

    print("7. GET APPLICATION BY ID")
    print("GET /api/v2/applications/{application_id}/")
    print("Response: Full application details with workflow information")
    print("\n" + "=" * 50 + "\n")

    print("8. UPDATE APPLICATION")
    print("PATCH /api/v2/applications/{application_id}/")
    print("Content-Type: application/json")
    print(json.dumps(sample_application_update, indent=2))
    print("\n" + "=" * 50 + "\n")

    print("9. ADVANCE APPLICATION TO NEXT STAGE")
    print("POST /api/v2/applications/{application_id}/advance/")
    print("This automatically moves the application to the next workflow stage")
    print("and triggers associated actions (emails, notifications, tasks)")
    print("\n" + "=" * 50 + "\n")

    print("10. MOVE APPLICATION TO SPECIFIC STAGE")
    print("POST /api/v2/applications/{application_id}/move-stage/")
    print("Content-Type: application/json")
    print(json.dumps(sample_stage_move_data, indent=2))
    print("\n" + "=" * 50 + "\n")


def print_workflow_explanation():
    """Explain the workflow processing system"""

    print("=== WORKFLOW PROCESSING SYSTEM ===\n")

    print("APPLICATION WORKFLOW FEATURES:")
    print("1. Each job can have a workflow template with ordered stages")
    print("2. Applications automatically start at the first workflow stage")
    print("3. Each stage can have multiple actions (email, notification, task)")
    print("4. When application moves to a stage, actions are triggered")
    print("5. Stage history is tracked for audit purposes")
    print("6. Applications can be moved forward/backward in workflow")
    print("\nWORKFLOW STAGE ACTIONS:")
    print("- Email: Send automated emails to candidates/team members")
    print("- Notification: Create in-app notifications")
    print("- Task: Create tasks for team members (interviews, reviews, etc.)")
    print("- Meeting: Schedule meetings/interviews")
    print("\nFORM ANSWERS:")
    print("- Job applications can include custom form answers")
    print("- Answers are stored both as JSON and individual records")
    print("- File uploads supported for forms")
    print("- Form structure defined by job form fields")
    print("\nCANDIDATE FEATURES:")
    print("- Enhanced candidate profiles with skills, experience, education")
    print("- CV/Resume upload support")
    print("- Parsed CV data storage")
    print("- Multiple contact methods and portfolio links")
    print("- Certification and language tracking")
    print("\n" + "=" * 50 + "\n")


def print_data_model_overview():
    """Print overview of the data model relationships"""

    print("=== DATA MODEL RELATIONSHIPS ===\n")

    print("CORE ENTITIES:")
    print("├── Job")
    print("│   ├── JobForm (1:1) - Custom application form")
    print("│   │   └── FormFields (1:Many) - Individual form questions")
    print("│   ├── WorkflowTemplate (1:1) - Application processing workflow")
    print("│   │   └── WorkflowSteps (1:Many) - Ordered stages")
    print("│   │       └── WorkflowActions (1:Many) - Stage actions")
    print("│   └── Applications (1:Many)")
    print("│")
    print("├── Candidate")
    print("│   ├── Enhanced personal information")
    print("│   ├── Skills, experience, education")
    print("│   ├── Resume/CV file upload")
    print("│   └── Applications (1:Many)")
    print("│")
    print("└── Application")
    print("    ├── Job (Many:1)")
    print("    ├── Candidate (Many:1)")
    print("    ├── Current workflow stage")
    print("    ├── Form answers (JSON + individual records)")
    print("    ├── ApplicationStageHistory (1:Many) - Audit trail")
    print("    └── ApplicationFormAnswers (1:Many) - Individual answers")
    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    print("ATS SYSTEM - APPLICATION & CANDIDATE ENDPOINTS DOCUMENTATION")
    print("=" * 60)
    print()

    print_data_model_overview()
    print_workflow_explanation()
    print_endpoint_examples()

    print("NOTES:")
    print("- All endpoints support pagination")
    print("- File uploads supported via multipart/form-data")
    print("- Detailed error responses with field-level validation")
    print("- Workflow actions are triggered automatically on stage changes")
    print("- Complete audit trail maintained for application processing")
