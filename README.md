# ATS (Application Tracking System) - Microservices Backend

## 🚀 Quick Start

### Database Setup (Recommended First Time)
```bash
# Windows
scripts\setup-databases.bat

# Linux/Mac  
chmod +x scripts/setup-databases.sh
./scripts/setup-databases.sh
```

### Manual Start
```bash
# Start all services
./start_services.bat    # Windows
./start_services.sh     # Linux/Mac

# Or using Docker Compose directly
docker-compose up -d --build

# Run comprehensive tests
python test_all_services.py
```

## 📂 Project Structure

```
ats_simple_be/
├── docs/                     # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── DATABASE_SETUP.md     # Database setup guide
│   ├── SETUP_SUMMARY.md      # Quick setup summary
│   └── TROUBLESHOOTING.md
├── scripts/                  # Setup and utility scripts
│   ├── init-db.sh           # Database initialization
│   ├── wait-for-db.sh       # Database readiness checker
│   ├── setup-databases.sh   # One-click setup (Linux/Mac)
│   ├── setup-databases.bat  # One-click setup (Windows)
│   ├── check-databases.sh   # Database status checker
│   └── reset-databases.sh   # Reset all data
├── auth_service/            # Authentication microservice
├── application_service/     # Core application logic
├── email_service/          # Email and notifications
├── notification_service/   # Push notifications (future)
└── docker-compose.yml     # Container orchestration
```

## 📖 Documentation

- **[Database Setup Guide](docs/DATABASE_SETUP.md)** - Complete database setup instructions
- **[Setup Summary](docs/SETUP_SUMMARY.md)** - Quick reference for setup
- **[API Documentation](docs/API_DOCUMENTATION.md)** - API endpoints and usage
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 📋 Services Overview

### 🔐 Authentication Service (:8000)
**Purpose**: User authentication, registration, JWT tokens, role management

**Features**:
- JWT-based authentication
- User registration and login  
- Role-based permissions
- Password reset functionality
- User profile management

**Technology**: Django, PostgreSQL, JWT

---

### 📊 Application Service (:8001)
**Purpose**: Core recruitment functionality with job management, candidate tracking, and workflow automation

**Features**:
- **Job Management**: Complete job lifecycle with forms, teams, and workflows
- **Enhanced Candidate Profiles**: Skills, experience, education, file uploads
- **Application Processing**: Workflow-driven application management
- **Form Management**: Custom application forms with file support
- **Team Collaboration**: Team assignments and task management
- **Workflow Automation**: Stage-based processing with automated actions

**Key Endpoints**:
- `/api/v1/jobs/` - Job management
- `/api/v1/candidates/` - Candidate management  
- `/api/v1/v2/applications/` - Enhanced application processing
- `/api/v1/workflow-templates/` - Workflow management

**Technology**: Django, PostgreSQL, File Storage

---

### 📧 Email Service (:8002)
**Purpose**: Email template management, queue processing, and analytics

**Features**:
- Template-based email system
- Queue-based email processing with Celery
- Email analytics and tracking
- Template variable substitution
- Background workers for async processing

**Technology**: Django, PostgreSQL, Celery, RabbitMQ, Redis

---

### 🔔 Notification Service (:8003)
**Purpose**: Real-time notifications and user preferences

**Features**:
- In-app notification system
- Real-time updates via WebSocket
- User notification preferences
- Notification categorization

**Technology**: Django, PostgreSQL, WebSocket

---

## 🏗️ Infrastructure

### Core Services
- **PostgreSQL** (:5432) - Primary database
- **Redis** (:6379) - Caching and sessions
- **RabbitMQ** (:5672, :15672) - Message queue

### Background Workers
- **email_worker** - Celery email processing
- **email_beat** - Celery scheduler
- **email_queue_consumer** - RabbitMQ consumer

## 📚 Documentation

- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Complete project documentation
- **[APPLICATION_CANDIDATE_API.md](APPLICATION_CANDIDATE_API.md)** - Enhanced application endpoints
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Detailed API documentation

## 🧪 Testing

