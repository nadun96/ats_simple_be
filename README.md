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

The API is powered by Django REST Framework. Access the browsable API at `http://localhost:8000/api/`.
