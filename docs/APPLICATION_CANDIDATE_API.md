# Application & Candidate Management API Documentation

This document describes the enhanced Application and Candidate management endpoints for the ATS (Application Tracking System).

## Overview

The enhanced ATS system provides comprehensive candidate and application management with workflow processing, form handling, and automated actions.

### Key Features

- **Enhanced Candidate Profiles**: Detailed candidate information with skills, experience, education
- **Workflow Processing**: Automated application processing through defined stages
- **Form Answers**: Custom job application forms with file upload support
- **Stage Actions**: Automated emails, notifications, and tasks on stage transitions
- **Audit Trail**: Complete history of application stage movements
- **File Handling**: Support for resume/CV uploads and form file attachments

## Models

### Candidate Model (Enhanced)

```python
{
    "candidate_id": "integer (auto)",
    "first_name": "string (required)",
    "last_name": "string (required)", 
    "email": "email (required, unique)",
    "phone": "string (optional)",
    "address": "text (optional)",
    "city": "string (optional)",
    "country": "string (optional)",
    "linkedin_url": "url (optional)",
    "portfolio_url": "url (optional)",
    "resume_file_path": "file (optional)",
    "cover_letter": "text (optional)",
    "parsed_cv_data": "json (optional)",
    "skills": "json array (optional)",
    "experience_years": "integer (optional)",
    "education": "json array (optional)",
    "work_experience": "json array (optional)",
    "certifications": "json array (optional)",
    "languages": "json array (optional)",
    "created_at": "datetime (auto)",
    "updated_at": "datetime (auto)"
}
```

### Application Model (Enhanced)

```python
{
    "application_id": "integer (auto)",
    "job": "foreign_key (required)",
    "candidate": "foreign_key (required)",
    "current_stage": "foreign_key to WorkflowStep (optional)",
    "status": "choice field",
    "stage_order": "integer (auto-managed)",
    "form_answers": "json (optional)",
    "notes": "text (optional)",
    "internal_notes": "text (optional)",
    "source": "string (optional)",
    "rating": "integer 1-5 (optional)",
    "tags": "json array (optional)",
    "is_starred": "boolean (default: false)",
    "is_archived": "boolean (default: false)",
    "applied_at": "datetime (auto)",
    "updated_at": "datetime (auto)",
    "processed_at": "datetime (auto on stage change)"
}
```

### Application Stage History

Tracks all stage movements for audit purposes:

```python
{
    "id": "integer (auto)",
    "application": "foreign_key",
    "from_stage": "foreign_key (optional)",
    "to_stage": "foreign_key (required)",
    "changed_by": "string (optional)",
    "notes": "text (optional)",
    "created_at": "datetime (auto)"
}
```

### Application Form Answer

Individual form field answers:

```python
{
    "id": "integer (auto)",
    "application": "foreign_key",
    "field_id": "string",
    "field_name": "string",
    "answer_value": "text (optional)",
    "answer_file": "file (optional)",
    "created_at": "datetime (auto)"
}
```

## API Endpoints

### Candidate Endpoints

#### 1. List/Create Candidates
```
GET  /api/candidates/
POST /api/candidates/
```

