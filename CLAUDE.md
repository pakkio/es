# CLAUDE.md - Development Context

## Project Overview
Everything Search Python Wrapper with Model Context Protocol (MCP) server for LLM integration.

## Key Components
- `everything_search.py` - Core Python wrapper for Everything Search (es.exe)
- `mcp_server.py` - MCP server exposing 8 search tools for LLMs
- `start_mcp_server.py` - MCP server startup script

## Development Setup

### WSL/Linux Environment
When developing from WSL, the Everything Search executable is accessed via Windows filesystem mounting:

```bash
# Everything Search path in WSL
/mnt/c/Program Files/Everything/es.exe

# Python wrapper automatically uses this path
es = EverythingSearch()  # Uses default WSL path
```

### Installation for WSL Development

1. **Install Everything Search on Windows**
   - Download from [voidtools.com](https://www.voidtools.com/)
   - Ensure Everything is running and indexing files

2. **Clone and setup Python environment**
   ```bash
   git clone https://github.com/pakkio/es.git
   cd es
   poetry install
   ```

3. **Test basic functionality**
   ```bash
   python3 -c "from everything_search import EverythingSearch; es = EverythingSearch(); print(f'Found {len(es.search(\"*.txt\", max_results=5))} txt files')"
   ```

### MCP Server Setup for Claude Desktop

When using from WSL, you'll need to copy files to Windows-accessible location:

1. **Copy project to Windows filesystem**
   ```bash
   # Create Windows directory
   mkdir -p "/mnt/c/Users/$USER/everything-search-py"
   
   # Copy project files
   cp -r . "/mnt/c/Users/$USER/everything-search-py/"
   ```

2. **Install MCP dependencies in Windows Python**
   ```bash
   # Navigate to Windows Python environment
   cd "/mnt/c/Users/$USER/everything-search-py"
   
   # Install MCP dependencies (requires Python 3.10+)
   pip install mcp fastmcp
   ```

3. **Configure Claude Desktop**
   Add to Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "everything-search": {
         "command": "python",
         "args": ["C:\\Users\\YOUR_USER\\everything-search-py\\start_mcp_server.py"]
       }
     }
   }
   ```

## Critical Issues Resolved

### UTF-8 Encoding Issue
**Problem**: Files with special characters (like "Español") caused UTF-8 decoding errors.

**Solution**: Added `errors="replace"` to subprocess call in `everything_search.py:165`:
```python
result = subprocess.run(
    cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
)
```

### Timeout Configuration
**Enhancement**: Added configurable timeouts to MCP tools (default: 30 seconds).

## Testing

### Basic Wrapper Test
```bash
python3 test_fixed_search.py
```

### MCP Server Test
```bash
python3 test_mcp.py
```

### Encoding Fix Verification
```bash
python3 -c "
from everything_search import EverythingSearch
es = EverythingSearch()
results = es.search('marvel', path_filter='Z:\\30.comix', max_results=5)
print(f'Found {len(results)} Marvel comics')
"
```

## Common Commands

### Development
```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .

# Run MCP server
poetry run python mcp_server.py
```

### Build and Deploy
```bash
# Build package
poetry build

# Commit changes
git add .
git commit -m "Description"
git push origin main
```

## Architecture Notes

### EverythingSearch Class
- Handles subprocess calls to `es.exe`
- Parses CSV output from Everything Search
- Provides Pythonic interface with comprehensive error handling

### MCP Server
- Exposes 8 tools: search_files, search_folders, search_by_extension, etc.
- Uses FastMCP framework
- Returns JSON-formatted results
- Configurable timeouts for large searches

### Path Handling
- WSL: Uses `/mnt/c/Program Files/Everything/es.exe`
- Windows: Can use direct Windows paths
- Supports both path_filter parameter and path: query syntax

## Known Issues

1. **Special Characters**: Handled via encoding replacement (fixed)
2. **WSL Path Access**: Requires Windows Everything installation
3. **Python Version**: MCP server requires Python 3.10+
4. **File Permissions**: Everything must be running with proper indexing permissions

## Performance Considerations

- Use `max_results` parameter to limit large searches
- Increase timeout for directories with many files (100k+)
- Consider using `get_result_count()` before fetching large result sets
- Path-specific searches are more efficient than global searches