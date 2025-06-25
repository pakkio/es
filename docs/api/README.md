# Everything Search Python API Documentation

## Overview

The Everything Search Python wrapper provides a comprehensive interface to Everything Search (es.exe) with two main components:

1. **EverythingSearch Class** - Core Python wrapper for es.exe
2. **MCP Server** - Model Context Protocol server exposing 8 search tools for LLM integration

## EverythingSearch Class

### Constructor

```python
EverythingSearch(es_path: str = "/mnt/c/Program Files/Everything/es.exe")
```

**Parameters:**
- `es_path` (str): Path to Everything Search executable
  - Default: `/mnt/c/Program Files/Everything/es.exe` (WSL path)
  - Windows: `C:\Program Files\Everything\es.exe`

**Raises:**
- `FileNotFoundError`: If es.exe not found at specified path

### Core Search Method

```python
search(
    query: str = "",
    regex: bool = False,
    case_sensitive: bool = False,
    whole_words: bool = False,
    match_path: bool = False,
    match_diacritics: bool = False,
    max_results: Optional[int] = None,
    offset: int = 0,
    path_filter: Optional[str] = None,
    parent_path: Optional[str] = None,
    parent: Optional[str] = None,
    folders_only: bool = False,
    files_only: bool = False,
    attributes: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_ascending: bool = True,
    include_name: bool = True,
    include_path: bool = False,
    include_full_path: bool = False,
    include_extension: bool = False,
    include_size: bool = False,
    include_date_created: bool = False,
    include_date_modified: bool = False,
    include_date_accessed: bool = False,
    include_attributes: bool = False,
    timeout: int = 5000,
) -> List[Dict[str, Union[str, int]]]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | str | `""` | Search query string |
| `regex` | bool | `False` | Use regular expressions |
| `case_sensitive` | bool | `False` | Match case exactly |
| `whole_words` | bool | `False` | Match whole words only |
| `match_path` | bool | `False` | Match full path and filename |
| `match_diacritics` | bool | `False` | Match diacritical marks |
| `max_results` | Optional[int] | `None` | Maximum results to return |
| `offset` | int | `0` | Starting offset for results |
| `path_filter` | Optional[str] | `None` | Search within specific path |
| `parent_path` | Optional[str] | `None` | Search in parent of specified path |
| `parent` | Optional[str] | `None` | Search for files with specified parent |
| `folders_only` | bool | `False` | Return only folders |
| `files_only` | bool | `False` | Return only files |
| `attributes` | Optional[str] | `None` | DIR style attributes filter |
| `sort_by` | Optional[str] | `None` | Sort field (name, path, size, etc.) |
| `sort_ascending` | bool | `True` | Sort in ascending order |
| `include_name` | bool | `True` | Include name in results |
| `include_path` | bool | `False` | Include path column |
| `include_full_path` | bool | `False` | Include full path and name |
| `include_extension` | bool | `False` | Include file extension |
| `include_size` | bool | `False` | Include file size |
| `include_date_created` | bool | `False` | Include creation date |
| `include_date_modified` | bool | `False` | Include modification date |
| `include_date_accessed` | bool | `False` | Include access date |
| `include_attributes` | bool | `False` | Include file attributes |
| `timeout` | int | `5000` | Timeout in milliseconds |

**Returns:**
- `List[Dict[str, Union[str, int]]]`: List of search results as dictionaries

**Raises:**
- `RuntimeError`: If Everything Search fails or command execution error
- `TimeoutError`: If search exceeds timeout

### Convenience Methods

#### search_files()
```python
search_files(query: str = "", **kwargs) -> List[Dict[str, Union[str, int]]]
```
Search for files only (sets `files_only=True`).

#### search_folders()
```python
search_folders(query: str = "", **kwargs) -> List[Dict[str, Union[str, int]]]
```
Search for folders only (sets `folders_only=True`).

#### search_by_extension()
```python
search_by_extension(extension: str, **kwargs) -> List[Dict[str, Union[str, int]]]
```
Search for files with specific extension.

**Parameters:**
- `extension` (str): File extension without dot (e.g., "py", "txt")

#### search_by_size()
```python
search_by_size(size_filter: str, **kwargs) -> List[Dict[str, Union[str, int]]]
```
Search for files by size.

**Parameters:**
- `size_filter` (str): Size filter expressions:
  - `">100MB"` - Files larger than 100MB
  - `"<1KB"` - Files smaller than 1KB
  - `"1GB..5GB"` - Files between 1GB and 5GB

#### search_recent()
```python
search_recent(days: int = 7, **kwargs) -> List[Dict[str, Union[str, int]]]
```
Search for recently modified files.

**Parameters:**
- `days` (int): Number of days to look back (default: 7)

### Utility Methods

#### get_version()
```python
get_version() -> str
```
Get Everything Search version string.

#### get_result_count()
```python
get_result_count(query: str) -> int
```
Get total number of results for a query without retrieving them.

#### export_results()
```python
export_results(
    query: str, 
    output_file: str, 
    format: str = "csv", 
    **kwargs
)
```
Export search results to file.

**Parameters:**
- `query` (str): Search query
- `output_file` (str): Output file path
- `format` (str): Export format (csv, txt, efu, m3u, m3u8, tsv)

## MCP Server Tools

The MCP server exposes 8 tools for LLM integration:

### 1. search_files
Search for files with comprehensive options.

**Parameters:**
- `query` (str): Search query
- `max_results` (int): Maximum results (default: 20)
- `regex` (bool): Use regex (default: False)
- `case_sensitive` (bool): Case sensitive (default: False)
- `include_size` (bool): Include file size (default: True)
- `include_date_modified` (bool): Include modification date (default: True)
- `sort_by` (str): Sort field (default: "name")
- `timeout` (int): Timeout in ms (default: 30000)

### 2. search_folders
Search for folders only.

**Parameters:**
- `query` (str): Search query
- `max_results` (int): Maximum results (default: 20)
- `regex` (bool): Use regex (default: False)
- `case_sensitive` (bool): Case sensitive (default: False)
- `sort_by` (str): Sort field (default: "name")
- `timeout` (int): Timeout in ms (default: 30000)

### 3. search_by_extension
Search files by extension.

**Parameters:**
- `extension` (str): File extension (e.g., "py", "txt")
- `max_results` (int): Maximum results (default: 20)
- `include_size` (bool): Include file size (default: True)
- `include_date_modified` (bool): Include modification date (default: True)
- `sort_by` (str): Sort field (default: "name")

### 4. search_by_size
Search files by size filter.

**Parameters:**
- `size_filter` (str): Size expression (e.g., ">100MB", "<1KB")
- `max_results` (int): Maximum results (default: 20)
- `include_date_modified` (bool): Include modification date (default: True)
- `sort_by` (str): Sort field (default: "size")
- `sort_ascending` (bool): Sort ascending (default: False)

### 5. search_recent_files
Search recently modified files.

**Parameters:**
- `days` (int): Days to look back (default: 7)
- `max_results` (int): Maximum results (default: 20)
- `include_size` (bool): Include file size (default: True)
- `sort_by` (str): Sort field (default: "date-modified")
- `sort_ascending` (bool): Sort ascending (default: False)

### 6. advanced_search
Full control over all search parameters.

**Parameters:**
- `query` (str): Search query
- `max_results` (int): Maximum results (default: 20)
- `regex` (bool): Use regex (default: False)
- `case_sensitive` (bool): Case sensitive (default: False)
- `whole_words` (bool): Match whole words (default: False)
- `match_path` (bool): Match path (default: False)
- `files_only` (bool): Files only (default: False)
- `folders_only` (bool): Folders only (default: False)
- `path_filter` (Optional[str]): Path filter
- `include_size` (bool): Include size (default: True)
- `include_extension` (bool): Include extension (default: True)
- `include_date_modified` (bool): Include mod date (default: True)
- `sort_by` (str): Sort field (default: "name")
- `sort_ascending` (bool): Sort ascending (default: True)
- `timeout` (int): Timeout in ms (default: 30000)

### 7. get_result_count
Get result count without fetching results.

**Parameters:**
- `query` (str): Search query

### 8. get_everything_version
Get Everything Search version.

**Returns:**
- JSON with version information

## Response Format

All MCP tools return JSON strings with the following structure:

### Success Response
```json
[
  {
    "Name": "filename.txt",
    "Full Path & Name": "C:\\path\\to\\filename.txt",
    "Size": 1024,
    "Date Modified": "2024-01-01 12:00:00",
    "Extension": "txt"
  }
]
```

### Error Response
```json
{
  "error": "Error message description"
}
```

## Query Syntax Examples

### Basic Searches
```python
# Find all Python files
es.search("*.py")

