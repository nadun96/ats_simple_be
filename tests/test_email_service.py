#!/usr/bin/env python3
"""
Email Service Test Suite
Tests all email service endpoints
"""

import requests
import json
import time

# Service URL
EMAIL_SERVICE_URL = "http://localhost:8002/api"

# Test Colors
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_header(text, color=Colors.BLUE):
    print(f"\n{color}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{color}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{color}{Colors.BOLD}{'=' * 60}{Colors.END}")


def print_section(text, color=Colors.CYAN):
    print(f"\n{color}{Colors.BOLD}{'-' * 50}{Colors.END}")
    print(f"{color}{Colors.BOLD}{text}{Colors.END}")
    print(f"{color}{'-' * 50}{Colors.END}")


def test_endpoint(method, url, data=None, description="", headers=None, expected_status=None):
    """Test an API endpoint with enhanced output"""
    print(f"\n{Colors.YELLOW}🔍 {description}{Colors.END}")
    print(f"{Colors.WHITE}{method.upper()} {url}{Colors.END}")

    if data:
        print(f"{Colors.WHITE}Request Data: {json.dumps(data, indent=2)[:200]}...{Colors.END}")

    try:
        response = None
        if method.lower() == "get":
            response = requests.get(url, headers=headers, timeout=10)
        elif method.lower() == "post":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.lower() == "patch":
            response = requests.patch(url, json=data, headers=headers, timeout=10)
        elif method.lower() == "delete":
            response = requests.delete(url, headers=headers, timeout=10)
        elif method.lower() == "put":
            response = requests.put(url, json=data, headers=headers, timeout=10)

        if response is None:
            print(f"{Colors.RED}✗ UNSUPPORTED METHOD: {method}{Colors.END}")
            return None

        status_ok = expected_status is None or response.status_code == expected_status

        if response.status_code < 400 and status_ok:
            print(f"{Colors.GREEN}✓ SUCCESS - Status: {response.status_code}{Colors.END}")
            try:
                result = response.json()
                if isinstance(result, dict) and len(result) > 0:
                    key_fields = ["id", "subject", "template_name", "status", "count", "results"]
                    summary = {k: v for k, v in result.items() if k in key_fields}
                    if summary:
                        print(f"{Colors.WHITE}Response: {json.dumps(summary, indent=2)[:300]}...{Colors.END}")
                elif isinstance(result, list) and len(result) > 0:
                    print(f"{Colors.WHITE}Response: List with {len(result)} items{Colors.END}")
                return result
            except Exception:
                return response.text
        else:
            print(f"{Colors.RED}✗ FAILED - Status: {response.status_code}{Colors.END}")
            try:
                error_data = response.json()
                print(f"{Colors.RED}Error: {json.dumps(error_data, indent=2)}{Colors.END}")
            except Exception:
                print(f"{Colors.RED}Error: {response.text}{Colors.END}")
            return None

    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}✗ CONNECTION ERROR - Service may not be running{Colors.END}")
        return None
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}✗ TIMEOUT ERROR{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.RED}✗ EXCEPTION: {e}{Colors.END}")
        return None


def check_service_health():
    """Check if email service is healthy"""
    print_section("🏥 EMAIL SERVICE HEALTH CHECK")

    health_endpoints = [
        f"{EMAIL_SERVICE_URL}/health/",
        f"{EMAIL_SERVICE_URL}/",
        "http://localhost:8002/health/",
        "http://localhost:8002/"
    ]

    for endpoint in health_endpoints:
        result = test_endpoint("GET", endpoint, description=f"Health check via {endpoint}")
        if result is not None:
            print(f"{Colors.GREEN}✓ Email service is running{Colors.END}")
            return True

    print(f"{Colors.RED}✗ Email service is not accessible{Colors.END}")
    return False


