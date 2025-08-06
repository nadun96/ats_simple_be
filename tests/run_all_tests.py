#!/usr/bin/env python3
"""
Master Test Runner for ATS Microservices
Runs all service tests in sequence
"""

import subprocess
import sys
import time
import os

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
    print(f"\n{color}{Colors.BOLD}{'=' * 80}{Colors.END}")
    print(f"{color}{Colors.BOLD}{text.center(80)}{Colors.END}")
    print(f"{color}{Colors.BOLD}{'=' * 80}{Colors.END}")


def print_section(text, color=Colors.CYAN):
    print(f"\n{color}{Colors.BOLD}{'-' * 60}{Colors.END}")
    print(f"{color}{Colors.BOLD}{text}{Colors.END}")
    print(f"{color}{'-' * 60}{Colors.END}")


def run_test_file(test_file, service_name):
    """Run a specific test file and return success status"""
    print_section(f"🧪 RUNNING {service_name.upper()} TESTS", Colors.YELLOW)
    
    start_time = time.time()
    
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.join(script_dir, test_file)
        
        if not os.path.exists(test_path):
            print(f"{Colors.RED}❌ Test file not found: {test_path}{Colors.END}")
            return False
        
        # Run the test file
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ {service_name} tests PASSED in {duration:.2f}s{Colors.END}")
            print(f"{Colors.WHITE}Output:{Colors.END}")
            print(result.stdout)
            return True
        else:
            print(f"{Colors.RED}❌ {service_name} tests FAILED in {duration:.2f}s{Colors.END}")
            print(f"{Colors.RED}Error output:{Colors.END}")
            print(result.stderr)
            print(f"{Colors.WHITE}Standard output:{Colors.END}")
            print(result.stdout)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}❌ {service_name} tests TIMED OUT after 5 minutes{Colors.END}")
        return False
    except Exception as e:
        print(f"{Colors.RED}❌ Error running {service_name} tests: {e}{Colors.END}")
        return False


def check_services_running():
    """Check if all services are running"""
    print_section("🔍 CHECKING SERVICES STATUS", Colors.CYAN)
    
    import requests
    
    services = {
        "Auth Service": "http://localhost:8000",
        "Application Service": "http://localhost:8001", 
        "Email Service": "http://localhost:8002"
    }
    
    all_running = True
    
    for service_name, url in services.items():
        try:
            response = requests.get(f"{url}/health/", timeout=5)
            if response.status_code < 400:
                print(f"{Colors.GREEN}✅ {service_name} is running{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠️  {service_name} responded with status {response.status_code}{Colors.END}")
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}❌ {service_name} is not accessible{Colors.END}")
            all_running = False
        except Exception as e:
            print(f"{Colors.RED}❌ Error checking {service_name}: {e}{Colors.END}")
            all_running = False
    
    return all_running


def run_all_tests():
    """Run all service tests"""
    print_header("🚀 ATS MICROSERVICES TEST RUNNER", Colors.GREEN)
    
    # Check if services are running
    if not check_services_running():
        print(f"\n{Colors.RED}❌ Some services are not running. Please start all services first.{Colors.END}")
        print(f"{Colors.YELLOW}💡 Run: docker-compose up -d{Colors.END}")
        return False
    
    # Define test files and service names
    tests = [
        ("test_auth_service.py", "Auth Service"),
        ("test_application_service.py", "Application Service"),
        ("test_email_service.py", "Email Service")
    ]
    
    results = {}
    total_start_time = time.time()
    
    # Run each test
    for test_file, service_name in tests:
        print(f"\n{Colors.BLUE}🔄 Starting {service_name} tests...{Colors.END}")
        success = run_test_file(test_file, service_name)
        results[service_name] = success
        
        if success:
            print(f"{Colors.GREEN}✅ {service_name} tests completed successfully{Colors.END}")
        else:
            print(f"{Colors.RED}❌ {service_name} tests failed{Colors.END}")
        
        # Add a small delay between tests
        time.sleep(2)
    
    total_duration = time.time() - total_start_time
    
    # Print summary
    print_header("📊 TEST RESULTS SUMMARY", Colors.PURPLE)
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    for service_name, success in results.items():
        status = f"{Colors.GREEN}✅ PASSED{Colors.END}" if success else f"{Colors.RED}❌ FAILED{Colors.END}"
        print(f"{service_name:20} : {status}")
    
    print(f"\n{Colors.BOLD}Total Duration: {total_duration:.2f} seconds{Colors.END}")
    print(f"{Colors.BOLD}Tests Passed: {passed_count}/{total_count}{Colors.END}")
    
    if passed_count == total_count:
        print_header("🎉 ALL TESTS PASSED!", Colors.GREEN)
        return True
    else:
        print_header("❌ SOME TESTS FAILED", Colors.RED)
        return False


def main():
    """Main function"""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Tests interrupted by user{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()