# Find files containing "config"
es.search("config")

# Case-sensitive search
es.search("Config", case_sensitive=True)
```

### Advanced Queries
```python
# Files larger than 100MB
es.search("size:>100MB")

# Files modified in last 7 days
es.search("datemodified:last7days")

# Files in specific path
es.search("*.log", path_filter="C:\\logs")

# Regular expression search
es.search(r"test_\d+\.py$", regex=True)
```

### Size Filters
- `>100MB` - Larger than 100MB
- `<1KB` - Smaller than 1KB  
- `1GB..5GB` - Between 1GB and 5GB
- `empty` - Empty files (0 bytes)
- `huge` - Files larger than 1GB

### Date Filters
- `today` - Modified today
- `yesterday` - Modified yesterday
- `thisweek` - Modified this week
- `lastweek` - Modified last week
- `thismonth` - Modified this month
- `last7days` - Modified in last 7 days
- `2024` - Modified in 2024
- `january` - Modified in January

## Error Handling

### Common Exceptions

#### FileNotFoundError
```python
try:
    es = EverythingSearch("/invalid/path/es.exe")
except FileNotFoundError as e:
    print(f"Everything Search not found: {e}")
```

#### RuntimeError
```python
try:
    results = es.search("invalid_query")
except RuntimeError as e:
    print(f"Search failed: {e}")