def test_email_template_endpoints():
    """Test email template endpoints"""
    print_section("📧 EMAIL TEMPLATE ENDPOINTS")
    
    # List templates
    test_endpoint("GET", f"{EMAIL_SERVICE_URL}/templates/", description="List email templates")
    
    # Create template
    template_data = {
        "name": f"test_template_{int(time.time())}",
        "subject": "Test Email Template",
        "body_text": "This is a test email template in plain text.",
        "body_html": "<h1>Test Email Template</h1><p>This is a test email template in HTML.</p>",
        "template_type": "notification"
    }
    
    template_result = test_endpoint(
        "POST", 
        f"{EMAIL_SERVICE_URL}/templates/", 
        template_data, 
        "Create email template"
    )
    
    # If template was created, test template detail
    if template_result and isinstance(template_result, dict) and "id" in template_result:
        template_id = template_result["id"]
        test_endpoint(
            "GET", 
            f"{EMAIL_SERVICE_URL}/templates/{template_id}/", 
            description=f"Get template detail for ID {template_id}"
        )
        
        # Test template update
        update_data = {"subject": "Updated Test Email Template"}
        test_endpoint(
            "PATCH", 
            f"{EMAIL_SERVICE_URL}/templates/{template_id}/", 
            update_data, 
            description=f"Update template {template_id}"
        )
        
        # Test template deletion
        test_endpoint(
            "DELETE", 
            f"{EMAIL_SERVICE_URL}/templates/{template_id}/", 
            description=f"Delete template {template_id}"
        )


def test_email_endpoints():
    """Test email endpoints"""
    print_section("✉️ EMAIL ENDPOINTS")
    
    # List emails
    test_endpoint("GET", f"{EMAIL_SERVICE_URL}/emails/", description="List emails")
    
    # Create/send email
    email_data = {
        "sender": "test_sender@example.com",
        "recipient": "test@example.com",
        "subject": f"Test Email {int(time.time())}",
        "body_text": "This is a test email.",
        "body_html": "<p>This is a test email.</p>",
        "email_type": "notification"
    }
    
    email_result = test_endpoint(
        "POST", 
        f"{EMAIL_SERVICE_URL}/emails/", 
        email_data, 
        "Create/send email"
    )
    
    # If email was created, test email detail
    if email_result and isinstance(email_result, dict) and "id" in email_result:
        email_id = email_result["id"]
        test_endpoint(
            "GET", 
            f"{EMAIL_SERVICE_URL}/emails/{email_id}/", 
            description=f"Get email detail for ID {email_id}"
        )
        
        # Test email update
        update_data = {"status": "sent"}
        test_endpoint(
            "PATCH", 
            f"{EMAIL_SERVICE_URL}/emails/{email_id}/", 
            update_data, 
            description=f"Update email {email_id}"
        )


def test_scheduled_task_endpoints():
    """Test scheduled task endpoints"""
    print_section("⏰ SCHEDULED TASK ENDPOINTS")
    
    # List scheduled tasks
    test_endpoint("GET", f"{EMAIL_SERVICE_URL}/scheduled-tasks/", description="List scheduled tasks")
    
    # Create scheduled task
    from datetime import datetime, timedelta
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    task_data = {
        "task_id": f"task_{int(time.time())}",
        "task_type": "meeting_reminder",  # Valid choice from API
        "scheduled_at": future_date,  # Future date
        "recipient_email": "test@example.com",
        "email_data": {"message": "Test scheduled task"}
    }
    
    task_result = test_endpoint(
        "POST", 
        f"{EMAIL_SERVICE_URL}/scheduled-tasks/", 
        task_data, 
        "Create scheduled task"
    )
    
    # If task was created, test task detail
    if task_result and isinstance(task_result, dict) and "id" in task_result:
        task_id = task_result["id"]
        test_endpoint(
            "GET", 
            f"{EMAIL_SERVICE_URL}/scheduled-tasks/{task_id}/", 
            description=f"Get task detail for ID {task_id}"
        )
        
        # Test task update
        update_data = {"status": "completed"}
        test_endpoint(
            "PATCH", 
            f"{EMAIL_SERVICE_URL}/scheduled-tasks/{task_id}/", 
            update_data, 
            description=f"Update task {task_id}"
        )
        
        # Test task deletion
        test_endpoint(
            "DELETE", 
            f"{EMAIL_SERVICE_URL}/scheduled-tasks/{task_id}/", 
            description=f"Delete task {task_id}"
        )