**GET Response:**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/candidates/?page=2",
    "previous": null,
    "results": [
        {
            "candidate_id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-0123",
            "address": "123 Main St, Anytown, CA 90210",
            "city": "Anytown",
            "country": "USA",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "portfolio_url": "https://johndoe.dev",
            "resume_file_path": "/media/resumes/john_doe_resume.pdf",
            "cover_letter": "I am very interested...",
            "skills": ["Python", "Django", "React"],
            "experience_years": 5,
            "education": [...],
            "work_experience": [...],
            "certifications": [...],
            "languages": [...],
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

**POST Request:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "address": "123 Main St, Anytown, CA 90210",
    "city": "Anytown",
    "country": "USA",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "portfolio_url": "https://johndoe.dev",
    "cover_letter": "I am very interested in this position...",
    "skills": ["Python", "Django", "React", "PostgreSQL", "AWS"],
    "experience_years": 5,
    "education": [
        {
            "degree": "Bachelor of Science",
            "field": "Computer Science",
            "school": "University of California",
            "year": 2019
        }
    ],
    "work_experience": [
        {
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "duration": "2021-2024",
            "description": "Led development of microservices architecture"
        }
    ],
    "certifications": [
        {
            "name": "AWS Solutions Architect",
            "issuer": "Amazon Web Services",
            "year": 2022
        }
    ],
    "languages": [
        {"language": "English", "level": "Native"},
        {"language": "Spanish", "level": "Intermediate"}
    ]
}
```

#### 2. Candidate Detail
```
GET    /api/candidates/{candidate_id}/
PATCH  /api/candidates/{candidate_id}/
DELETE /api/candidates/{candidate_id}/
```

### Application Endpoints (Enhanced)

#### 1. List/Create Applications
```
GET  /api/v2/applications/
POST /api/v2/applications/
```

**GET Response:**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/v2/applications/?page=2",
    "previous": null,
    "results": [
        {
            "application_id": 1,
            "job": 1,
            "job_title": "Senior Software Engineer",
            "job_company": "Tech Corp",
            "candidate": {
                "candidate_id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                // ... full candidate details
            },
            "current_stage": 2,
            "current_stage_name": "Technical Interview",
            "status": "Interview",
            "stage_order": 2,
            "form_answers": {
                "why_interested": "I'm passionate about building scalable systems...",
                "salary_expectation": "120000",
                "availability": "2 weeks notice"
            },
            "individual_answers": [
                {
                    "id": 1,
                    "field_id": "why_interested",
                    "field_name": "Why are you interested?",
                    "answer_value": "I'm passionate about building scalable systems...",
                    "answer_file": null,
                    "created_at": "2024-01-15T10:30:00Z"
                }
            ],
            "notes": "Strong candidate with relevant experience",
            "internal_notes": "Passed initial screening",
            "source": "LinkedIn",
            "rating": 4,
            "tags": ["senior-level", "full-stack"],
            "is_starred": true,
            "is_archived": false,
            "applied_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T14:30:00Z",
            "processed_at": "2024-01-15T14:30:00Z",
            "stage_history": [
                {
                    "id": 1,
                    "from_stage": null,
                    "from_stage_name": null,
                    "to_stage": 1,
                    "to_stage_name": "Initial Screening",
                    "changed_by": "system",
                    "notes": "Application created",
                    "created_at": "2024-01-15T10:30:00Z"
                }
            ]
        }
    ]
}
```

**POST Request (New Candidate):**
```json
{
    "job": 1,
    "candidate_data": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        // ... full candidate data
    },
    "form_answers": {
        "why_interested": "I'm passionate about building scalable systems...",
        "salary_expectation": "120000",
        "availability": "2 weeks notice",
        "remote_preference": "hybrid"
    },
    "notes": "Strong candidate with relevant experience",
    "source": "LinkedIn",
    "tags": ["senior-level", "full-stack", "experienced"]
}
```

**POST Request (Existing Candidate):**
```json
{
    "job": 1,
    "candidate_id": 5,
    "form_answers": {
        "why_interested": "Looking for new challenges...",
        "salary_expectation": "110000",
        "availability": "immediate"
    },
    "notes": "Referred by current employee",
    "source": "Employee Referral",
    "tags": ["referral", "immediate-start"]
}
```

#### 2. Application Detail
```
GET    /api/v2/applications/{application_id}/
PATCH  /api/v2/applications/{application_id}/
DELETE /api/v2/applications/{application_id}/
```

**PATCH Request:**
```json
{
    "status": "Interview",
    "rating": 4,
    "internal_notes": "Strong technical skills, good communication",
    "is_starred": true,
    "tags": ["high-priority", "technical-strong"]
}
```

#### 3. Advance Application Stage
```
POST /api/v2/applications/{application_id}/advance/
```

Automatically moves application to next workflow stage and triggers associated actions.

**Response:**
```json
{
    "message": "Application advanced successfully",
    "application": {
        // Full application details with updated stage
    }
}
```

#### 4. Move Application to Specific Stage
```
POST /api/v2/applications/{application_id}/move-stage/
```

**Request:**
```json
{
    "stage_id": 3,
    "notes": "Candidate passed initial screening, moving to technical interview"
}
```

**Response:**
```json
{
    "message": "Application moved successfully", 
    "application": {
        // Full application details with updated stage
    }
}
```

## Workflow Processing

### Automatic Actions

When an application moves to a new workflow stage, the system automatically:

1. **Updates Application State**: Sets new current_stage and stage_order
2. **Creates History Record**: Logs the stage transition with timestamp and user
3. **Triggers Stage Actions**: Executes all actions defined for the new stage:
   - **Email Actions**: Send automated emails to candidates/team members
   - **Notification Actions**: Create in-app notifications
   - **Task Actions**: Create tasks for team members (interviews, reviews, etc.)
   - **Meeting Actions**: Schedule meetings/interviews

### Workflow Stage Actions

Each workflow stage can have multiple actions that are triggered when an application reaches that stage:

```json
{
    "action_id": "email_screening_passed",
    "action_name": "Send Screening Passed Email",
    "action_type": "email",
    "action_description": "Notify candidate they passed initial screening",
    "email_template": "screening_passed_template",
    "action_details": {
        "recipients": ["candidate"],
        "cc": ["hiring_manager"],
        "template_vars": {
            "next_step": "Technical Interview",
            "interview_date": "auto_schedule"
        }
    }
}
```

## File Upload Support

### Resume/CV Upload
- Endpoint: `POST /api/candidates/` (multipart/form-data)
- Field: `resume_file_path`
- Supported formats: PDF, DOC, DOCX
- Storage: `/media/resumes/`

### Form File Attachments
- Endpoint: `POST /api/v2/applications/` (multipart/form-data)
- Field: Individual form answers can include file uploads
- Storage: `/media/application_files/`

## Error Responses

All endpoints return detailed error information:

```json
{
    "field_name": ["Error message for this field"],
    "non_field_errors": ["General error messages"]
}
```

## Status Codes

- `200 OK`: Successful GET/PATCH requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Validation errors
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server errors

## Pagination

All list endpoints support pagination:

```
GET /api/candidates/?page=2&page_size=20
```

Parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

## Integration Points

### Email Service Integration
The workflow email actions integrate with the email service (port 8002) to send automated emails.

### Notification Service Integration  
The workflow notification actions integrate with the notification service (port 8003) to create in-app notifications.

### Task Management
Workflow task actions can create tasks for team members with due dates and assignments.

## Example Workflows

### Standard Interview Process
1. **Application Received** → Send acknowledgment email
2. **Initial Screening** → Create screening task for HR
3. **Phone Screen** → Schedule phone interview, send calendar invite
4. **Technical Interview** → Create technical assessment task
5. **Final Interview** → Schedule final interview with hiring manager
6. **Reference Check** → Create reference check task
7. **Offer Made** → Send offer letter
8. **Hired** → Send welcome email, create onboarding tasks