```

#### TimeoutError
```python
try:
    results = es.search("*", timeout=1000)  # 1 second timeout
except TimeoutError as e:
    print(f"Search timed out: {e}")
```

## Performance Considerations

### Optimization Tips

1. **Use max_results** to limit large result sets:
   ```python
   results = es.search("*", max_results=100)
   ```

2. **Check result count** before fetching:
   ```python
   count = es.get_result_count("*.mp4")
   if count > 1000:
       print(f"Warning: {count} results found")
   ```

3. **Use path filters** for focused searches:
   ```python
   results = es.search("*.py", path_filter="C:\\projects")
   ```

4. **Increase timeout** for large directories:
   ```python
   results = es.search("*", timeout=60000)  # 60 seconds
   ```

### Memory Management

- Large result sets consume memory proportional to result count
- Use pagination with `offset` and `max_results` for large datasets
- Consider exporting to file for very large result sets

## Thread Safety

The EverythingSearch class is **not thread-safe**. Create separate instances for concurrent use:

```python
import threading
from everything_search import EverythingSearch

def search_worker(query):
    es = EverythingSearch()  # Separate instance per thread
    return es.search(query)

threads = []
for query in ["*.py", "*.txt", "*.log"]:
    thread = threading.Thread(target=search_worker, args=(query,))
    threads.append(thread)
    thread.start()
```

## Integration Examples

### With Pandas
```python
import pandas as pd
from everything_search import EverythingSearch

es = EverythingSearch()
results = es.search("*.csv", include_size=True, include_date_modified=True)
df = pd.DataFrame(results)
print(df.head())
```

### With Path Objects
```python
from pathlib import Path
from everything_search import EverythingSearch

es = EverythingSearch()
results = es.search("*.py", include_full_path=True)

for result in results:
    path = Path(result["Full Path & Name"])
    print(f"File: {path.name}, Size: {path.stat().st_size} bytes")
```

### Async Usage Pattern
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from everything_search import EverythingSearch

async def async_search(query):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        es = EverythingSearch()
        return await loop.run_in_executor(executor, es.search, query)

# Usage
results = await async_search("*.py")
```