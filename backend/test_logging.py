#!/usr/bin/env python3
"""
Test script to verify logging middleware functionality
"""
import requests
import json
import time

def test_logging_middleware():
    """Test the logging middleware with a sample query"""
    
    # Test server endpoint
    url = "http://localhost:8000/query"
    
    # Sample query data
    test_data = {
        "question": "What is artificial intelligence?"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Testing logging middleware...")
    print(f"Sending query: {test_data['question']}")
    
    try:
        # Make the request
        start_time = time.time()
        response = requests.post(url, json=test_data, headers=headers)
        end_time = time.time()
        
        print(f"Response status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.3f}s")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result.get('answer', 'No answer')[:100]}...")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_logging_middleware()
