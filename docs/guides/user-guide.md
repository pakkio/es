# User Guide

## Quick Start

### Basic Usage

```python
from everything_search import EverythingSearch

# Initialize the wrapper
es = EverythingSearch()

# Simple search
results = es.search("*.py")
print(f"Found {len(results)} Python files")

# Display results
for file in results[:5]:  # Show first 5 results
    print(f"- {file['Name']}")
```

### Your First Search

```python
from everything_search import EverythingSearch

es = EverythingSearch()

# Search for text files
text_files = es.search("*.txt", max_results=10, include_size=True)

for file in text_files:
    name = file.get('Name', 'Unknown')
    size = file.get('Size', 0)
    print(f"{name} ({size} bytes)")
```

## Common Search Patterns

### File Type Searches

```python
# Find all images
images = es.search("*.jpg *.png *.gif")

# Find documents  
docs = es.search("*.pdf *.docx *.txt")

# Find code files
code = es.search("*.py *.js *.html *.css")

# Use extension method
python_files = es.search_by_extension("py", max_results=20)
```

### Size-Based Searches

```python
# Large files (over 100MB)
large_files = es.search_by_size(">100MB", max_results=10)

# Small files (under 1KB)
small_files = es.search_by_size("<1KB")

# Files in specific size range
medium_files = es.search_by_size("1MB..10MB")

# Empty files
empty_files = es.search_by_size("empty")
```

### Date-Based Searches

```python
# Recently modified files (last 7 days)
recent = es.search_recent(days=7)

# Today's files
today = es.search("datemodified:today")

# This week's files
this_week = es.search("datemodified:thisweek")

# Files from specific year
files_2024 = es.search("datemodified:2024")
```

### Path-Specific Searches

```python
# Search in specific directory
project_files = es.search("*.py", path_filter="C:\\projects")

# Search multiple directories
docs = es.search("*.md", path_filter="C:\\docs;D:\\documentation")

# Find files in Downloads folder
downloads = es.search("path:downloads")
```

## Advanced Search Techniques

### Regular Expressions

```python
# Enable regex mode
test_files = es.search(r"test_\d+\.py$", regex=True)

# Match patterns
log_files = es.search(r"log_\d{4}-\d{2}-\d{2}\.txt", regex=True)

# Find versioned files
versioned = es.search(r"v\d+\.\d+\.\d+", regex=True)
```

### Complex Queries

```python
# Case-sensitive search
config_files = es.search("Config", case_sensitive=True)

# Whole words only
readme_files = es.search("readme", whole_words=True)

# Match in full path
system_files = es.search("system", match_path=True)

# Combine options
results = es.search(
    "test",
    case_sensitive=True,
    whole_words=True,
    files_only=True,
    include_size=True,
    sort_by="size",
    sort_ascending=False
)
```

### Filtering Results

```python
# Files only
files = es.search_files("config")

# Folders only  
folders = es.search_folders("project")

# With detailed information
detailed = es.search(
    "*.log",
    include_full_path=True,
    include_size=True,
    include_date_modified=True,
    include_extension=True
)

# Sort by size (largest first)
large_logs = es.search(
    "*.log",
    include_size=True,
    sort_by="size",
    sort_ascending=False,
    max_results=10
)
```

## Working with Results

### Result Structure

```python
results = es.search("*.py", include_size=True, include_date_modified=True)

# Each result is a dictionary
for result in results[:3]:
    print("Result fields:", result.keys())
    print("Name:", result.get('Name'))
    print("Size:", result.get('Size'))
    print("Date Modified:", result.get('Date Modified'))
    print("---")
```

### Processing Results

```python
import os
from pathlib import Path

results = es.search("*.py", include_full_path=True, include_size=True)

# Convert to Path objects
paths = [Path(r['Full Path & Name']) for r in results if 'Full Path & Name' in r]

# Calculate total size
total_size = sum(r.get('Size', 0) for r in results)
print(f"Total size: {total_size:,} bytes")

# Group by directory
from collections import defaultdict
by_dir = defaultdict(list)
for result in results:
    if 'Full Path & Name' in result:
        dir_path = os.path.dirname(result['Full Path & Name'])
        by_dir[dir_path].append(result)

print(f"Files found in {len(by_dir)} directories")
```

