#!/usr/bin/env python3
"""
Comprehensive Test Runner for All Microservices
Runs all service tests and provides a summary
"""

import os
import sys
import subprocess
import time
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text, color=Colors.CYAN):
    """Print a formatted header"""
    print(f"\n{color}{Colors.BOLD}{'='*60}")
    print(f"{text.center(60)}")
    print(f"{'='*60}{Colors.END}\n")

def print_section(text, color=Colors.BLUE):
    """Print a formatted section header"""
    print(f"\n{color}{Colors.BOLD}{'-'*50}")
    print(f"{text}")
    print(f"{'-'*50}{Colors.END}")

def run_test_file(test_file, service_name):
    """Run a test file and return results"""
    print_section(f"🧪 TESTING {service_name.upper()}", Colors.PURPLE)
    
    if not os.path.exists(test_file):
        print(f"{Colors.RED}❌ Test file not found: {test_file}{Colors.END}")
        return False, f"Test file not found"
    
    try:
        start_time = time.time()
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, timeout=120)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ {service_name} tests PASSED ({duration:.1f}s){Colors.END}")
            
            # Count successful operations from output
            success_count = result.stdout.count('✓ SUCCESS')
            fail_count = result.stdout.count('✗ FAILED')
            
            print(f"{Colors.CYAN}📊 Results: {success_count} passed, {fail_count} failed{Colors.END}")
            
            return True, f"{success_count} passed, {fail_count} failed"
        else:
            print(f"{Colors.RED}❌ {service_name} tests FAILED ({duration:.1f}s){Colors.END}")
            print(f"{Colors.YELLOW}Error Output:{Colors.END}")
            print(result.stderr[-500:] if result.stderr else "No error output")
            
            return False, f"Test execution failed: {result.returncode}"
            
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}❌ {service_name} tests TIMED OUT{Colors.END}")
        return False, "Timeout after 120 seconds"
    except Exception as e:
        print(f"{Colors.RED}❌ {service_name} tests ERROR: {e}{Colors.END}")
        return False, f"Exception: {e}"

def check_services_running():
    """Check if all services are running"""
    print_section("🔍 CHECKING SERVICE HEALTH", Colors.YELLOW)
    
    services = [
        ("Auth Service", "http://localhost:8000/api/"),
        ("Application Service", "http://localhost:8001/api/"),
        ("Email Service", "http://localhost:8002/api/")
    ]
    
    all_running = True
    for service_name, url in services:
        try:
            import requests
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"{Colors.GREEN}✅ {service_name} is running{Colors.END}")
            else:
                print(f"{Colors.RED}❌ {service_name} returned status {response.status_code}{Colors.END}")
                all_running = False
        except Exception as e:
            print(f"{Colors.RED}❌ {service_name} is not accessible: {e}{Colors.END}")
            all_running = False
    
    return all_running

def main():
    print_header("🚀 COMPREHENSIVE MICROSERVICES TEST SUITE", Colors.PURPLE)
    
    # Record start time
    overall_start = time.time()
    
    # Check if services are running
    if not check_services_running():
        print(f"\n{Colors.RED}❌ Not all services are running. Please start all services first.{Colors.END}")
        print(f"{Colors.YELLOW}💡 Run: docker-compose up -d{Colors.END}")
        return 1
    
    # Define test files and service names
    tests = [
        ("test_auth_service.py", "Auth Service"),
        ("test_application_service.py", "Application Service"),
        ("test_email_service.py", "Email Service")
    ]
    
    results = []
    
    # Run each test
    for test_file, service_name in tests:
        success, details = run_test_file(test_file, service_name)
        results.append((service_name, success, details))
        
        # Add small delay between tests
        time.sleep(1)
    
    # Print final summary
    overall_end = time.time()
    total_duration = overall_end - overall_start
    
    print_header("📊 FINAL TEST SUMMARY", Colors.CYAN)
    
    passed_tests = 0
    failed_tests = 0
    
    for service_name, success, details in results:
        status_icon = "✅" if success else "❌"
        status_color = Colors.GREEN if success else Colors.RED
        
        print(f"{status_color}{status_icon} {service_name}: {details}{Colors.END}")
        
        if success:
            passed_tests += 1
        else:
            failed_tests += 1
    
    print(f"\n{Colors.BOLD}Overall Results:{Colors.END}")
    print(f"{Colors.GREEN}✅ Services Passed: {passed_tests}{Colors.END}")
    print(f"{Colors.RED}❌ Services Failed: {failed_tests}{Colors.END}")
    print(f"{Colors.BLUE}⏱️  Total Duration: {total_duration:.1f} seconds{Colors.END}")
    
    # Final status
    if failed_tests == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! 🎉{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  SOME TESTS FAILED ⚠️{Colors.END}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