def test_email_queue_endpoints():
    """Test email queue endpoints"""
    print_section("📬 EMAIL QUEUE ENDPOINTS")
    
    # List queue items
    test_endpoint("GET", f"{EMAIL_SERVICE_URL}/queue/", description="List email queue items")
    
    # Note: POST is not allowed for queue endpoint (405 Method Not Allowed)
    # Create queue item
    # queue_data = {
    #     "to_email": "queue_test@example.com",
    #     "subject": f"Queued Email {int(time.time())}",
    #     "body_text": "This email is queued for sending.",
    #     "priority": "normal",
    #     "status": "pending"
    # }
    
    # queue_result = test_endpoint(
    #     "POST", 
    #     f"{EMAIL_SERVICE_URL}/queue/", 
    #     queue_data, 
    #     "Add item to email queue"
    # )
    
    # Since POST is not allowed, we can't test detail operations
    # If queue item was created, test queue item detail
    # if queue_result and isinstance(queue_result, dict) and "id" in queue_result:
    #     queue_id = queue_result["id"]
    #     test_endpoint(
    #         "GET", 
    #         f"{EMAIL_SERVICE_URL}/queue/{queue_id}/", 
    #         description=f"Get queue item detail for ID {queue_id}"
    #     )
        
    #     # Test queue item update
    #     update_data = {"status": "sent"}
    #     test_endpoint(
    #         "PATCH", 
    #         f"{EMAIL_SERVICE_URL}/queue/{queue_id}/", 
    #         update_data, 
    #         description=f"Update queue item {queue_id}"
    #     )
        
    #     # Test queue item deletion
    #     test_endpoint(
    #         "DELETE", 
    #         f"{EMAIL_SERVICE_URL}/queue/{queue_id}/", 
    #         description=f"Delete queue item {queue_id}"
    #     )


def test_bulk_operations():
    """Test bulk email operations"""
    print_section("📦 BULK OPERATIONS")
    
    # Note: Bulk endpoint returns 405 Method Not Allowed
    # Test bulk email creation
    # bulk_data = {
    #     "emails": [
    #         {
    #             "to_email": "bulk1@example.com",
    #             "subject": "Bulk Email 1",
    #             "body_text": "First bulk email"
    #         },
    #         {
    #             "to_email": "bulk2@example.com",
    #             "subject": "Bulk Email 2", 
    #             "body_text": "Second bulk email"
    #         }
    #     ]
    # }
    
    # test_endpoint(
    #     "POST", 
    #     f"{EMAIL_SERVICE_URL}/emails/bulk/", 
    #     bulk_data, 
    #     "Send bulk emails"
    # )
    
    print("⚠️  Bulk operations endpoint not available (405 Method Not Allowed)")


def test_email_statistics():
    """Test email statistics endpoints"""
    print_section("📊 EMAIL STATISTICS")
    
    # Test the actual available statistics endpoint
    test_endpoint(
        "GET", 
        f"{EMAIL_SERVICE_URL}/emails/statistics/", 
        description="Get email statistics"
    )
    
    # Test send notification endpoint
    test_endpoint(
        "GET", 
        f"{EMAIL_SERVICE_URL}/emails/send_notification/", 
        description="Get send notification endpoint info"
    )


def test_email_service():
    """Test all email service endpoints"""
    print_header("EMAIL SERVICE TESTS", Colors.PURPLE)

    if not check_service_health():
        return False

    test_email_template_endpoints()
    test_email_endpoints()
    test_scheduled_task_endpoints()
    test_email_queue_endpoints()
    test_bulk_operations()
    test_email_statistics()

    return True


if __name__ == "__main__":
    print_header("🚀 STARTING EMAIL SERVICE TESTS", Colors.GREEN)
    result = test_email_service()
    
    if result:
        print_header("✅ EMAIL SERVICE TESTS COMPLETED", Colors.GREEN)
    else:
        print_header("❌ EMAIL SERVICE TESTS FAILED", Colors.RED)
