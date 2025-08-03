# ATS Application Service - API Documentation

## Overview
The ATS (Applicant Tracking System) Application Service is a Django-based microservice that provides comprehensive job management functionality. It handles complete job postings with metadata, workflow management, team assignments, and form configurations.

## Features Implemented ✅

### 🔥 Main Features
- **Complete Job Creation**: Single endpoint to create jobs with all nested metadata
- **Full CRUD Operations**: Create, Read, Update, Delete for all entities
- **Pagination Support**: All list endpoints support pagination
- **Microservice Architecture**: Dockerized for easy deployment
- **Database Schema**: PostgreSQL with comprehensive data models

### 📊 Data Models Created
1. **Society** - Company/Organization information
2. **Job** - Main job entity with comprehensive fields
3. **JobForm** - Application form structure
4. **FormField** - Individual form fields
5. **Team** - Team assigned to job
6. **TeamMember** - Individual team members
7. **WorkflowTemplate** - Workflow definitions
8. **WorkflowStep** - Individual workflow steps
9. **WorkflowAction** - Actions within steps
10. **WorkflowTask** - Tasks with assignments
11. **TaskComment** - Comments on tasks
12. **StepLink** - Links within workflow steps
13. **JobSite** - Sites where jobs are posted

## API Endpoints

### Base URL
```
http://localhost:8001/api/v1/
```

### 🔥 Main Job Endpoints

#### Create Complete Job (Primary Feature)
```http
POST /jobs/complete/
Content-Type: application/json

{
  "job": {
    "description": {
      "society": {
        "name": "XYZ Corporation",
        "type": "Company",
        "industry": "Technology",
        // ... full society data
      },
      "job description": {
        "urgency": "High",
        "title": "Software Engineer",
        "remoteStatus": {
          "isRemote": true,
          "type": "Hybrid"
        },
        // ... complete job description
      },
      "settings": {
        "isActive": true,
        "isPublic": true
        // ... job settings
      },
      "tag": {
        "tags": ["Software Development", "Engineering"]
      }
    },
    "JobForm": {
      "templateName": "Job Application Form",
      "formFields": [
        {
          "fieldType": "text",
          "fieldName": "Full Name",
          "isRequired": true
          // ... form field config
        }
      ]
    },
    "Team": {
      "teamName": "Engineering Team",
      "members": [
        {
          "name": "John Doe",
          "role": "Lead Software Engineer"
          // ... team member data
        }
      ]
    },
    "WorkFlow": {
      "template": {
        "name": "Job Application Workflow",
        "steps": [
          {
            "stepName": "Application Received",
            "actions": [...],
            "tasks": [...],
            "links": [...]
          }
        ]
      }
    },
    "sites": [
      {
        "siteName": "XYZ Corporation Careers",
        "siteUrl": "https://xyzcorporation.com/careers"
        // ... site information
      }
    ]
  }
}
```

#### Standard Job CRUD
```http
GET    /jobs/              # List all jobs (paginated)
POST   /jobs/              # Create simple job
GET    /jobs/{id}/         # Get job by ID
PATCH  /jobs/{id}/         # Update job
DELETE /jobs/{id}/         # Delete job
```

### 🏢 Society Endpoints
```http
GET    /societies/         # List all societies
POST   /societies/         # Create society
GET    /societies/{id}/    # Get society by ID
PATCH  /societies/{id}/    # Update society
DELETE /societies/{id}/    # Delete society
```

### 📝 Form Management
```http
# Job Forms
GET    /job-forms/         # List all job forms
POST   /job-forms/         # Create job form
GET    /job-forms/{id}/    # Get job form by ID
PATCH  /job-forms/{id}/    # Update job form
DELETE /job-forms/{id}/    # Delete job form

# Form Fields
GET    /form-fields/       # List all form fields
POST   /form-fields/       # Create form field
GET    /form-fields/{id}/  # Get form field by ID
PATCH  /form-fields/{id}/  # Update form field
DELETE /form-fields/{id}/  # Delete form field
```

### 👥 Team Management
```http
# Teams
GET    /teams/             # List all teams
POST   /teams/             # Create team
GET    /teams/{id}/        # Get team by ID
PATCH  /teams/{id}/        # Update team
DELETE /teams/{id}/        # Delete team

# Team Members
GET    /team-members/      # List all team members
POST   /team-members/      # Create team member
GET    /team-members/{id}/ # Get team member by ID
PATCH  /team-members/{id}/ # Update team member
DELETE /team-members/{id}/ # Delete team member
```