### Pagination

```python
# Get total count first
total = es.get_result_count("*.mp4")
print(f"Total MP4 files: {total}")

# Paginate through results
page_size = 50
for page in range(0, min(total, 500), page_size):  # Limit to 500 total
    batch = es.search(
        "*.mp4",
        offset=page,
        max_results=page_size,
        include_size=True
    )
    print(f"Page {page//page_size + 1}: {len(batch)} files")
    
    # Process batch
    for file in batch:
        print(f"  {file['Name']} - {file.get('Size', 0)} bytes")
```

## Data Export

### Export to Files

```python
# Export to CSV
es.export_results("*.py", "python_files.csv", format="csv")

# Export to text
es.export_results("*.log", "log_files.txt", format="txt")

# Export with filters
es.export_results(
    "*.mp4", 
    "large_videos.csv", 
    format="csv",
    max_results=100
)
```

### Export to DataFrames

```python
import pandas as pd

# Search and convert to DataFrame
results = es.search(
    "*.csv",
    include_size=True,
    include_date_modified=True,
    include_full_path=True
)

df = pd.DataFrame(results)
print(df.head())

# Save to Excel
df.to_excel("csv_files_inventory.xlsx", index=False)

# Basic statistics
print(f"Total CSV files: {len(df)}")
print(f"Total size: {df['Size'].sum():,} bytes")
print(f"Average size: {df['Size'].mean():.1f} bytes")
```

## File Management Tasks

### Find Duplicates by Name

```python
from collections import Counter

# Get all files with sizes
results = es.search("", files_only=True, include_size=True, max_results=10000)

# Count by filename
name_counts = Counter(r['Name'] for r in results)
duplicates = {name: count for name, count in name_counts.items() if count > 1}

print(f"Found {len(duplicates)} duplicate filenames")
for name, count in sorted(duplicates.items()):
    print(f"  {name}: {count} copies")
```

### Find Large Files

```python
# Find files over 1GB
large_files = es.search_by_size(">1GB", max_results=20)

# Sort by size
large_files.sort(key=lambda x: x.get('Size', 0), reverse=True)

print("Largest files:")
for file in large_files:
    size_gb = file.get('Size', 0) / (1024**3)
    print(f"  {file['Name']}: {size_gb:.2f} GB")
```

### Clean Up Temp Files

```python
# Find temporary files
temp_patterns = ["*.tmp", "*.temp", "*~", "*.bak"]
temp_files = []

for pattern in temp_patterns:
    temp_files.extend(es.search(pattern, include_size=True))

# Calculate total size
total_temp_size = sum(f.get('Size', 0) for f in temp_files)
print(f"Found {len(temp_files)} temp files using {total_temp_size:,} bytes")

# List by type
from collections import defaultdict
by_extension = defaultdict(list)
for file in temp_files:
    ext = os.path.splitext(file['Name'])[1].lower()
    by_extension[ext].append(file)

for ext, files in by_extension.items():
    total_size = sum(f.get('Size', 0) for f in files)
    print(f"  {ext}: {len(files)} files, {total_size:,} bytes")
```

## Integration Examples

### With File Operations

```python
import shutil
from pathlib import Path

# Find and copy Python files to backup directory
python_files = es.search("*.py", path_filter="C:\\projects", include_full_path=True)

backup_dir = Path("backup")
backup_dir.mkdir(exist_ok=True)

for file_info in python_files[:10]:  # Limit to 10 files
    if 'Full Path & Name' in file_info:
        source = Path(file_info['Full Path & Name'])
        if source.exists():
            dest = backup_dir / source.name
            shutil.copy2(source, dest)
            print(f"Copied: {source.name}")
```

### With Git Operations

