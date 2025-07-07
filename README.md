# Microservices Architecture


## 1. User & Auth Service

### Scope:
- Authentication, Authorization, JWT/Supabase Auth
- User and role management (admin, recruiter, manager, external client)
- Permissions, audit logs, GDPR compliance, and consent management

### Technology:
- Django/Flask
- PostgreSQL
- JWT or Supabase Auth

---

## 2. Jobs & Applications Service

### Scope:
- Job creation, editing, archival, multi-channel publishing
- Customizable pipeline and application management
- Advanced filtering, emails, notes, task assignments, collaborative feedback, mentions
- Approval workflows
- Interview scheduling & calendar integrations
- Candidate portal (status tracking, job recommendations)

### Technology:
- Django/Flask
- PostgreSQL
- SMTP API (SendGrid/Mailgun)
- Google/Microsoft Calendar APIs

---

## 3. AI Engine Service (Parsing, Matching, Scoring & Chatbot)

### Scope:
- CV parsing (LangChain + PyMuPDF + spaCy/HuggingFace)
- AI-based semantic matching (Instructor Embedding, vector storage with Qdrant)
- Candidate scoring logic and customization (ML/rule-based)
- AI prequalification chatbot (LLM integrations like GPT-4/Mistral)

### Technology:
- FastAPI (for high performance)
- Qdrant
- LangChain
- HuggingFace
- GPT-4/Mistral API
- PostgreSQL (scoring data)

---

## 4. Integration & Notification Service

### Scope:
- REST APIs (documented with Swagger/Redoc)
- Webhooks, Zapier/Make integrations, external APIs (Notion, Pipedrive, etc.)
- Real-time notifications, email communications
- Chrome extension API integration for LinkedIn profile extraction

### Technology:
- Django Rest Framework/FastAPI
- PostgreSQL
- SMTP
- WebSockets (optional)
- Chrome Extension API

---

## 5. Analytics & Reporting Service

### Scope:
- Recruitment analytics and statistics (conversion rates, delays, etc.)
- Predictive analytics (time-to-hire, drop-off detection)
- Dashboard visualizations, KPIs, interactive charts

### Technology:
- Django/Flask
- PostgreSQL
- Pandas, NumPy
- Recharts/Vue.js for frontend dashboards










# ATS Simple Backend

This project is a simple backend API built with Django and Django REST Framework.

## Setup Instructions (Windows)

1. **Clone the repository**
    ```bash
    git clone <repository-url>
    cd ats_simple_be
    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server**
    ```bash
    python manage.py runserver
    ```

## API

The API is powered by Django REST Framework. Access the browsable API at `http://127.0.0.1:8000/api/schema/swagger-ui/` OR `http://127.0.0.1:8000/api/`.


