#!/usr/bin/env python3
"""
FluxCore Backend API Testing Suite
Tests all endpoints and the Six-Walled Fortress security system
"""

import requests
import sys
import time
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class FluxCoreAPITester:
    def __init__(self, base_url="https://self-running-apps.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        self.test_results.append({
            "name": name,
            "success": success,
            "details": details
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        
        # Default headers
        default_headers = {'Content-Type': 'application/json'}
        if self.token:
            default_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            default_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.log_test(name, True)
                try:
                    return True, response.json()
                except:
                    return True, response.text
            else:
                self.log_test(name, False, f"Expected {expected_status}, got {response.status_code}: {response.text}")
                return False, {}

        except Exception as e:
            self.log_test(name, False, f"Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        print("\n🔍 Testing Root Endpoint...")
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )
        return success

    def test_user_registration(self):
        """Test user registration"""
        print("\n🔍 Testing User Registration...")
        test_email = f"testuser_{int(time.time())}@fluxcore.com"
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data={"email": test_email, "password": "test123"}
        )
        
        if success and 'token' in response:
            self.token = response['token']
            self.user_id = response['user']['id']
            print(f"   📝 Registered user: {test_email}")
            print(f"   🎁 Welcome credits: {response['user']['credits']}")
        
        return success

    def test_user_login(self):
        """Test user login with existing credentials"""
        print("\n🔍 Testing User Login...")
        
        # First register a user
        test_email = f"logintest_{int(time.time())}@fluxcore.com"
        reg_success, reg_response = self.run_test(
            "Registration for Login Test",
            "POST",
            "auth/register",
            200,
            data={"email": test_email, "password": "test123"}
        )
        
        if not reg_success:
            return False
        
        # Now test login
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data={"email": test_email, "password": "test123"}
        )
        
        if success and 'token' in response:
            print(f"   🔑 Login successful for: {test_email}")
        
        return success

    def test_user_profile(self):
        """Test getting user profile (requires auth)"""
        print("\n🔍 Testing User Profile...")
        if not self.token:
            self.log_test("User Profile", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Get User Profile",
            "GET",
            "user/profile",
            200
        )
        
        if success:
            print(f"   👤 Profile: {response.get('email', 'N/A')}")
            print(f"   💰 Credits: {response.get('credits', 'N/A')}")
        
        return success

    def test_user_transactions(self):
        """Test getting user transactions"""
        print("\n🔍 Testing User Transactions...")
        if not self.token:
            self.log_test("User Transactions", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Get User Transactions",
            "GET",
            "user/transactions",
            200
        )
        
        if success:
            print(f"   📊 Transaction count: {len(response) if isinstance(response, list) else 'N/A'}")
        
        return success

    def test_marketplace_packages(self):
        """Test getting marketplace packages"""
        print("\n🔍 Testing Marketplace Packages...")
        success, response = self.run_test(
            "Get Marketplace Packages",
            "GET",
            "marketplace/packages",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   📦 Available packages: {len(response)}")
            for pkg in response:
                popular = " (POPULAR)" if pkg.get('popular') else ""
                print(f"   - {pkg.get('name', 'N/A')}: ${pkg.get('price', 'N/A')}{popular}")
        
        return success

    def test_marketplace_purchase(self):
        """Test purchasing credits"""
        print("\n🔍 Testing Marketplace Purchase...")
        if not self.token:
            self.log_test("Marketplace Purchase", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Purchase Credits (Starter Pack)",
            "POST",
            "marketplace/purchase",
            200,
            data={"package_id": "starter", "user_id": self.user_id}
        )
        
        if success:
            print(f"   💳 Purchase result: {response.get('success', False)}")
            print(f"   ➕ Credits added: {response.get('credits_added', 'N/A')}")
        
        return success

    def test_wall_status(self):
        """Test getting wall status"""
        print("\n🔍 Testing Wall Status...")
        success, response = self.run_test(
            "Get Wall Status",
            "GET",
            "monitor/walls",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   🏰 Active walls: {len(response)}")
            for wall in response:
                print(f"   - Wall {wall.get('wall_number', 'N/A')}: {wall.get('name', 'N/A')}")
                print(f"     Status: {wall.get('status', 'N/A')}, Blocked: {wall.get('total_blocked', 0)}")
        
        return success

    def test_starheart_status(self):
        """Test getting Starheart status"""
        print("\n🔍 Testing Starheart Status...")
        success, response = self.run_test(
            "Get Starheart Status",
            "GET",
            "monitor/starheart",
            200
        )
        
        if success:
            print(f"   ⭐ Status: {response.get('status', 'N/A')}")
            print(f"   ⚡ Total power: {response.get('total_generated', 0)}")
            print(f"   📈 Generation rate: {response.get('power_generation_rate', 0)}")
            print(f"   🎯 Efficiency: {response.get('efficiency', 0):.2f}%")
        
        return success

    def test_system_stats(self):
        """Test getting system statistics"""
        print("\n🔍 Testing System Statistics...")
        success, response = self.run_test(
            "Get System Stats",
            "GET",
            "monitor/stats",
            200
        )
        
        if success:
            print(f"   👥 Total users: {response.get('total_users', 0)}")
            print(f"   💰 Credits distributed: {response.get('total_credits_distributed', 0)}")
            print(f"   🌀 Entropy converted: {response.get('total_entropy_converted', 0)}")
            print(f"   🛡️ Attacks blocked: {response.get('total_attacks_blocked', 0)}")
        
        return success

    def test_rate_limiting(self):
        """Test rate limiting to trigger the Six-Walled Fortress"""
        print("\n🔍 Testing Rate Limiting (Six-Walled Fortress)...")
        
        # Make rapid requests to trigger walls
        def make_request():
            try:
                response = requests.get(f"{self.base_url}/monitor/walls", timeout=5)
                return response.status_code
            except:
                return None
        
        print("   🚀 Sending rapid requests to trigger walls...")
        
        # Send 20 rapid requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = []
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
        
        # Check if any requests were blocked (429 status)
        blocked_count = sum(1 for r in results if r == 429)
        success_count = sum(1 for r in results if r == 200)
        
        print(f"   📊 Results: {success_count} successful, {blocked_count} blocked")
        
        if blocked_count > 0:
            self.log_test("Rate Limiting Triggered", True, f"{blocked_count} requests blocked by fortress")
            
            # Wait a moment then check if entropy was generated
            time.sleep(2)
            wall_success, wall_response = self.run_test(
                "Wall Status After Attack",
                "GET",
                "monitor/walls",
                200
            )
            
            if wall_success:
                total_blocked = sum(wall.get('total_blocked', 0) for wall in wall_response)
                total_entropy = sum(wall.get('entropy_generated', 0) for wall in wall_response)
                print(f"   🏰 Total attacks blocked: {total_blocked}")
                print(f"   🌀 Total entropy generated: {total_entropy:.2f}")
            
            return True
        else:
            self.log_test("Rate Limiting Triggered", False, "No requests were blocked")
            return False

    def test_entropy_to_power_conversion(self):
        """Test if entropy is being converted to power"""
        print("\n🔍 Testing Entropy to Power Conversion...")
        
        # Get initial Starheart status
        initial_success, initial_response = self.run_test(
            "Initial Starheart Status",
            "GET",
            "monitor/starheart",
            200
        )
        
        if not initial_success:
            return False
        
        initial_power = initial_response.get('total_generated', 0)
        
        # Trigger some rate limiting to generate entropy
        print("   🚀 Generating entropy through rate limiting...")
        for _ in range(10):
            try:
                requests.get(f"{self.base_url}/monitor/walls", timeout=1)
            except:
                pass
        
        # Wait for processing
        time.sleep(3)
        
        # Check Starheart status again
        final_success, final_response = self.run_test(
            "Final Starheart Status",
            "GET",
            "monitor/starheart",
            200
        )
        
        if final_success:
            final_power = final_response.get('total_generated', 0)
            power_increase = final_power - initial_power
            
            print(f"   ⚡ Initial power: {initial_power}")
            print(f"   ⚡ Final power: {final_power}")
            print(f"   📈 Power increase: {power_increase}")
            
            if power_increase > 0:
                self.log_test("Entropy to Power Conversion", True, f"Generated {power_increase} power units")
                return True
            else:
                self.log_test("Entropy to Power Conversion", False, "No power increase detected")
                return False
        
        return False

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting FluxCore Backend API Tests")
        print("=" * 50)
        
        # Basic API tests
        self.test_root_endpoint()
        self.test_user_registration()
        self.test_user_login()
        self.test_user_profile()
        self.test_user_transactions()
        
        # Marketplace tests
        self.test_marketplace_packages()
        self.test_marketplace_purchase()
        
        # Monitoring tests
        self.test_wall_status()
        self.test_starheart_status()
        self.test_system_stats()
        
        # Security system tests
        self.test_rate_limiting()
        self.test_entropy_to_power_conversion()
        
        # Print final results
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        print(f"✅ Tests passed: {self.tests_passed}/{self.tests_run}")
        print(f"❌ Tests failed: {self.tests_run - self.tests_passed}/{self.tests_run}")
        
        if self.tests_passed < self.tests_run:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['name']}: {result['details']}")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"\n📈 Success rate: {success_rate:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = FluxCoreAPITester()
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())