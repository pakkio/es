#!/usr/bin/env python3
"""
Test script for MCP server functionality
"""

import asyncio
import json
from mcp_server import mcp


async def test_mcp_server():
    """Test the MCP server tools"""
    print("Testing Everything Search MCP Server")
    print("=" * 50)
    
    # List available tools
    tools = await mcp.list_tools()
    print(f"Available tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description or 'No description'}")
    
    print("\n" + "=" * 50)
    print("MCP Server is ready!")
    
    # Test a simple tool call
    try:
        result = await mcp.call_tool("get_everything_version", {})
        print(f"Everything Search version: {result}")
    except Exception as e:
        print(f"Note: Could not test version tool (Everything Search may not be available): {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())