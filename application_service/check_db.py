#!/usr/bin/env python
"""
Database connection test script for Application Service
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from django.db import connection
from django.core.management.color import make_style

style = make_style()


def check_database():
    """Check database connection and run basic queries"""
    try:
        print(style.HTTP_INFO("🔍 Testing database connection..."))

        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(style.SUCCESS(f"✅ Database connection successful: {result}"))

        # Check database name
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            db_name = cursor.fetchone()[0]
            print(style.SUCCESS(f"✅ Connected to database: {db_name}"))

        # Check if tables exist
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%job%'
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            if tables:
                table_names = [table[0] for table in tables]
                print(style.SUCCESS(f"✅ Job-related tables found: {table_names}"))
            else:
                print(
                    style.WARNING(
                        "⚠️  No job-related tables found yet (migrations may not have run)"
                    )
                )

        # Test model imports
        try:
            from apps.api.models.job import Job, Society

            print(style.SUCCESS("✅ Models imported successfully"))

            # Count existing records
            job_count = Job.objects.count()
            society_count = Society.objects.count()
            print(
                style.SUCCESS(
                    f"✅ Current data: {job_count} jobs, {society_count} societies"
                )
            )

        except Exception as model_error:
            print(style.WARNING(f"⚠️  Model import/query error: {model_error}"))

        return True

    except Exception as e:
        print(style.ERROR(f"❌ Database check failed: {e}"))
        return False


if __name__ == "__main__":
    print(style.HTTP_INFO("🚀 ATS Application Service - Database Health Check"))
    print(style.HTTP_INFO("=" * 50))

    success = check_database()

    if success:
        print(style.HTTP_INFO("=" * 50))
        print(style.SUCCESS("🎉 Database is ready for use!"))
    else:
        print(style.HTTP_INFO("=" * 50))
        print(style.ERROR("💥 Database check failed!"))

    sys.exit(0 if success else 1)
