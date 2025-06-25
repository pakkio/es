# Installation Guide

## Overview

Everything Search Python wrapper provides two installation methods:

1. **Standard Installation** - For using the Python wrapper only
2. **MCP Server Installation** - For LLM integration with Claude Desktop

## Prerequisites

### System Requirements

- **Windows**: Everything Search application installed and running
- **WSL/Linux**: Access to Windows filesystem with Everything Search
- **Python**: 3.10 or higher
- **Memory**: Minimal (searches are processed by Everything, not Python)

### Everything Search Setup

1. **Download Everything Search**
   - Visit [voidtools.com](https://www.voidtools.com/)
   - Download the installer (free)
   - Install with default settings

2. **Verify Installation**
   - Launch Everything Search
   - Let it complete initial indexing (may take a few minutes)
   - Test search functionality in the GUI

3. **Command Line Access**
   - Everything Search automatically installs `es.exe` in:
     - Windows: `C:\Program Files\Everything\es.exe`
     - WSL: `/mnt/c/Program Files/Everything/es.exe`

## Standard Installation

### Method 1: pip (Recommended)

```bash
pip install everything-search-py
```

### Method 2: From Source

1. **Clone Repository**
   ```bash
   git clone https://github.com/pakkio/es.git
   cd es
   ```

2. **Install with Poetry**
   ```bash
   poetry install
   ```

3. **Install with pip**
   ```bash
   pip install -e .
   ```

### Verify Installation

```python
from everything_search import EverythingSearch

# Test basic functionality
es = EverythingSearch()
print(f"Everything Search version: {es.get_version()}")

# Test search
results = es.search("*.txt", max_results=5)
print(f"Found {len(results)} text files")
```

## MCP Server Installation

### For Claude Desktop Integration

The MCP (Model Context Protocol) server allows Claude Desktop to search your files directly.

#### Step 1: Install Dependencies

```bash
pip install everything-search-py mcp
```

#### Step 2: Copy Files to Windows

**From WSL/Linux:**
```bash
# Create Windows directory
mkdir -p "/mnt/c/Users/$USER/everything-search-py"

# Copy project files
cp -r . "/mnt/c/Users/$USER/everything-search-py/"
```

**From Windows:**
```cmd
REM Clone to Windows filesystem
git clone https://github.com/pakkio/es.git C:\Users\%USERNAME%\everything-search-py
cd C:\Users\%USERNAME%\everything-search-py
pip install -e .
```

#### Step 3: Configure Claude Desktop

1. **Locate Claude Desktop Config**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Path example: `C:\Users\YourName\AppData\Roaming\Claude\claude_desktop_config.json`

2. **Add MCP Server Configuration**
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

3. **Update Path**
   - Replace `YOUR_USERNAME` with your actual Windows username
   - Ensure the path points to your installation directory

#### Step 4: Test MCP Server

1. **Manual Test**
   ```bash
   cd /path/to/everything-search-py
   python start_mcp_server.py
   ```
   
2. **Test in Claude Desktop**
   - Restart Claude Desktop
   - Start a new conversation
   - Try: "Search for Python files in my system"

## Platform-Specific Setup

### Windows

```python
from everything_search import EverythingSearch

# Use default Windows path
es = EverythingSearch()

# Or specify custom path
es = EverythingSearch(r"C:\Program Files\Everything\es.exe")
```

### WSL (Windows Subsystem for Linux)

```python
from everything_search import EverythingSearch

# Default WSL path (automatically detected)
es = EverythingSearch()

# Or specify WSL path explicitly
es = EverythingSearch("/mnt/c/Program Files/Everything/es.exe")
```

### Linux with Wine

```python
from everything_search import EverythingSearch

# Custom path for Wine installation
es = EverythingSearch("/home/user/.wine/drive_c/Program Files/Everything/es.exe")
```

## Troubleshooting

### Common Issues

#### 1. "Everything Search executable not found"

**Solution:**
```python
import os
from everything_search import EverythingSearch

# Check if Everything is installed
paths_to_check = [
    "/mnt/c/Program Files/Everything/es.exe",  # WSL
    "C:\\Program Files\\Everything\\es.exe",   # Windows
    "/mnt/c/Program Files (x86)/Everything/es.exe"  # 32-bit
]

for path in paths_to_check:
    if os.path.exists(path):
        print(f"Found Everything at: {path}")
        es = EverythingSearch(path)
        break
```

#### 2. "UTF-8 decoding errors"

**Status:** Fixed in v0.1.0+
- The wrapper now handles special characters automatically
- Uses `errors="replace"` for robust encoding

#### 3. Search timeouts

**Solutions:**
```python
# Increase timeout for large searches
results = es.search("*", timeout=60000)  # 60 seconds

# Use result count first
count = es.get_result_count("*")
if count > 10000:
    print(f"Large result set: {count} files")
    results = es.search("*", max_results=1000)
```

#### 4. MCP Server not connecting

**Check Configuration:**
1. Verify file paths in Claude Desktop config
2. Ensure Python can execute the server script
3. Check Everything Search is running
4. Restart Claude Desktop after config changes

**Test MCP Server:**
```bash
python test_mcp.py
```

#### 5. Permission errors

**Windows:**
- Run Everything Search as Administrator once
- Ensure indexing is complete

**WSL:**
- Verify mount point access: `ls "/mnt/c/Program Files/Everything/"`
- Check file permissions

### Performance Optimization

#### For Large File Systems

1. **Use Path Filters**
   ```python
   # Search specific directories
   results = es.search("*.py", path_filter="C:\\projects")
   ```

2. **Limit Results**
   ```python
   # Prevent memory issues
   results = es.search("*", max_results=1000)
   ```

3. **Check Count First**
   ```python
   count = es.get_result_count("*.mp4")
   if count > 5000:
       print("Too many results, refining search...")
   ```

#### For MCP Server

1. **Adjust Timeouts**
   - Default: 30 seconds
   - Large directories: 60+ seconds
   - Network drives: 120+ seconds

2. **Configure Result Limits**
   - Default: 20 results per MCP call
   - Increase for comprehensive searches
   - Decrease for faster responses

## Development Setup

### For Contributors

1. **Clone and Setup**
   ```bash
   git clone https://github.com/pakkio/es.git
   cd es
   poetry install --with dev
   ```

2. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

3. **Run Tests**
   ```bash
   # Unit tests
   pytest
   
   # Coverage report
   pytest --cov=everything_search --cov-report=html
   
   # Test with real Everything Search
   python test_fixed_search.py
   ```

4. **Code Quality**
   ```bash
   # Format code
   black .
   isort .
   
   # Type checking
   mypy everything_search.py
   
   # Linting
   flake8
   ```

## Environment Variables

### Optional Configuration

```bash
# Custom Everything Search path
export EVERYTHING_SEARCH_PATH="/custom/path/to/es.exe"

# Default timeout (milliseconds)
export EVERYTHING_SEARCH_TIMEOUT="30000"

# Default max results
export EVERYTHING_SEARCH_MAX_RESULTS="100"
```

### Usage in Code

```python
import os
from everything_search import EverythingSearch

# Use environment variable if set
es_path = os.getenv("EVERYTHING_SEARCH_PATH", "/mnt/c/Program Files/Everything/es.exe")
es = EverythingSearch(es_path)

# Use environment timeout
timeout = int(os.getenv("EVERYTHING_SEARCH_TIMEOUT", "5000"))
results = es.search("*.py", timeout=timeout)
```

## Next Steps

After installation:

1. **Read the [User Guide](user-guide.md)** for usage examples
2. **Check the [API Documentation](../api/README.md)** for detailed reference
3. **See [Integration Examples](examples.md)** for common use cases
4. **Visit [Troubleshooting](troubleshooting.md)** if you encounter issues

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/pakkio/es/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pakkio/es/discussions)
- **Documentation**: [Full Documentation](../README.md)
- **Everything Search**: [Official Documentation](https://www.voidtools.com/support/everything/)