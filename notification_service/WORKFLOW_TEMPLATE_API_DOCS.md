# Workflow Template API Documentation

This document describes the newly implemented WorkflowTemplate and WorkflowStageTemplate REST API endpoints in the notification service. These templates allow you to create reusable workflow patterns that can be applied to multiple jobs.

## Models

### WorkflowTemplate Model
- **id**: Primary key (auto-generated)
- **name**: Template name (max 200 characters)
- **description**: Optional description of the template
- **is_active**: Boolean flag for template status
- **created_at**: Auto-generated creation timestamp
- **updated_at**: Auto-generated update timestamp

### WorkflowStageTemplate Model
- **id**: Primary key (auto-generated)
- **template**: Foreign key to WorkflowTemplate
- **order_index**: Positive integer defining the order of stages
- **stage_name**: Stage name (max 200 characters)
- **description**: Optional text description
- **stage_type**: Choice field with options:
  - screening
  - interview
  - assessment
  - reference_check
  - offer
  - onboarding
  - custom
- **is_active**: Boolean flag for stage status
- **created_at**: Auto-generated creation timestamp
- **updated_at**: Auto-generated update timestamp

## API Endpoints

### Workflow Template Endpoints

#### 1. List/Create Workflow Templates
- **GET** `/api/workflow-templates/`
  - List all workflow templates with optional filtering
  - Query parameters:
    - `is_active`: Filter by active status (true/false)
    - `name`: Filter by template name (partial match)
  - Response: Array of template objects with nested stages and stage count

- **POST** `/api/workflow-templates/`
  - Create a new workflow template
  - Request body:
    ```json
    {
      "name": "Standard Software Engineer Process",
      "description": "Complete hiring workflow for software engineering positions",
      "is_active": true
    }
    ```

#### 2. Workflow Template Detail Operations
- **GET** `/api/workflow-templates/{id}/`
  - Retrieve a specific workflow template with its stages

- **PUT** `/api/workflow-templates/{id}/`
  - Update a specific workflow template (full update)

- **PATCH** `/api/workflow-templates/{id}/`
  - Partially update a specific workflow template

- **DELETE** `/api/workflow-templates/{id}/`
  - Delete a specific workflow template

### Workflow Stage Template Endpoints

#### 1. List/Create Workflow Stage Templates
- **GET** `/api/workflow-stage-templates/`
  - List all workflow stage templates with optional filtering
  - Query parameters:
    - `template_id`: Filter by template ID
    - `stage_type`: Filter by stage type
    - `is_active`: Filter by active status (true/false)

- **POST** `/api/workflow-stage-templates/`
  - Create a new workflow stage template
  - Request body:
    ```json
    {
      "template": 1,
      "order_index": 1,
      "stage_name": "Resume Screening",
      "description": "Initial review of candidate resume and qualifications",
      "stage_type": "screening",
      "is_active": true
    }
    ```

#### 2. Workflow Stage Template Detail Operations
- **GET** `/api/workflow-stage-templates/{id}/`
  - Retrieve a specific workflow stage template

- **PUT** `/api/workflow-stage-templates/{id}/`
  - Update a specific workflow stage template (full update)

- **PATCH** `/api/workflow-stage-templates/{id}/`
  - Partially update a specific workflow stage template

- **DELETE** `/api/workflow-stage-templates/{id}/`
  - Delete a specific workflow stage template

## Example Usage

### Creating a Complete Workflow Template

1. **Create a Workflow Template:**
```json
POST /api/workflow-templates/
{
  "name": "Software Engineer Hiring Template",
  "description": "Complete hiring process for software engineering positions",
  "is_active": true
}
```

