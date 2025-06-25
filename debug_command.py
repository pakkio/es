#!/usr/bin/env python3
"""
Debug script to see exactly what command the Python wrapper generates.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from everything_search import EverythingSearch

def debug_marvel_search():
    """Debug the exact command being generated for Marvel search."""
    try:
        # Initialize Everything Search
        es = EverythingSearch()
        
        # Monkey patch the search method to print the command
        original_search = es.search
        
        def debug_search(*args, **kwargs):
            # Import required modules inside the function
            import tempfile
            
            # This is a simplified version of the command building logic
            cmd = [es.es_path]
            
            query = kwargs.get('query', args[0] if args else '')
            path_filter = kwargs.get('path_filter', None)
            timeout = kwargs.get('timeout', 5000)
            max_results = kwargs.get('max_results', None)
            
            if query:
                cmd.append(query)
            
            if path_filter:
                cmd.extend(['-path', path_filter])
            
            if max_results:
                cmd.extend(['-n', str(max_results)])
                
            cmd.append('-csv')
            cmd.extend(['-timeout', str(timeout)])
            cmd.append('-full-path-and-name')
            
            print(f"Generated command: {' '.join(repr(c) for c in cmd)}")
            print(f"Command as string: {' '.join(cmd)}")
            
            # Call original method
            return original_search(*args, **kwargs)
        
        # Patch the method
        es.search = debug_search
        
        print("Testing Marvel search with different path formats...")
        
        # Test 1: Using path_filter parameter
        print("\n1. Using path_filter parameter:")
        try:
            results = es.search(
                query="marvel",
                path_filter="Z:\\30.comix",
                max_results=10,
                timeout=30000,
                include_full_path=True
            )
            print(f"Found {len(results)} results")
        except Exception as e:
            print(f"Failed: {e}")
        
        # Test 2: Using path: syntax in query
        print("\n2. Using path: syntax in query:")
        try:
            results = es.search(
                query="marvel path:Z:\\30.comix",
                max_results=10,
                timeout=30000,
                include_full_path=True
            )
            print(f"Found {len(results)} results")
        except Exception as e:
            print(f"Failed: {e}")
            
    except Exception as e:
        print(f"Debug failed: {e}")

if __name__ == "__main__":
    debug_marvel_search()