#!/usr/bin/env python3
"""
Test script for the Evolution Tool Hub MCP endpoints.
Verifies that all tools are discoverable and executable.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_discovery():
    """Test the /agent/tools discovery endpoint"""
    print("🔍 Testing Tool Discovery...")
    response = requests.get(f"{BASE_URL}/agent/tools")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Discovery successful!")
        print(f"   Protocol: {data.get('protocol')}")
        print(f"   Tools available: {len(data.get('tools', []))}")
        
        for tool in data.get('tools', [])[:3]:
            print(f"   - {tool['name']}: {tool['description']}")
        
        return True
    else:
        print(f"❌ Discovery failed: {response.status_code}")
        return False

def test_execution_safe():
    """Test executing a safe tool (k8s_cluster_status)"""
    print("\n🛠️  Testing Safe Tool Execution...")
    payload = {
        "name": "k8s_cluster_status",
        "arguments": {}
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/execute",
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Execution successful!")
        print(f"   Status: {data.get('status')}")
        if 'pods' in data:
            print(f"   Pods found: {len(data.get('pods', []))}")
        elif 'message' in data:
            print(f"   Message: {data.get('message')}")
        return True
    else:
        print(f"❌ Execution failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def test_health():
    """Test the agent health endpoint"""
    print("\n💚 Testing Agent Health...")
    response = requests.get(f"{BASE_URL}/agent/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Agent is {data.get('status')}")
        print(f"   Tools available: {data.get('tools_available')}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def main():
    print("=" * 50)
    print("Evolution Tool Hub - MCP Endpoint Tests")
    print("=" * 50)
    
    try:
        results = []
        results.append(("Discovery", test_discovery()))
        results.append(("Health", test_health()))
        results.append(("Safe Execution", test_execution_safe()))
        
        print("\n" + "=" * 50)
        print("Test Results:")
        print("=" * 50)
        
        for name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} - {name}")
        
        all_passed = all(result[1] for result in results)
        
        if all_passed:
            print("\n🎉 All tests passed! MCP interface is operational.")
        else:
            print("\n⚠️  Some tests failed. Check the backend logs.")
        
        return all_passed
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to backend at", BASE_URL)
        print("   Make sure the backend is running:")
        print("   cd phase2/backend && python main.py")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
