#!/usr/bin/env python3
"""
Test script to verify the encoding fix and proper search syntax.
"""

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from everything_search import EverythingSearch

def test_working_search():
    """Test with the exact syntax that works from command line."""
    try:
        # Initialize Everything Search
        es = EverythingSearch()
        
        print("Testing with exact working command syntax...")
        
        # Test 1: Use exact working syntax from command line
        print("\n1. Using exact working syntax (marvel path:Z:\\30.comix):")
        try:
            results = es.search(
                query="marvel path:Z:\\30.comix",
                max_results=10,
                timeout=30000,
                include_full_path=True,
                include_size=True
            )
            print(f"Found {len(results)} results")
            if results:
                print("Sample results:")
                for i, result in enumerate(results[:5]):
                    print(f"  {i+1}. {result}")
        except Exception as e:
            print(f"Failed: {e}")
        
        # Test 2: Use path_filter parameter (that was failing with encoding)
        print("\n2. Using path_filter parameter with encoding fix:")
        try:
            results = es.search(
                query="marvel",
                path_filter="Z:\\30.comix",
                max_results=10,
                timeout=30000,
                include_full_path=True,
                include_size=True
            )
            print(f"Found {len(results)} results")
            if results:
                print("Sample results:")
                for i, result in enumerate(results[:5]):
                    print(f"  {i+1}. {result}")
        except Exception as e:
            print(f"Failed: {e}")
            
        # Test 3: Simple test without path restriction
        print("\n3. Simple marvel search without path:")
        try:
            results = es.search(
                query="marvel",
                max_results=5,
                timeout=30000,
                include_full_path=True
            )
            print(f"Found {len(results)} results")
            if results:
                print("Sample results:")
                for i, result in enumerate(results[:3]):
                    print(f"  {i+1}. {result}")
        except Exception as e:
            print(f"Failed: {e}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_working_search()