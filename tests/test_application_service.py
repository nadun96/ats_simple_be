#!/usr/bin/env python3
"""
Application Service Test Suite
Tests all application service endpoints
"""

import requests
import json
import time

# Service URL
APPLICATION_SERVICE_URL = "http://localhost:8001/api/v1"

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
                    key_fields = ["id", "title", "name", "status", "count", "results"]
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
    """Check if application service is healthy"""
    print_section("🏥 APPLICATION SERVICE HEALTH CHECK")

    health_endpoints = [
        f"{APPLICATION_SERVICE_URL}/health/",
        f"{APPLICATION_SERVICE_URL}/",
        "http://localhost:8001/health/",
        "http://localhost:8001/"
    ]

    for endpoint in health_endpoints:
        result = test_endpoint("GET", endpoint, description=f"Health check via {endpoint}")
        if result is not None:
            print(f"{Colors.GREEN}✓ Application service is running{Colors.END}")
            return True

    print(f"{Colors.RED}✗ Application service is not accessible{Colors.END}")
    return False


def test_job_endpoints():
    """Test job-related endpoints"""
    print_section("💼 JOB ENDPOINTS")
    
    # Test job listing
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/jobs/", description="List jobs")
    
    # Test job creation
    job_data = {
        "title": f"Test Job {int(time.time())}",
        "description": "A test job for automated testing",
        "status": "open",
        "location": "Remote"
    }
    
    job_result = test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/jobs/", 
        job_data, 
        "Create new job"
    )
    
    # Test complete job creation
    complete_job_data = {
        "title": f"Complete Test Job {int(time.time())}",
        "description": "A complete test job",
        "requirements": ["Python", "Django"],
        "status": "open"
    }
    
    test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/jobs/complete/", 
        complete_job_data, 
        "Create complete job"
    )
    
    # If job was created, test job detail
    if job_result and isinstance(job_result, dict) and "id" in job_result:
        job_id = job_result["id"]
        test_endpoint(
            "GET", 
            f"{APPLICATION_SERVICE_URL}/jobs/{job_id}/", 
            description=f"Get job detail for ID {job_id}"
        )
        
        # Test job update
        update_data = {"status": "closed"}
        test_endpoint(
            "PATCH", 
            f"{APPLICATION_SERVICE_URL}/jobs/{job_id}/", 
            update_data, 
            description=f"Update job {job_id}"
        )


def test_society_endpoints():
    """Test society-related endpoints"""
    print_section("🏢 SOCIETY ENDPOINTS")
    
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/societies/", description="List societies")
    
    society_data = {
        "name": f"Test Society {int(time.time())}",
        "description": "A test society",
        "status": "active"
    }
    
    society_result = test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/societies/", 
        society_data, 
        "Create new society"
    )
    
    if society_result and isinstance(society_result, dict) and "id" in society_result:
        society_id = society_result["id"]
        test_endpoint(
            "GET", 
            f"{APPLICATION_SERVICE_URL}/societies/{society_id}/", 
            description=f"Get society detail for ID {society_id}"
        )


def test_form_endpoints():
    """Test form-related endpoints"""
    print_section("📝 FORM ENDPOINTS")
    
    # Job Forms
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/job-forms/", description="List job forms")
    
    form_data = {
        "name": f"Test Form {int(time.time())}",
        "description": "A test form"
    }
    
    form_result = test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/job-forms/", 
        form_data, 
        "Create job form"
    )
    
    if form_result and isinstance(form_result, dict) and "id" in form_result:
        form_id = form_result["id"]
        test_endpoint(
            "GET", 
            f"{APPLICATION_SERVICE_URL}/job-forms/{form_id}/", 
            description=f"Get form detail for ID {form_id}"
        )
    
    # Form Fields
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/form-fields/", description="List form fields")
    
    field_data = {
        "name": f"test_field_{int(time.time())}",
        "field_type": "text",
        "label": "Test Field"
    }
    
    test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/form-fields/", 
        field_data, 
        "Create form field"
    )


def test_team_endpoints():
    """Test team-related endpoints"""
    print_section("👥 TEAM ENDPOINTS")
    
    # Teams
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/teams/", description="List teams")
    
    team_data = {
        "name": f"Test Team {int(time.time())}",
        "description": "A test team"
    }
    
    team_result = test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/teams/", 
        team_data, 
        "Create team"
    )
    
    if team_result and isinstance(team_result, dict) and "id" in team_result:
        team_id = team_result["id"]
        test_endpoint(
            "GET", 
            f"{APPLICATION_SERVICE_URL}/teams/{team_id}/", 
            description=f"Get team detail for ID {team_id}"
        )
    
    # Team Members
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/team-members/", description="List team members")
    
    member_data = {
        "email": f"testmember_{int(time.time())}@test.com",
        "role": "member"
    }
    
    test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/team-members/", 
        member_data, 
        "Create team member"
    )


