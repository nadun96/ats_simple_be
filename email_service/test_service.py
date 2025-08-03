#!/usr/bin/env python
"""
Test script for Email Service
Run this after starting the service to validate functionality
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8002/api/"


def test_health_check():
    """Test health endpoints"""
    print("Testing health check...")

    response = requests.get("http://localhost:8002/health/")
    assert response.status_code == 200
    print("✓ Basic health check passed")

    response = requests.get("http://localhost:8002/health/detailed/")
    assert response.status_code == 200
    health_data = response.json()
    print(f"✓ Detailed health check: {health_data['status']}")


def test_email_templates():
    """Test email template endpoints"""
    print("\nTesting email templates...")

    # List templates
    response = requests.get(f"{BASE_URL}templates/")
    assert response.status_code == 200
    templates = response.json()["results"]
    print(f"✓ Found {len(templates)} email templates")

    # Create test template
    test_template = {
        "name": "test_template",
        "template_type": "notification",
        "subject": "Test Subject - {name}",
        "body_html": "<p>Hello {name}, this is a test.</p>",
        "body_text": "Hello {name}, this is a test.",
    }

    response = requests.post(f"{BASE_URL}templates/", json=test_template)
    if response.status_code == 201:
        template_id = response.json()["id"]
        print("✓ Test template created")

        # Clean up
        requests.delete(f"{BASE_URL}templates/{template_id}/")
        print("✓ Test template cleaned up")


def test_send_notification():
    """Test immediate notification sending"""
    print("\nTesting notification sending...")

    notification_data = {
        "recipient": "test@example.com",
        "subject": "Test Notification",
        "message": "This is a test notification from the email service.",
        "email_type": "notification",
        "notification_id": "test_001",
    }

    response = requests.post(
        f"{BASE_URL}emails/send_notification/", json=notification_data
    )
    assert response.status_code == 200
    print("✓ Notification queued successfully")


def test_scheduled_email():
    """Test scheduled email creation"""
    print("\nTesting scheduled email...")

    # Schedule email for 1 hour from now
    scheduled_time = datetime.now() + timedelta(hours=1)

    email_data = {
        "recipient": "scheduled@example.com",
        "subject": "Scheduled Test Email",
        "body_html": "<p>This is a scheduled test email.</p>",
        "body_text": "This is a scheduled test email.",
        "email_type": "task_reminder",
        "scheduled_at": scheduled_time.isoformat(),
    }

    response = requests.post(f"{BASE_URL}emails/", json=email_data)
    assert response.status_code == 201
    email_id = response.json()["id"]
    print(f"✓ Scheduled email created with ID: {email_id}")


def test_scheduled_task():
    """Test scheduled task creation"""
    print("\nTesting scheduled task...")

    # Schedule task for 30 minutes from now
    scheduled_time = datetime.now() + timedelta(minutes=30)

    task_data = {
        "task_id": f"test_task_{int(datetime.now().timestamp())}",
        "task_type": "meeting_reminder",
        "scheduled_at": scheduled_time.isoformat(),
        "recipient_email": "task@example.com",
        "email_data": {
            "task_name": "Test Meeting",
            "assignee_name": "Test User",
            "due_date": scheduled_time.strftime("%Y-%m-%d %H:%M"),
            "priority": "High",
        },
    }

    response = requests.post(f"{BASE_URL}scheduled-tasks/", json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]
    print(f"✓ Scheduled task created with ID: {task_id}")


def test_email_statistics():
    """Test email statistics endpoint"""
    print("\nTesting email statistics...")

    response = requests.get(f"{BASE_URL}emails/statistics/")
    assert response.status_code == 200
    stats = response.json()
    print(f"✓ Statistics: {stats['total_emails']} total emails")


def test_upcoming_tasks():
    """Test upcoming tasks endpoint"""
    print("\nTesting upcoming tasks...")

    response = requests.get(f"{BASE_URL}scheduled-tasks/upcoming/?hours=24")
    assert response.status_code == 200
    tasks = response.json()
    print(f"✓ Found {len(tasks)} upcoming tasks in next 24 hours")


def main():
    """Run all tests"""
    print("Email Service Test Suite")
    print("=" * 40)

    try:
        test_health_check()
        test_email_templates()
        test_send_notification()
        test_scheduled_email()
        test_scheduled_task()
        test_email_statistics()
        test_upcoming_tasks()

        print("\n" + "=" * 40)
        print("✓ All tests passed! Email service is working correctly.")

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Cannot connect to email service at {BASE_URL}")
        print("Make sure the service is running on http://localhost:8002")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