```bash
# Test all microservices
python test_all_services.py

# Test application service only
python test_endpoints.py

# Run specific service tests
docker-compose exec application_service python manage.py test
```

## 🔧 Development Setup

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd ats_simple_be
   cp .env.example .env
   ```

2. **Start Services**
   ```bash
   docker-compose up -d --build
   ```

3. **Apply Migrations**
   ```bash
   docker-compose exec application_service python manage.py migrate
   docker-compose exec auth_service python manage.py migrate
   docker-compose exec email_service python manage.py migrate
   ```

4. **Load Initial Data**
   ```bash
   docker-compose exec email_service python manage.py load_email_templates
   ```

## 🌟 Key Features

### Workflow Processing
- Applications automatically flow through defined stages
- Each stage triggers automated actions (emails, notifications, tasks)
- Complete audit trail for compliance
- Manual stage advancement and movement

### Enhanced Candidate Management
- Rich candidate profiles with skills, experience, education
- Resume/CV upload and parsing
- Flexible data storage for various attributes
- Integration with application workflow

### Smart Application Processing
- Create applications with new or existing candidates
- Custom job application forms with file uploads
- Automated workflow assignment
- Form answer processing and storage

### Email Automation
- Template-based email system
- Queue processing for high volume
- Integration with workflow stages
- Analytics and tracking

## 🚀 Production Deployment

See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for detailed deployment instructions including:
- Environment configuration
- Database setup
- Scaling considerations
- Security guidelines
- Monitoring setup

## 🔧 Troubleshooting

Common issues and solutions are documented in [TROUBLESHOOTING.md](TROUBLESHOOTING.md):
- Service connection issues
- Database problems
- Port conflicts
- Environment configuration
- Performance monitoring

## 📊 Service URLs

- **Auth Service**: http://localhost:8000
- **Application Service**: http://localhost:8001
- **Email Service**: http://localhost:8002  
- **Notification Service**: http://localhost:8003
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

## 🎯 Future Enhancements

### Planned Services

#### 🤖 AI Engine Service (Future)
- **CV Parsing**: LangChain + PyMuPDF + spaCy/HuggingFace
- **Semantic Matching**: Instructor Embedding, vector storage with Qdrant
- **Candidate Scoring**: ML/rule-based scoring logic
- **AI Chatbot**: LLM integrations (GPT-4/Mistral) for prequalification
- **Technology**: FastAPI, Qdrant, LangChain, HuggingFace

#### 📱 Communication Service (Future)
- **Real-time Chat**: WebSocket-based messaging
- **Video Interviews**: Integration with video platforms
- **SMS Notifications**: Two-way SMS communication
- **Social Integration**: LinkedIn, Indeed integrations

#### 📊 Analytics Service (Future)  
- **Recruitment Metrics**: Time-to-hire, source effectiveness
- **Predictive Analytics**: Success prediction models
- **Custom Reports**: Flexible reporting engine
- **Data Visualization**: Interactive dashboards

#### 🔧 Integration Service (Future)
- **Third-party APIs**: ATS integrations, job boards
- **Webhook Management**: Event-driven integrations
- **Data Sync**: Multi-platform synchronization
- **API Gateway**: Centralized API management

## 📈 Current Status

✅ **Completed**:
- Authentication Service with JWT
- Core Application Service with enhanced features
- Email Service with template management
- Notification Service foundation
- Workflow automation system
- Enhanced candidate management
- File upload and processing
- Comprehensive API documentation
- Docker-based deployment
- Testing suite

🚧 **In Development**:
- Advanced analytics
- Real-time features
- Performance optimization
- Security enhancements

📋 **Planned**:
- AI-powered features
- Mobile API optimization  
- Third-party integrations
- Advanced reporting

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

- 📖 **Documentation**: Check the `/docs` directory
- 🐛 **Issues**: Create GitHub issues for bugs
- 💬 **Questions**: Use GitHub discussions
- 🧪 **Testing**: Run `python test_all_services.py`

---

**Last Updated**: August 2025  
**Version**: 1.0.0  
**Status**: Production Ready

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

The API is powered by Django REST Framework. Access the browsable API at `http://127.0.0.1:8000/swagger/`.