def test_workflow_endpoints():
    """Test workflow-related endpoints"""
    print_section("🔄 WORKFLOW ENDPOINTS")
    
    # Workflow Templates
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/workflow-templates/", description="List workflow templates")
    
    template_data = {
        "name": f"Test Template {int(time.time())}",
        "description": "A test workflow template"
    }
    
    test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/workflow-templates/", 
        template_data, 
        "Create workflow template"
    )
    
    # Workflow Steps
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/workflow-steps/", description="List workflow steps")
    
    # Workflow Actions
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/workflow-actions/", description="List workflow actions")
    
    # Workflow Tasks
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/workflow-tasks/", description="List workflow tasks")
    
    # Task Comments
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/task-comments/", description="List task comments")
    
    # Step Links
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/step-links/", description="List step links")


def test_candidate_endpoints():
    """Test candidate and application endpoints"""
    print_section("👤 CANDIDATE & APPLICATION ENDPOINTS")
    
    # Candidates
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/candidates/", description="List candidates")
    
    candidate_data = {
        "first_name": "Test",
        "last_name": "Candidate",
        "email": f"candidate_{int(time.time())}@test.com",
        "phone": "+1234567890"
    }
    
    candidate_result = test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/candidates/", 
        candidate_data, 
        "Create candidate"
    )
    
    if candidate_result and isinstance(candidate_result, dict) and "candidate_id" in candidate_result:
        candidate_id = candidate_result["candidate_id"]
        test_endpoint(
            "GET", 
            f"{APPLICATION_SERVICE_URL}/candidates/{candidate_id}/", 
            description=f"Get candidate detail for ID {candidate_id}"
        )
    
    # Applications V2
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/v2/applications/", description="List applications v2")
    
    application_data = {
        "candidate_email": f"applicant_{int(time.time())}@test.com",
        "job_id": 1,
        "status": "submitted"
    }
    
    app_result = test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/v2/applications/", 
        application_data, 
        "Create application v2"
    )
    
    if app_result and isinstance(app_result, dict) and "application_id" in app_result:
        app_id = app_result["application_id"]
        test_endpoint(
            "GET", 
            f"{APPLICATION_SERVICE_URL}/v2/applications/{app_id}/", 
            description=f"Get application detail for ID {app_id}"
        )
        
        # Test application stage operations
        test_endpoint(
            "POST", 
            f"{APPLICATION_SERVICE_URL}/v2/applications/{app_id}/advance/", 
            {}, 
            f"Advance application {app_id} stage"
        )
        
        move_data = {"stage": "interview"}
        test_endpoint(
            "POST", 
            f"{APPLICATION_SERVICE_URL}/v2/applications/{app_id}/move-stage/", 
            move_data, 
            f"Move application {app_id} to stage"
        )


def test_legacy_endpoints():
    """Test legacy endpoints"""
    print_section("📚 LEGACY ENDPOINTS")
    
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/job-description/", description="Job description endpoint")
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/job-descriptions/", description="Job descriptions list")
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/applications/", description="Legacy applications list")


def test_job_site_endpoints():
    """Test job site endpoints"""
    print_section("🌐 JOB SITE ENDPOINTS")
    
    test_endpoint("GET", f"{APPLICATION_SERVICE_URL}/job-sites/", description="List job sites")
    
    site_data = {
        "name": f"Test Site {int(time.time())}",
        "url": "https://testsite.com"
    }
    
    test_endpoint(
        "POST", 
        f"{APPLICATION_SERVICE_URL}/job-sites/", 
        site_data, 
        "Create job site"
    )


def test_application_service():
    """Test all application service endpoints"""
    print_header("APPLICATION SERVICE TESTS", Colors.BLUE)

    if not check_service_health():
        return False

    test_job_endpoints()
    test_society_endpoints()
    test_form_endpoints()
    test_team_endpoints()
    test_workflow_endpoints()
    test_candidate_endpoints()
    test_legacy_endpoints()
    test_job_site_endpoints()

    return True


if __name__ == "__main__":
    print_header("🚀 STARTING APPLICATION SERVICE TESTS", Colors.GREEN)
    result = test_application_service()
    
    if result:
        print_header("✅ APPLICATION SERVICE TESTS COMPLETED", Colors.GREEN)
    else:
        print_header("❌ APPLICATION SERVICE TESTS FAILED", Colors.RED)
