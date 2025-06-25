#!/usr/bin/env python3
"""
Test script to verify the timeout fix in MCP server.
This script tests the Marvel comics search with increased timeout.
"""

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from everything_search import EverythingSearch

def test_marvel_search_with_timeout():
    """Test Marvel search with different timeout values."""
    try:
        # Initialize Everything Search
        es = EverythingSearch()
        
        print("Testing Marvel search with different timeouts...")
        
        # Test with original short timeout (5 seconds)
        print("\n1. Testing with 5-second timeout:")
        try:
            results = es.search(
                query="marvel path:Z:\\30.comix",
                max_results=50,
                timeout=5000,
                include_full_path=True,
                include_size=True
            )
            print(f"Found {len(results)} results with 5s timeout")
            if results:
                print(f"First result: {results[0].get('Name', 'N/A')}")
        except Exception as e:
            print(f"5s timeout failed: {e}")
        
        # Test with longer timeout (30 seconds)
        print("\n2. Testing with 30-second timeout:")
        try:
            results = es.search(
                query="marvel path:Z:\\30.comix",
                max_results=50,
                timeout=30000,
                include_full_path=True,
                include_size=True
            )
            print(f"Found {len(results)} results with 30s timeout")
            if results:
                print(f"First result: {results[0].get('Name', 'N/A')}")
                print(f"Sample results:")
                for i, result in enumerate(results[:5]):
                    print(f"  {i+1}. {result.get('Name', 'N/A')}")
        except Exception as e:
            print(f"30s timeout failed: {e}")
        
        # Test with very long timeout (60 seconds) 
        print("\n3. Testing with 60-second timeout:")
        try:
            results = es.search(
                query="marvel path:Z:\\30.comix",
                max_results=100,
                timeout=60000,
                include_full_path=True,
                include_size=True
            )
            print(f"Found {len(results)} results with 60s timeout")
            if results:
                print(f"First result: {results[0].get('Name', 'N/A')}")
                print(f"Total results found: {len(results)}")
        except Exception as e:
            print(f"60s timeout failed: {e}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_marvel_search_with_timeout()