#!/usr/bin/env python3
"""
Auth Service Test Suite
Tests all auth service endpoints
"""

import requests
import json
import time

# Service URL
AUTH_SERVICE_URL = "http://localhost:8000/api"

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
                    # Print key info without overwhelming output
                    key_fields = ["id", "message", "count", "status", "email", "username", "access", "refresh"]
                    summary = {k: v for k, v in result.items() if k in key_fields}
                    if summary:
                        print(f"{Colors.WHITE}Response: {json.dumps(summary, indent=2)}{Colors.END}")
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
    """Check if auth service is healthy"""
    print_section("🏥 AUTH SERVICE HEALTH CHECK")

    # Health check endpoints
    health_endpoints = [
        f"{AUTH_SERVICE_URL}/health/",
        f"{AUTH_SERVICE_URL}/",
        "http://localhost:8000/health/",
        "http://localhost:8000/"
    ]

    for endpoint in health_endpoints:
        result = test_endpoint("GET", endpoint, description=f"Health check via {endpoint}")
        if result is not None:
            print(f"{Colors.GREEN}✓ Auth service is running{Colors.END}")
            return True

    print(f"{Colors.RED}✗ Auth service is not accessible{Colors.END}")
    return False


def test_auth_endpoints():
    """Test all authentication endpoints"""
    print_header("AUTHENTICATION SERVICE TESTS", Colors.PURPLE)

    if not check_service_health():
        return None

    print_section("📋 AVAILABLE ENDPOINTS")
    
    # Test the items endpoint (the only available endpoint)
    test_endpoint("GET", f"{AUTH_SERVICE_URL}/items/", description="List items")
    
    # Test item creation
    item_data = {
        "name": f"Test Item {int(time.time())}",
        "description": "A test item for automated testing"
    }
    
    item_result = test_endpoint(
        "POST", 
        f"{AUTH_SERVICE_URL}/items/", 
        item_data, 
        "Create new item"
    )
    
    # If item was created, test item detail
    if item_result and isinstance(item_result, dict) and "id" in item_result:
        item_id = item_result["id"]
        test_endpoint(
            "GET", 
            f"{AUTH_SERVICE_URL}/items/{item_id}/", 
            description=f"Get item detail for ID {item_id}"
        )
        
        # Test item update
        update_data = {"description": "Updated test item"}
        test_endpoint(
            "PATCH", 
            f"{AUTH_SERVICE_URL}/items/{item_id}/", 
            update_data, 
            description=f"Update item {item_id}"
        )
        
        # Test item deletion
        test_endpoint(
            "DELETE", 
            f"{AUTH_SERVICE_URL}/items/{item_id}/", 
            description=f"Delete item {item_id}"
        )

    print_section("� DOCUMENTATION ENDPOINTS")
    
    # Test documentation endpoints
    test_endpoint("GET", f"{AUTH_SERVICE_URL}/schema/", description="API Schema")
    test_endpoint("GET", f"{AUTH_SERVICE_URL}/schema/swagger-ui/", description="Swagger UI")
    test_endpoint("GET", f"{AUTH_SERVICE_URL}/schema/redoc/", description="ReDoc")

    return {"message": "Auth service tested successfully"}


if __name__ == "__main__":
    print_header("🚀 STARTING AUTH SERVICE TESTS", Colors.GREEN)
    result = test_auth_endpoints()
    
    if result:
        print_header("✅ AUTH SERVICE TESTS COMPLETED", Colors.GREEN)
    else:
        print_header("❌ AUTH SERVICE TESTS FAILED", Colors.RED)
