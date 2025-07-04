# The Everything Search Python Wrapper provides a fast and flexible interface to search through files on your system.

# Everything Search Python Wrapper

[![Python Version](https://img.shields.io/badge/python-3.8.1%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive Python wrapper for Everything Search (es.exe) command-line tool by [voidtools](https://www.voidtools.com/).

Everything Search is an extremely fast file and folder search utility for Windows. This wrapper provides a Pythonic interface to harness its power programmatically.

## Features

- 🔍 **Comprehensive Search**: Files, folders, extensions, sizes, dates, and attributes
- 🎯 **Advanced Filtering**: Regex, case-sensitive, whole-word, and path matching
- 📊 **Flexible Output**: CSV parsing, result counting, and data export
- ⚡ **High Performance**: Leverages Everything's instant search capabilities
- 🐍 **Pythonic API**: Clean, intuitive interface with type hints
- 🧪 **Well Tested**: 72% test coverage with comprehensive test suite
- 📦 **Poetry Managed**: Modern Python packaging and dependency management
- 🤖 **MCP Server**: Model Context Protocol server for LLM integration

## Prerequisites

- **Everything Search** installed on your system
  - Download from [voidtools.com](https://www.voidtools.com/)
  - Ensure `es.exe` (command-line interface) is available
- **Python 3.10+** (required for MCP server functionality)

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/pakkio/es.git
cd es

# Install with Poetry
poetry install

# Or install for development
poetry install --with dev
```

### WSL/Linux Installation

When developing from WSL, special setup is required for MCP server integration:

1. **Install Everything Search on Windows** (required)
   - Download and install from [voidtools.com](https://www.voidtools.com/)
   - Ensure Everything is running and has indexed your drives

2. **Setup Python environment in WSL**
   ```bash
   git clone https://github.com/pakkio/es.git
   cd es
   poetry install
   
   # Test basic functionality
   python3 -c "from everything_search import EverythingSearch; es = EverythingSearch(); print('Everything Search is working!')"
   ```

3. **For MCP Server (Claude Desktop integration)**
   ```bash
   # Copy project to Windows-accessible location
   mkdir -p "/mnt/c/Users/$USER/everything-search-py"
   cp -r . "/mnt/c/Users/$USER/everything-search-py/"
   
   # Install MCP dependencies in Windows Python environment
   cd "/mnt/c/Users/$USER/everything-search-py"
   pip install mcp fastmcp
   ```

4. **Configure Claude Desktop**
   Add to `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "everything-search": {
         "command": "python",
         "args": ["C:\\Users\\YOUR_USERNAME\\everything-search-py\\start_mcp_server.py"]
       }
     }
   }
   ```

### Manual Installation

```bash
# Install dependencies
pip install mcp fastmcp  # For MCP server functionality

# Or just copy everything_search.py to your project (basic wrapper only)
```

## Quick Start

```python
from everything_search import EverythingSearch

# Initialize (default path works for WSL)
es = EverythingSearch()

# Basic search
results = es.search("python", max_results=10)
print(f"Found {len(results)} results")

# Search for specific file types
exe_files = es.search_by_extension("exe", max_results=5)

# Search folders only
folders = es.search_folders("temp", max_results=5)

# Search by file size
large_files = es.search_by_size(">100MB", max_results=3)

# Search recent files
recent = es.search_recent(days=7, max_results=5)
```

## MCP Server Usage

This project includes a Model Context Protocol (MCP) server that allows LLM applications like Claude Desktop to use Everything Search functionality as tools.

### Starting the MCP Server

```bash
# Using Poetry
poetry run python mcp_server.py

# Or using the startup script
python start_mcp_server.py

# Or using the installed script
poetry run everything-search-mcp
```

### Available MCP Tools

The MCP server exposes 8 tools that LLMs can use:

1. **search_files** - Search for files with various filters
2. **search_folders** - Search for folders only
3. **search_by_extension** - Search files by extension (e.g., "py", "txt")
4. **search_by_size** - Search files by size (e.g., ">100MB", "<1KB")
5. **search_recent_files** - Find recently modified files
6. **advanced_search** - Full control over all search parameters
7. **get_result_count** - Count results without fetching them
8. **get_everything_version** - Get Everything Search version

### Gradio UI

This project also includes a Gradio UI for interacting with Everything Search in a web browser.

#### Starting the Gradio UI

```bash
# Using Poetry
poetry run everything-search-gradio
```

This will launch a local web server with a user-friendly interface for all the main search functions.

### MCP Server Configuration

For Claude Desktop, add this to your configuration:

```json
{
  "mcpServers": {
    "everything-search": {
      "command": "python",
      "args": ["/path/to/everything-search-py/start_mcp_server.py"]
    }
  }
}
```

### Example MCP Tool Usage

Once connected, you can ask Claude:

- "Find all Python files larger than 1MB"
- "Search for recent text files modified in the last 3 days"
- "List all executable files in Program Files"
- "Find folders containing 'temp' in their name"

The LLM will automatically use the appropriate search tools and present the results in a readable format.

## Advanced Usage

```python
# Regex search for log files
results = es.search(r".*\.log$", regex=True, max_results=10)

# Case-sensitive search
results = es.search("Python", case_sensitive=True)

# Complex search with multiple options
results = es.search(
    "document",
    files_only=True,
    include_size=True,
    include_date_modified=True,
    sort_by="size",
    sort_ascending=False,
    max_results=50
)

# Path-specific search
results = es.search("config", path_filter="C:/Program Files/")

# Search with file attributes
results = es.search("", attributes="H", folders_only=True)  # Hidden folders

# Get result count without fetching data
count = es.get_result_count("ext:txt")
print(f"Total .txt files: {count}")

# Export search results to file
es.export_results("*.mp3", "music_files.csv", format="csv", max_results=1000)
```

## API Reference

### Core Methods

#### `EverythingSearch(es_path: str)`
Initialize the wrapper with path to `es.exe`.

**Parameters:**
- `es_path`: Path to Everything Search executable (default: `/mnt/c/Program Files/Everything/es.exe`)

#### `search(query: str, **options) -> List[Dict[str, Union[str, int]]]`
Main search method with comprehensive options.

**Key Parameters:**
- `query`: Search query string
- `max_results`: Limit number of results
- `regex`: Use regular expressions
- `case_sensitive`: Match case exactly
- `files_only`/`folders_only`: Filter by type
- `include_size`/`include_date_modified`: Include metadata
- `sort_by`: Sort by field (name, size, date, etc.)

### Convenience Methods

| Method | Description | Example |
|--------|-------------|---------|
| `search_files(query)` | Search files only | `es.search_files("*.py")` |
| `search_folders(query)` | Search folders only | `es.search_folders("temp")` |
| `search_by_extension(ext)` | Search by file extension | `es.search_by_extension("pdf")` |
| `search_by_size(filter)` | Search by file size | `es.search_by_size(">100MB")` |
| `search_recent(days)` | Search recent files | `es.search_recent(7)` |

### Utility Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| `get_version()` | Get Everything version | `str` |
| `get_result_count(query)` | Count results without fetching | `int` |
| `export_results(query, file, format)` | Export to file | `None` |

## Size Filters

Use these patterns with `search_by_size()`:

```python
es.search_by_size(">100MB")     # Larger than 100MB
es.search_by_size("<1KB")       # Smaller than 1KB  
es.search_by_size("1GB..5GB")   # Between 1GB and 5GB
es.search_by_size("=1024")      # Exactly 1024 bytes
```

## Date Filters

Use these patterns in search queries:

```python
es.search("datemodified:today")
es.search("datecreated:yesterday") 
es.search("datemodified:last7days")
es.search("datecreated:2024")
```

## Example Output Format

```python
[
    {
        'Filename': 'document.pdf',
        'Size': 1048576,  # bytes
        'Date Modified': '2024-01-15 14:30:22',
        'Path': 'C:\\Documents\\',
        'Extension': 'pdf'
    },
    {
        'Filename': 'image.jpg', 
        'Size': 524288,
        'Date Modified': '2024-01-14 09:15:33'
    }
]
```

## Development

### Setting Up Development Environment

```bash
# Clone and install
git clone <repository-url>
cd everything-search-py
poetry install

# Run tests
make test

# Format code  
make format

# Run linting
make lint

# Build package
make build
```

### Available Make Commands

- `make install` - Install dependencies
- `make test` - Run tests with coverage
- `make format` - Format code with black/isort
- `make lint` - Run all linting tools
- `make build` - Build distributable package
- `make clean` - Clean build artifacts

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov

# Run specific test
poetry run pytest tests/test_everything_search.py::TestEverythingSearch::test_search_basic

# Test MCP server
poetry run python test_mcp.py
```

## Error Handling

The wrapper provides comprehensive error handling:

```python
try:
    results = es.search("query")
except FileNotFoundError:
    print("Everything Search not found")
except TimeoutError:
    print("Search timed out")
except RuntimeError as e:
    print(f"Search failed: {e}")
```

## Performance Tips

1. **Use result limits**: Always set `max_results` for large searches
2. **Enable specific columns**: Only include needed metadata fields
3. **Use result counting**: Use `get_result_count()` for pagination
4. **Cache searches**: Store results for repeated use
5. **Export large datasets**: Use `export_results()` for bulk operations

## Compatibility

- **Windows**: Native support with Everything Search installed
- **WSL/Linux**: Works via Windows filesystem mounting
- **Python**: 3.10+ (required for MCP server, 3.8.1+ for basic wrapper)
- **Everything Search**: 1.1.0.30+ (may work with older versions)
- **MCP Clients**: Compatible with Claude Desktop and other MCP-enabled applications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite and linting
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [voidtools](https://www.voidtools.com/) for creating Everything Search
- The Python community for excellent tooling and libraries

## Support

- Check existing [Issues](https://github.com/yourusername/everything-search-py/issues)
- Create a new issue for bugs or feature requests
- See `example_usage.py` for comprehensive examples