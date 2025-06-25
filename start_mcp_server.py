#!/usr/bin/env python3
"""
Startup script for Everything Search MCP Server
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_server import run_server

if __name__ == "__main__":
    run_server()