```python
import subprocess
from pathlib import Path

# Find all Git repositories
git_dirs = es.search_folders(".git", max_results=50)

print("Git repositories found:")
for repo in git_dirs:
    if 'Full Path & Name' in repo:
        repo_path = Path(repo['Full Path & Name']).parent
        print(f"  {repo_path}")
        
        # Get Git status (optional)
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip():
                print(f"    (has uncommitted changes)")
        except:
            pass
```

### With Media Files

```python
# Find and organize media files
media_extensions = ["mp4", "avi", "mkv", "mp3", "flac", "jpg", "png"]
media_files = {}

for ext in media_extensions:
    files = es.search_by_extension(ext, include_size=True, max_results=100)
    if files:
        media_files[ext] = files

# Summary by type
print("Media files summary:")
for ext, files in media_files.items():
    total_size = sum(f.get('Size', 0) for f in files)
    size_gb = total_size / (1024**3)
    print(f"  {ext.upper()}: {len(files)} files, {size_gb:.2f} GB")

# Find largest media files
all_media = []
for files in media_files.values():
    all_media.extend(files)

all_media.sort(key=lambda x: x.get('Size', 0), reverse=True)

print("\\nLargest media files:")
for file in all_media[:10]:
    size_mb = file.get('Size', 0) / (1024**2)
    print(f"  {file['Name']}: {size_mb:.1f} MB")
```

## Performance Tips

### Optimize Search Speed

```python
# Use specific paths instead of global search
fast_search = es.search("*.py", path_filter="C:\\current_project")

# Check count before retrieving all results
count = es.get_result_count("*")
if count > 10000:
    print(f"Large result set ({count} files), limiting to 1000")
    results = es.search("*", max_results=1000)

# Use appropriate timeouts
results = es.search("*", timeout=30000)  # 30 seconds for large searches
```

### Memory Management

```python
# Process results in batches
def process_large_search(query, batch_size=100):
    total = es.get_result_count(query)
    processed = 0
    
    for offset in range(0, total, batch_size):
        batch = es.search(
            query,
            offset=offset,
            max_results=batch_size,
            include_size=True
        )
        
        # Process batch
        yield batch
        processed += len(batch)
        print(f"Processed {processed}/{total} files")

# Usage
for batch in process_large_search("*.mp4"):
    # Process each batch
    for file in batch:
        # Do something with file
        pass
```

### Error Handling

```python
def safe_search(query, **kwargs):
    """Perform search with error handling."""
    try:
        return es.search(query, **kwargs)
    except TimeoutError:
        print(f"Search timed out for query: {query}")
        # Try with smaller result set
        return es.search(query, max_results=100, **kwargs)
    except RuntimeError as e:
        print(f"Search failed: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# Usage
results = safe_search("*.log", timeout=60000)
```

## Troubleshooting Common Issues

### Search Returns No Results

```python
# Debug search query
query = "*.py"
print(f"Searching for: {query}")

# Check if Everything is indexing
version = es.get_version()
print(f"Everything version: {version}")

# Try broader search
all_files = es.search("", max_results=5)
if all_files:
    print("Everything is working, try different query")
else:
    print("Everything may not be running or indexed")
```

### Handle Special Characters

```python
# Search for files with special characters
results = es.search("español", case_sensitive=False)

# The wrapper automatically handles UTF-8 encoding issues
for file in results:
    print(f"Found: {file['Name']}")
```

### Large Result Sets

```python
# Handle large result sets efficiently
query = "*"
count = es.get_result_count(query)

if count > 50000:
    print(f"Very large result set: {count} files")
    print("Consider using filters:")
    
    # Suggest filters
    recent_count = es.get_result_count("datemodified:thisweek")
    print(f"  This week: {recent_count} files")
    
    large_count = es.get_result_count("size:>100MB")
    print(f"  Large files (>100MB): {large_count} files")
```

## Next Steps

- **Explore [MCP Integration](mcp-integration.md)** for Claude Desktop
- **Check [API Reference](../api/README.md)** for detailed documentation
- **See [Examples Repository](examples.md)** for more use cases
- **Read [Troubleshooting Guide](troubleshooting.md)** for common issues