# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### 1. "Everything Search executable not found"

**Symptoms:**
```
FileNotFoundError: Everything Search executable not found at: /mnt/c/Program Files/Everything/es.exe
```

**Solutions:**

1. **Check Everything Search Installation**
   ```python
   import os
   
   # Common paths to check
   paths = [
       "/mnt/c/Program Files/Everything/es.exe",       # WSL 64-bit
       "/mnt/c/Program Files (x86)/Everything/es.exe", # WSL 32-bit
       "C:\\Program Files\\Everything\\es.exe",        # Windows 64-bit
       "C:\\Program Files (x86)\\Everything\\es.exe",  # Windows 32-bit
   ]
   
   for path in paths:
       if os.path.exists(path):
           print(f"Found Everything at: {path}")
           break
   else:
       print("Everything Search not found. Please install from voidtools.com")
   ```

2. **Manual Path Specification**
   ```python
   from everything_search import EverythingSearch
   
   # Specify custom path
   es = EverythingSearch("/custom/path/to/es.exe")
   ```

3. **Install Everything Search**
   - Download from [voidtools.com](https://www.voidtools.com/)
   - Install with default settings
   - Ensure Everything service is running

#### 2. Permission Denied Errors

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. **Run Everything as Administrator** (Windows)
   - Right-click Everything Search
   - Select "Run as administrator"
   - Allow initial indexing to complete

2. **Check WSL Mount Permissions**
   ```bash
   # Check mount point
   ls -la "/mnt/c/Program Files/Everything/"
   
   # If permission denied, remount with proper permissions
   sudo umount /mnt/c
   sudo mount -t drvfs C: /mnt/c -o metadata,uid=1000,gid=1000
   ```

#### 3. Python Version Compatibility

**Symptoms:**
```
ERROR: Package 'everything-search-py' requires a different Python: 3.9.0 not in '>=3.10'
```

**Solutions:**

1. **Check Python Version**
   ```bash
   python --version
   # Should be 3.10 or higher
   ```

2. **Install Compatible Python**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.11 python3.11-pip
   
   # Use specific version
   python3.11 -m pip install everything-search-py
   ```

### Search Issues

#### 1. No Results Found

**Symptoms:**
- Search returns empty list
- Expected files are not found

**Diagnosis:**
```python
from everything_search import EverythingSearch

es = EverythingSearch()

# Test basic functionality
try:
    version = es.get_version()
    print(f"Everything version: {version}")
    
    # Test with broad search
    all_files = es.search("", max_results=5)
    if all_files:
        print("Everything is working")
        print("Sample files:")
        for f in all_files:
            print(f"  {f.get('Name', 'Unknown')}")
    else:
        print("No files returned - check indexing")
        
except Exception as e:
    print(f"Error: {e}")
```

**Solutions:**

1. **Check Everything Indexing**
   - Open Everything GUI
   - Verify files are visible
   - Wait for indexing to complete
   - Check if drives are included in index

2. **Verify Search Syntax**
   ```python
   # Correct patterns
   es.search("*.py")        # Extension search
   es.search("filename")    # Name search
   es.search("path:C:\\")   # Path search
   
   # Incorrect patterns (may not work as expected)
   es.search(".py")         # Missing asterisk
   es.search("C:\\*.py")    # Use path_filter instead
   ```

3. **Use Path Filters**
   ```python
   # Instead of including path in query
   results = es.search("*.py", path_filter="C:\\projects")
   
   # Check specific directory
   results = es.search("", path_filter="C:\\Users", max_results=5)
   ```

#### 2. Search Timeouts

**Symptoms:**
```
TimeoutError: Search timed out after 5000ms
```

**Solutions:**

1. **Increase Timeout**
   ```python
   # For large file systems
   results = es.search("*", timeout=60000)  # 60 seconds
   
   # For network drives
   results = es.search("*.mp4", timeout=120000)  # 2 minutes
   ```

2. **Use Result Count Check**
   ```python
   # Check before searching
   count = es.get_result_count("*")
   if count > 100000:
       print(f"Large result set: {count} files")
       # Use more specific search or limit results
       results = es.search("*", max_results=1000, timeout=30000)
   ```

3. **Optimize Search Query**
   ```python
   # Instead of broad search
   # results = es.search("*")  # Very slow
   
   # Use specific filters
   results = es.search("*.py", path_filter="C:\\current_project")
   results = es.search_recent(days=7)
   results = es.search_by_size(">100MB", max_results=50)
   ```

#### 3. UTF-8 Encoding Issues

**Status:** Fixed in v0.1.0+

**Previous Symptoms:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 1234
```

**Current Behavior:**
- Automatically handles special characters
- Uses `errors="replace"` for robust decoding
- Files with special characters are properly displayed

**Verification:**
```python
# Test with files containing special characters
results = es.search("español OR café OR naïve", max_results=10)
for file in results:
    print(f"Found: {file['Name']}")  # Should work without errors
```

### MCP Server Issues

#### 1. MCP Server Not Connecting

**Symptoms:**
- Claude Desktop shows "MCP server failed to start"
- No Everything Search tools available

**Diagnosis:**
```bash
# Test MCP server manually
cd /path/to/everything-search-py
python start_mcp_server.py
# Should start without errors
```

**Solutions:**

1. **Check Configuration File**
   ```json
   {
     "mcpServers": {
       "everything-search": {
         "command": "python",
         "args": ["C:\\Users\\YOUR_USERNAME\\everything-search-py\\start_mcp_server.py"],
         "env": {}
       }
     }
   }
   ```

2. **Verify File Paths**
   ```bash
   # Check if file exists
   ls "C:\\Users\\YOUR_USERNAME\\everything-search-py\\start_mcp_server.py"
   
   # Check if Python can execute it
   python "C:\\Users\\YOUR_USERNAME\\everything-search-py\\start_mcp_server.py"
   ```

3. **Check Python Environment**
   ```bash
   # Verify MCP dependencies
   python -c "import mcp; print('MCP available')"
   python -c "from everything_search import EverythingSearch; print('ES available')"
   ```

4. **Update Claude Desktop Config Path**
   ```json
   {
     "mcpServers": {
       "everything-search": {
         "command": "python",
         "args": ["C:\\Full\\Absolute\\Path\\To\\start_mcp_server.py"]
       }
     }
   }
   ```

#### 2. MCP Tools Return Errors

**Symptoms:**
- Tools execute but return error messages
- JSON responses contain "error" field

**Diagnosis:**
```python
# Test MCP tools directly
from mcp_server import search_files, get_everything_version

# Test basic functionality
version_result = get_everything_version()
print(f"Version result: {version_result}")

# Test search
search_result = search_files("*.py", max_results=5)
print(f"Search result: {search_result}")
```

**Solutions:**

1. **Check Everything Search Status**
   - Ensure Everything is running
   - Verify indexing is complete
   - Test with Everything GUI first

2. **Increase MCP Timeouts**
   ```python
   # In MCP tool calls, use longer timeouts
   result = search_files("*", timeout=60000)  # 60 seconds
   ```

### Performance Issues

#### 1. Slow Search Performance

**Symptoms:**
- Searches take longer than expected
- High memory usage
- System becomes unresponsive

**Solutions:**

1. **Optimize Search Queries**
   ```python
   # Instead of
   # results = es.search("*")  # Searches everything
   
   # Use specific filters
   results = es.search("*.py", path_filter="C:\\projects")
   results = es.search_recent(days=7)
   results = es.search_by_extension("mp4", max_results=100)
   ```

2. **Use Result Limits**
   ```python
   # Always limit results for UI applications
   results = es.search("*.mp4", max_results=50)
   
   # For analysis, paginate
   def paginated_search(query, page_size=100):
       offset = 0
       while True:
           batch = es.search(query, offset=offset, max_results=page_size)
           if not batch:
               break
           yield batch
           offset += page_size
   ```

3. **Check System Resources**
   - Ensure sufficient RAM
   - Check disk I/O performance
   - Monitor CPU usage during searches

#### 2. Memory Issues

**Symptoms:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

1. **Process Results in Batches**
   ```python
   def process_large_search(query):
       total = es.get_result_count(query)
       batch_size = 1000
       
       for offset in range(0, total, batch_size):
           batch = es.search(
               query,
               offset=offset,
               max_results=batch_size
           )
           
           # Process batch immediately
           for file in batch:
               process_file(file)  # Your processing logic
           
           # Don't accumulate results
           del batch
   ```

2. **Use Export for Large Datasets**
   ```python
   # Instead of loading all results into memory
   es.export_results("*.mp4", "large_videos.csv", format="csv")
   
   # Then process file
   import pandas as pd
   df = pd.read_csv("large_videos.csv", chunksize=1000)
   for chunk in df:
       process_chunk(chunk)
   ```

### Platform-Specific Issues

#### WSL Issues

1. **Mount Point Problems**
   ```bash
   # If /mnt/c doesn't exist or is inaccessible
   sudo mkdir -p /mnt/c
   sudo mount -t drvfs C: /mnt/c
   
   # For permanent mounting, add to /etc/fstab
   echo "C: /mnt/c drvfs defaults 0 0" | sudo tee -a /etc/fstab
   ```

2. **Path Format Issues**
   ```python
   # Use forward slashes in WSL
   es = EverythingSearch("/mnt/c/Program Files/Everything/es.exe")
   
   # Not backslashes
   # es = EverythingSearch("\\mnt\\c\\Program Files\\Everything\\es.exe")
   ```

#### Windows Issues

1. **Spaces in Paths**
   ```python
   # Paths with spaces work automatically
   es = EverythingSearch("C:\\Program Files\\Everything\\es.exe")
   
   # Or use raw strings
   es = EverythingSearch(r"C:\Program Files\Everything\es.exe")
   ```

2. **Long Path Names**
   ```python
   # For very long paths, use extended syntax
   import os
   es_path = os.path.expanduser("~\\AppData\\Local\\Programs\\Everything\\es.exe")
   es = EverythingSearch(es_path)
   ```

## Debug Mode

### Enable Detailed Logging

```python
import logging
import subprocess

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

from everything_search import EverythingSearch

# Create instance
es = EverythingSearch()

# Debug search will show exact command
results = es.search("*.py", max_results=5)
```

### Manual Command Testing

```bash
# Test Everything Search directly
"/mnt/c/Program Files/Everything/es.exe" -version

# Test basic search
"/mnt/c/Program Files/Everything/es.exe" "*.py" -max-results 5 -csv

# Test with specific options
"/mnt/c/Program Files/Everything/es.exe" "*.py" -path "C:\\projects" -csv -timeout 30000
```

### Trace Network Issues

```python
import time
from everything_search import EverythingSearch

def trace_search_performance():
    es = EverythingSearch()
    
    queries = ["*.py", "*.txt", "*.mp4"]
    
    for query in queries:
        start_time = time.time()
        try:
            results = es.search(query, max_results=10)
            duration = time.time() - start_time
            print(f"{query}: {len(results)} results in {duration:.2f}s")
        except Exception as e:
            duration = time.time() - start_time
            print(f"{query}: ERROR after {duration:.2f}s - {e}")

trace_search_performance()
```

## Getting Additional Help

### Information to Provide

When reporting issues, include:

1. **System Information**
   ```python
   import platform
   import sys
   from everything_search import EverythingSearch
   
   print(f"Python: {sys.version}")
   print(f"Platform: {platform.platform()}")
   print(f"Architecture: {platform.architecture()}")
   
   try:
       es = EverythingSearch()
       print(f"Everything version: {es.get_version()}")
   except Exception as e:
       print(f"Everything error: {e}")
   ```

2. **Error Details**
   - Complete error message
   - Steps to reproduce
   - Expected vs actual behavior

3. **Configuration**
   - Installation method (pip, Poetry, source)
   - File paths used
   - Search queries that fail

### Support Channels

1. **GitHub Issues**: [github.com/pakkio/es/issues](https://github.com/pakkio/es/issues)
2. **GitHub Discussions**: [github.com/pakkio/es/discussions](https://github.com/pakkio/es/discussions)
3. **Documentation**: Review all guides and API docs

### Before Reporting

1. **Update to Latest Version**
   ```bash
   pip install --upgrade everything-search-py
   ```

2. **Test with Minimal Example**
   ```python
   from everything_search import EverythingSearch
   es = EverythingSearch()
   print(es.get_version())
   ```

3. **Check Everything Search Directly**
   - Test searches in Everything GUI
   - Verify files exist and are indexed
   - Check Everything Search logs

Remember: Most issues are configuration-related and can be resolved by carefully following the installation guide and checking file paths.