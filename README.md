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

## Prerequisites

- **Everything Search** installed on your system
  - Download from [voidtools.com](https://www.voidtools.com/)
  - Ensure `es.exe` (command-line interface) is available
- **Python 3.8.1+**

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd everything-search-py

# Install with Poetry
poetry install

# Or install for development
poetry install --with dev
```

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt  # (if you have requirements.txt)

# Or just copy everything_search.py to your project
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
- **Python**: 3.8.1+ (tested up to 3.12)
- **Everything Search**: 1.1.0.30+ (may work with older versions)

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