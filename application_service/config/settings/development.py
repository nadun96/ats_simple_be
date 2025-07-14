from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "3.83.252.93"]

print("🧪 ALLOWED_HOSTS:", ALLOWED_HOSTS)

print("🧪 DB Host:", os.environ.get("DATABASE_HOST"))
print("🧪 DB User:", os.environ.get("DATABASE_USER"))
# TODO: Move sensitive data to environment variables
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get(
            "DATABASE_HOST",
        ),
        "PORT": "5432",
    }
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS settings for development - allow all origins
CORS_ALLOW_ALL_ORIGINS = True
# Remove the specific allowed origins since we're allowing all
CORS_ALLOWED_ORIGINS = [
    "http://3.83.252.93:8000",
    "http://localhost",  # Add scheme
]
