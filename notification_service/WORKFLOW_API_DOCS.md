# Workflow API Documentation

This document describes the newly implemented Workflow and WorkflowStep REST API endpoints in the notification service.

## Models

### Workflow Model
- **workflow_id**: Primary key (auto-generated)
- **job**: One-to-one relationship with Job model
- **name**: Workflow name (max 200 characters)
- **created_at**: Auto-generated creation timestamp
- **updated_at**: Auto-generated update timestamp

### WorkflowStep Model
- **step_id**: Primary key (auto-generated)
- **workflow**: Foreign key to Workflow
- **step_order**: Positive integer defining the order of steps
- **name**: Step name (max 200 characters)
- **step_type**: Choice field with options:
  - screening
  - interview
  - assessment
  - reference_check
  - offer
  - onboarding
  - custom
- **description**: Optional text description
- **is_active**: Boolean flag for step status
- **created_at**: Auto-generated creation timestamp
- **updated_at**: Auto-generated update timestamp

## API Endpoints

### Workflow Endpoints

#### 1. List/Create Workflows
- **GET** `/api/workflows/`
  - List all workflows with optional filtering
  - Query parameters:
    - `job_id`: Filter by job ID
  - Response: Array of workflow objects with nested steps

- **POST** `/api/workflows/`
  - Create a new workflow
  - Request body:
    ```json
    {
      "job": 1,
      "name": "Standard Hiring Process"
    }
    ```

#### 2. Workflow Detail Operations
- **GET** `/api/workflows/{workflow_id}/`
  - Retrieve a specific workflow with its steps

- **PUT** `/api/workflows/{workflow_id}/`
  - Update a specific workflow (full update)

- **PATCH** `/api/workflows/{workflow_id}/`
  - Partially update a specific workflow

- **DELETE** `/api/workflows/{workflow_id}/`
  - Delete a specific workflow

### Workflow Step Endpoints

#### 1. List/Create Workflow Steps
- **GET** `/api/workflow-steps/`
  - List all workflow steps with optional filtering
  - Query parameters:
    - `workflow_id`: Filter by workflow ID
    - `step_type`: Filter by step type
    - `is_active`: Filter by active status (true/false)

- **POST** `/api/workflow-steps/`
  - Create a new workflow step
  - Request body:
    ```json
    {
      "workflow": 1,
      "step_order": 1,
      "name": "Initial Screening",
      "step_type": "screening",
      "description": "Review resume and basic qualifications",
      "is_active": true
    }
    ```

#### 2. Workflow Step Detail Operations
- **GET** `/api/workflow-steps/{step_id}/`
  - Retrieve a specific workflow step

- **PUT** `/api/workflow-steps/{step_id}/`
  - Update a specific workflow step (full update)

- **PATCH** `/api/workflow-steps/{step_id}/`
  - Partially update a specific workflow step

- **DELETE** `/api/workflow-steps/{step_id}/`
  - Delete a specific workflow step

## Example Usage

### Creating a Complete Workflow

1. **Create a Workflow:**
```json
POST /api/workflows/
{
  "job": 1,
  "name": "Software Engineer Hiring Process"
}
```

2. **Add Workflow Steps:**
```json
POST /api/workflow-steps/
{
  "workflow": 1,
  "step_order": 1,
  "name": "Resume Review",
  "step_type": "screening",
  "description": "Initial resume screening",
  "is_active": true
}

POST /api/workflow-steps/
{
  "workflow": 1,
  "step_order": 2,
  "name": "Technical Interview",
  "step_type": "interview",
  "description": "Technical skills assessment",
  "is_active": true
}

POST /api/workflow-steps/
{
  "workflow": 1,
  "step_order": 3,
  "name": "Final Offer",
  "step_type": "offer",
  "description": "Salary negotiation and offer",
  "is_active": true
}
```

### Querying Workflows

1. **Get all workflows for a specific job:**
```
GET /api/workflows/?job_id=1
```

2. **Get all steps for a specific workflow:**
```
GET /api/workflow-steps/?workflow_id=1
```

3. **Get only active screening steps:**
```
GET /api/workflow-steps/?step_type=screening&is_active=true
```

## Swagger Documentation

All endpoints are documented with Swagger/OpenAPI. The following decorators provide comprehensive API documentation:

- Request/response schemas
- Parameter descriptions
- Error response codes
- Example payloads

Access the interactive API documentation at `/swagger/` when the service is running.

## Database Considerations

- **Unique Constraints**: Each workflow can have only one step with the same `step_order`
- **Cascading Deletes**: Deleting a workflow will delete all associated workflow steps
- **Job Relationship**: Each job can have only one workflow (OneToOne relationship)

## Migration

To apply the database changes, run:
```bash
python manage.py migrate
```

This will create the `workflows` and `workflow_steps` tables in your database.