### 🔄 Workflow Management
```http
# Workflow Templates
GET    /workflow-templates/     # List all workflow templates
POST   /workflow-templates/     # Create workflow template
GET    /workflow-templates/{id}/ # Get workflow template by ID
PATCH  /workflow-templates/{id}/ # Update workflow template
DELETE /workflow-templates/{id}/ # Delete workflow template

# Workflow Steps
GET    /workflow-steps/         # List all workflow steps
POST   /workflow-steps/         # Create workflow step
GET    /workflow-steps/{id}/    # Get workflow step by ID
PATCH  /workflow-steps/{id}/    # Update workflow step
DELETE /workflow-steps/{id}/    # Delete workflow step

# Workflow Actions
GET    /workflow-actions/       # List all workflow actions
POST   /workflow-actions/       # Create workflow action
GET    /workflow-actions/{id}/  # Get workflow action by ID
PATCH  /workflow-actions/{id}/  # Update workflow action
DELETE /workflow-actions/{id}/  # Delete workflow action

# Workflow Tasks
GET    /workflow-tasks/         # List all workflow tasks
POST   /workflow-tasks/         # Create workflow task
GET    /workflow-tasks/{id}/    # Get workflow task by ID
PATCH  /workflow-tasks/{id}/    # Update workflow task
DELETE /workflow-tasks/{id}/    # Delete workflow task

# Task Comments
GET    /task-comments/          # List all task comments
POST   /task-comments/          # Create task comment
GET    /task-comments/{id}/     # Get task comment by ID
PATCH  /task-comments/{id}/     # Update task comment
DELETE /task-comments/{id}/     # Delete task comment

# Step Links
GET    /step-links/             # List all step links
POST   /step-links/             # Create step link
GET    /step-links/{id}/        # Get step link by ID
PATCH  /step-links/{id}/        # Update step link
DELETE /step-links/{id}/        # Delete step link
```

### 🌐 Job Site Management
```http
GET    /job-sites/         # List all job sites
POST   /job-sites/         # Create job site
GET    /job-sites/{id}/    # Get job site by ID
PATCH  /job-sites/{id}/    # Update job site
DELETE /job-sites/{id}/    # Delete job site
```

## Response Format

### Success Response
```json
{
  "id": 1,
  "title": "Software Engineer",
  "urgency": "High",
  "society": {
    "id": 1,
    "name": "XYZ Corporation",
    "industry": "Technology"
  },
  "created_at": "2025-08-03T10:30:00Z",
  "updated_at": "2025-08-03T10:30:00Z"
  // ... other fields
}
```

### Error Response
```json
{
  "error": "Validation failed",
  "details": {
    "title": ["This field is required."]
  }
}
```

### Paginated Response
```json
{
  "count": 25,
  "next": "http://localhost:8001/api/v1/jobs/?page=2",
  "previous": null,
  "results": [
    // ... job objects
  ]
}
```

## Docker Deployment

### Starting the Service
```bash
# Start PostgreSQL database
docker-compose up postgres -d

# Build and start application service
docker-compose up application_service -d

# Run migrations (if needed)
docker-compose run --rm application_service python manage.py migrate
```

### Environment Variables
```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=ats_db
DATABASE_USER=ats_user
DATABASE_PASSWORD=ats_password
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

## Key Features

### 🎯 All Fields Optional
Every field in all models is optional (`blank=True, null=True`), allowing flexible data entry.

### 🔄 Complete Workflow Support
- Multi-step workflows with actions
- Task assignments with comments
- Link management for resources
- Team-based task distribution

### 📊 Comprehensive Data Model
- Society/Company information
- Detailed job descriptions with salary ranges
- Contract duration and remote work settings
- Benefits, qualifications, and responsibilities
- Application deadlines and links

### 🚀 Microservice Ready
- Dockerized deployment
- PostgreSQL database
- Health check endpoints
- CORS enabled for frontend integration

## Testing

Run the comprehensive test suite:
```bash
python test_endpoints.py
```

The test covers:
- ✅ Complete job creation with all metadata
- ✅ CRUD operations for all entities
- ✅ Pagination functionality
- ✅ Data relationships and integrity
- ✅ Error handling

## API Documentation

Access interactive API documentation:
- Swagger UI: http://localhost:8001/swagger/
- ReDoc: http://localhost:8001/redoc/

## Usage Examples

### Create a Simple Job
```python
import requests

job_data = {
    "title": "Python Developer",
    "urgency": "Medium",
    "country": "USA",
    "city": "New York",
    "department": "Technology",
    "type_of_contract": "Full-time"
}

response = requests.post(
    "http://localhost:8001/api/v1/jobs/", 
    json=job_data
)
```

### Get All Jobs with Pagination
```python
response = requests.get(
    "http://localhost:8001/api/v1/jobs/?page=1&page_size=10"
)
```

### Update a Job
```python
update_data = {"title": "Senior Python Developer"}
response = requests.patch(
    "http://localhost:8001/api/v1/jobs/1/", 
    json=update_data
)
```

## Status
✅ **PRODUCTION READY**
- All endpoints tested and working
- Database migrations applied
- Docker deployment configured
- Comprehensive data model implemented
- Frontend integration ready

The microservice is now ready to accept job postings from the frontend and handle all job-related operations with full metadata support.
