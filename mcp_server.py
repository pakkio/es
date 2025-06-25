"""
MCP Server for Everything Search

This module provides a Model Context Protocol (MCP) server that exposes
Everything Search functionality as tools that can be used by LLM applications.
"""

import json
from typing import Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP
from everything_search import EverythingSearch

# Initialize the MCP server
mcp = FastMCP("everything-search")

# Global instance of Everything Search
es_instance = None


def get_everything_search() -> EverythingSearch:
    """Get or create Everything Search instance."""
    global es_instance
    if es_instance is None:
        es_instance = EverythingSearch()
    return es_instance


@mcp.tool()
def search_files(
    query: str = "",
    max_results: int = 20,
    regex: bool = False,
    case_sensitive: bool = False,
    include_size: bool = True,
    include_date_modified: bool = True,
    sort_by: str = "name",
    timeout: int = 30000,
) -> str:
    """
    Search for files using Everything Search.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 20)
        regex: Use regular expressions (default: False)
        case_sensitive: Match case exactly (default: False)
        include_size: Include file size in results (default: True)
        include_date_modified: Include modification date (default: True)
        sort_by: Sort results by field (name, size, date, etc.)
        timeout: Search timeout in milliseconds (default: 30000 = 30 seconds)
    
    Returns:
        JSON string containing search results
    """
    try:
        es = get_everything_search()
        results = es.search_files(
            query=query,
            max_results=max_results,
            regex=regex,
            case_sensitive=case_sensitive,
            include_size=include_size,
            include_date_modified=include_date_modified,
            include_full_path=True,
            sort_by=sort_by,
            timeout=timeout,
        )
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def search_folders(
    query: str = "",
    max_results: int = 20,
    regex: bool = False,
    case_sensitive: bool = False,
    sort_by: str = "name",
    timeout: int = 30000,
) -> str:
    """
    Search for folders using Everything Search.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 20)
        regex: Use regular expressions (default: False)
        case_sensitive: Match case exactly (default: False)
        sort_by: Sort results by field (name, size, date, etc.)
        timeout: Search timeout in milliseconds (default: 30000 = 30 seconds)
    
    Returns:
        JSON string containing search results
    """
    try:
        es = get_everything_search()
        results = es.search_folders(
            query=query,
            max_results=max_results,
            regex=regex,
            case_sensitive=case_sensitive,
            include_full_path=True,
            sort_by=sort_by,
            timeout=timeout,
        )
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def search_by_extension(
    extension: str,
    max_results: int = 20,
    include_size: bool = True,
    include_date_modified: bool = True,
    sort_by: str = "name",
) -> str:
    """
    Search for files by extension using Everything Search.
    
    Args:
        extension: File extension to search for (e.g., "py", "txt", "exe")
        max_results: Maximum number of results to return (default: 20)
        include_size: Include file size in results (default: True)
        include_date_modified: Include modification date (default: True)
        sort_by: Sort results by field (name, size, date, etc.)
    
    Returns:
        JSON string containing search results
    """
    try:
        es = get_everything_search()
        results = es.search_by_extension(
            extension=extension,
            max_results=max_results,
            include_size=include_size,
            include_date_modified=include_date_modified,
            include_full_path=True,
            sort_by=sort_by,
        )
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def search_by_size(
    size_filter: str,
    max_results: int = 20,
    include_date_modified: bool = True,
    sort_by: str = "size",
    sort_ascending: bool = False,
) -> str:
    """
    Search for files by size using Everything Search.
    
    Args:
        size_filter: Size filter (e.g., ">100MB", "<1KB", "1GB..5GB")
        max_results: Maximum number of results to return (default: 20)
        include_date_modified: Include modification date (default: True)
        sort_by: Sort results by field (default: "size")
        sort_ascending: Sort in ascending order (default: False for largest first)
    
    Returns:
        JSON string containing search results
    """
    try:
        es = get_everything_search()
        results = es.search_by_size(
            size_filter=size_filter,
            max_results=max_results,
            include_size=True,
            include_date_modified=include_date_modified,
            include_full_path=True,
            sort_by=sort_by,
            sort_ascending=sort_ascending,
        )
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def search_recent_files(
    days: int = 7,
    max_results: int = 20,
    include_size: bool = True,
    sort_by: str = "date-modified",
    sort_ascending: bool = False,
) -> str:
    """
    Search for recently modified files using Everything Search.
    
    Args:
        days: Number of days to look back (default: 7)
        max_results: Maximum number of results to return (default: 20)
        include_size: Include file size in results (default: True)
        sort_by: Sort results by field (default: "date-modified")
        sort_ascending: Sort in ascending order (default: False for newest first)
    
    Returns:
        JSON string containing search results
    """
    try:
        es = get_everything_search()
        results = es.search_recent(
            days=days,
            max_results=max_results,
            include_size=include_size,
            include_date_modified=True,
            include_full_path=True,
            sort_by=sort_by,
            sort_ascending=sort_ascending,
        )
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def advanced_search(
    query: str,
    max_results: int = 20,
    regex: bool = False,
    case_sensitive: bool = False,
    whole_words: bool = False,
    match_path: bool = False,
    files_only: bool = False,
    folders_only: bool = False,
    path_filter: Optional[str] = None,
    include_size: bool = True,
    include_extension: bool = True,
    include_date_modified: bool = True,
    sort_by: str = "name",
    sort_ascending: bool = True,
    timeout: int = 30000,
) -> str:
    """
    Advanced search with full control over search parameters.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 20)
        regex: Use regular expressions (default: False)
        case_sensitive: Match case exactly (default: False)
        whole_words: Match whole words only (default: False)
        match_path: Match full path and filename (default: False)
        files_only: Return only files (default: False)
        folders_only: Return only folders (default: False)
        path_filter: Search within specific path (optional)
        include_size: Include file size in results (default: True)
        include_extension: Include file extension (default: True)
        include_date_modified: Include modification date (default: True)
        sort_by: Sort results by field (default: "name")
        sort_ascending: Sort in ascending order (default: True)
        timeout: Search timeout in milliseconds (default: 30000 = 30 seconds)
    
    Returns:
        JSON string containing search results
    """
    try:
        es = get_everything_search()
        results = es.search(
            query=query,
            max_results=max_results,
            regex=regex,
            case_sensitive=case_sensitive,
            whole_words=whole_words,
            match_path=match_path,
            files_only=files_only,
            folders_only=folders_only,
            path_filter=path_filter,
            include_name=True,
            include_full_path=True,
            include_size=include_size,
            include_extension=include_extension,
            include_date_modified=include_date_modified,
            sort_by=sort_by,
            sort_ascending=sort_ascending,
            timeout=timeout,
        )
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_result_count(query: str) -> str:
    """
    Get the total number of results for a search query without fetching them.
    
    Args:
        query: Search query string
    
    Returns:
        JSON string with result count
    """
    try:
        es = get_everything_search()
        count = es.get_result_count(query)
        return json.dumps({"query": query, "count": count})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_everything_version() -> str:
    """
    Get the version of Everything Search.
    
    Returns:
        JSON string with version information
    """
    try:
        es = get_everything_search()
        version = es.get_version()
        return json.dumps({"version": version})
    except Exception as e:
        return json.dumps({"error": str(e)})


# Export function for running the server
def run_server():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    run_server()