2. **Add Workflow Stage Templates:**
```json
POST /api/workflow-stage-templates/
{
  "template": 1,
  "order_index": 1,
  "stage_name": "Resume Review",
  "description": "Initial resume screening and qualification check",
  "stage_type": "screening",
  "is_active": true
}

POST /api/workflow-stage-templates/
{
  "template": 1,
  "order_index": 2,
  "stage_name": "Phone Screening",
  "description": "Brief phone conversation to assess basic fit",
  "stage_type": "interview",
  "is_active": true
}

POST /api/workflow-stage-templates/
{
  "template": 1,
  "order_index": 3,
  "stage_name": "Technical Assessment",
  "description": "Coding challenge or technical evaluation",
  "stage_type": "assessment",
  "is_active": true
}

POST /api/workflow-stage-templates/
{
  "template": 1,
  "order_index": 4,
  "stage_name": "Technical Interview",
  "description": "In-depth technical discussion with team",
  "stage_type": "interview",
  "is_active": true
}

POST /api/workflow-stage-templates/
{
  "template": 1,
  "order_index": 5,
  "stage_name": "Cultural Fit Interview",
  "description": "Assess cultural alignment and soft skills",
  "stage_type": "interview",
  "is_active": true
}

POST /api/workflow-stage-templates/
{
  "template": 1,
  "order_index": 6,
  "stage_name": "Reference Check",
  "description": "Contact previous employers and references",
  "stage_type": "reference_check",
  "is_active": true
}

POST /api/workflow-stage-templates/
{
  "template": 1,
  "order_index": 7,
  "stage_name": "Job Offer",
  "description": "Salary negotiation and formal offer",
  "stage_type": "offer",
  "is_active": true
}
```

### Querying Templates

1. **Get all active workflow templates:**
```
GET /api/workflow-templates/?is_active=true
```

2. **Search templates by name:**
```
GET /api/workflow-templates/?name=engineer
```

3. **Get all stages for a specific template:**
```
GET /api/workflow-stage-templates/?template_id=1
```

4. **Get only screening stages:**
```
GET /api/workflow-stage-templates/?stage_type=screening&is_active=true
```

### Sample Response

**GET /api/workflow-templates/1/**
```json
{
  "id": 1,
  "name": "Software Engineer Hiring Template",
  "description": "Complete hiring process for software engineering positions",
  "is_active": true,
  "created_at": "2025-07-26T12:00:00Z",
  "updated_at": "2025-07-26T12:00:00Z",
  "stage_count": 7,
  "stages": [
    {
      "id": 1,
      "template": 1,
      "order_index": 1,
      "stage_name": "Resume Review",
      "description": "Initial resume screening and qualification check",
      "stage_type": "screening",
      "is_active": true,
      "created_at": "2025-07-26T12:01:00Z",
      "updated_at": "2025-07-26T12:01:00Z"
    },
    {
      "id": 2,
      "template": 1,
      "order_index": 2,
      "stage_name": "Phone Screening",
      "description": "Brief phone conversation to assess basic fit",
      "stage_type": "interview",
      "is_active": true,
      "created_at": "2025-07-26T12:02:00Z",
      "updated_at": "2025-07-26T12:02:00Z"
    }
    // ... additional stages
  ]
}
```

## Use Cases

### 1. Template-Based Workflow Creation
Create standardized workflows for different job types:
- Software Engineer Template
- Sales Representative Template
- Manager Template
- Intern Template

### 2. Workflow Consistency
Ensure all hiring processes follow the same structured approach across different departments or job postings.

### 3. Template Management
- Enable/disable templates based on current hiring needs
- Update templates to reflect process improvements
- Clone successful templates for new job types

### 4. Process Analytics
- Track which template stages are most effective
- Identify bottlenecks in standard processes
- Compare performance across different templates

## Database Considerations

- **Unique Constraints**: Each template can have only one stage with the same `order_index`
- **Cascading Deletes**: Deleting a template will delete all associated stage templates
- **Template Inheritance**: Templates can be used to create actual workflows for specific jobs
- **Flexible Ordering**: Stages can be reordered by updating `order_index` values

## Validation Rules

### WorkflowTemplate Validation
- `name` cannot be empty or just whitespace
- `name` is trimmed of leading/trailing whitespace

### WorkflowStageTemplate Validation
- `order_index` must be positive (> 0)
- `order_index` must be unique within a template
- `stage_type` must be one of the predefined choices

## Migration

To apply the database changes, run:
```bash
python manage.py migrate
```

This will create the `workflow_templates` and `workflow_stage_templates` tables in your database.

## Integration with Existing Workflow System

The template system is designed to work alongside the existing Workflow and WorkflowStep models:

1. **Templates as Blueprints**: Use templates to define standard processes
2. **Instance Creation**: Create actual workflows from templates for specific jobs
3. **Customization**: Modify individual workflow instances without affecting the template
4. **Maintenance**: Update templates to improve future workflow creation

This template system provides a foundation for creating consistent, reusable hiring processes while maintaining the flexibility to customize individual workflows as needed.
