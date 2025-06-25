# Examples and Use Cases

## Table of Contents
1. [Basic Usage Examples](#basic-usage-examples)
2. [File Management](#file-management)
3. [Development Workflows](#development-workflows)
4. [Data Analysis](#data-analysis)
5. [Media Management](#media-management)
6. [System Administration](#system-administration)
7. [Integration Examples](#integration-examples)
8. [Advanced Patterns](#advanced-patterns)

## Basic Usage Examples

### Simple File Search

```python
from everything_search import EverythingSearch

es = EverythingSearch()

# Find Python files
python_files = es.search("*.py", max_results=10)
print(f"Found {len(python_files)} Python files:")
for file in python_files:
    print(f"  {file['Name']}")
```

### Search with Details

```python
# Get detailed file information
detailed_search = es.search(
    "*.log",
    include_size=True,
    include_date_modified=True,
    include_full_path=True,
    max_results=5
)

for file in detailed_search:
    name = file.get('Name', 'Unknown')
    size = file.get('Size', 0)
    path = file.get('Full Path & Name', 'Unknown')
    date = file.get('Date Modified', 'Unknown')
    
    print(f"File: {name}")
    print(f"  Size: {size:,} bytes")
    print(f"  Path: {path}")
    print(f"  Modified: {date}")
    print("---")
```

### Different Search Methods

```python
# By extension
python_files = es.search_by_extension("py", max_results=20)

# By size
large_files = es.search_by_size(">100MB", max_results=10)

# Recent files
recent_files = es.search_recent(days=3, max_results=15)

# Files only
files_only = es.search_files("config", max_results=10)

# Folders only
folders_only = es.search_folders("project", max_results=5)
```

## File Management

### Find Duplicate Files by Name

```python
from collections import Counter, defaultdict
import os

def find_duplicate_names(path_filter=None):
    """Find files with duplicate names across the system."""
    
    # Search for all files
    search_params = {
        'files_only': True,
        'include_size': True,
        'include_full_path': True,
        'max_results': 50000  # Adjust based on your system
    }
    
    if path_filter:
        search_params['path_filter'] = path_filter
    
    files = es.search("", **search_params)
    
    # Group by filename
    by_name = defaultdict(list)
    for file in files:
        name = file.get('Name', '')
        if name:
            by_name[name].append(file)
    
    # Find duplicates
    duplicates = {name: files for name, files in by_name.items() if len(files) > 1}
    
    print(f"Found {len(duplicates)} duplicate filenames:")
    for name, file_list in sorted(duplicates.items()):
        print(f"\n{name} ({len(file_list)} copies):")
        for file in file_list:
            path = file.get('Full Path & Name', 'Unknown')
            size = file.get('Size', 0)
            print(f"  {path} ({size:,} bytes)")
    
    return duplicates

# Usage
duplicates = find_duplicate_names("C:\\Users")
```

### Find Large Files Taking Up Space

```python
def find_space_hogs(min_size="100MB", max_results=20):
    """Find files consuming the most disk space."""
    
    large_files = es.search_by_size(
        f">{min_size}",
        include_size=True,
        include_full_path=True,
        include_date_modified=True,
        sort_by="size",
        sort_ascending=False,
        max_results=max_results
    )
    
    total_size = 0
    print(f"Top {len(large_files)} files larger than {min_size}:")
    print("-" * 80)
    
    for i, file in enumerate(large_files, 1):
        name = file.get('Name', 'Unknown')
        size = file.get('Size', 0)
        path = file.get('Full Path & Name', 'Unknown')
        date = file.get('Date Modified', 'Unknown')
        
        size_gb = size / (1024**3)
        total_size += size
        
        print(f"{i:2d}. {name}")
        print(f"    Size: {size_gb:.2f} GB")
        print(f"    Path: {path}")
        print(f"    Modified: {date}")
        print()
    
    total_gb = total_size / (1024**3)
    print(f"Total size of top {len(large_files)} files: {total_gb:.2f} GB")
    
    return large_files

# Find files larger than 500MB
large_files = find_space_hogs("500MB", 15)
```

### Clean Up Temporary Files

```python
def find_temp_files():
    """Find temporary files that can potentially be cleaned up."""
    
    temp_patterns = [
        "*.tmp", "*.temp", "*~", "*.bak", 
        "*.old", "*.cache", "*.swp", "*.swo"
    ]
    
    all_temp_files = []
    total_size = 0
    
    print("Searching for temporary files...")
    
    for pattern in temp_patterns:
        files = es.search(
            pattern,
            include_size=True,
            include_full_path=True,
            include_date_modified=True,
            max_results=1000
        )
        
        if files:
            pattern_size = sum(f.get('Size', 0) for f in files)
            total_size += pattern_size
            all_temp_files.extend(files)
            
            print(f"{pattern}: {len(files)} files, {pattern_size / (1024**2):.1f} MB")
    
    print(f"\nTotal temporary files: {len(all_temp_files)}")
    print(f"Total size: {total_size / (1024**2):.1f} MB")
    
    # Show largest temp files
    all_temp_files.sort(key=lambda x: x.get('Size', 0), reverse=True)
    
    print("\nLargest temporary files:")
    for file in all_temp_files[:10]:
        name = file.get('Name', 'Unknown')
        size = file.get('Size', 0)
        path = file.get('Full Path & Name', 'Unknown')
        
        print(f"  {name} - {size / (1024**2):.1f} MB")
        print(f"    {path}")
    
    return all_temp_files

temp_files = find_temp_files()
```

### Organize Downloads Folder

```python
import os
from pathlib import Path
from datetime import datetime, timedelta

def analyze_downloads():
    """Analyze downloads folder for organization opportunities."""
    
    downloads_path = "C:\\Users\\%USERNAME%\\Downloads"  # Adjust path
    
    # Find all files in downloads
    downloads = es.search(
        "",
        path_filter=downloads_path,
        files_only=True,
        include_size=True,
        include_extension=True,
        include_date_modified=True,
        include_full_path=True,
        max_results=1000
    )
    
    if not downloads:
        print("No files found in downloads folder")
        return
    
    # Analyze by extension
    by_extension = {}
    total_size = 0
    
    for file in downloads:
        ext = file.get('Extension', '').lower()
        size = file.get('Size', 0)
        
        if ext not in by_extension:
            by_extension[ext] = {'files': [], 'total_size': 0}
        
        by_extension[ext]['files'].append(file)
        by_extension[ext]['total_size'] += size
        total_size += size
    
    print(f"Downloads folder analysis ({len(downloads)} files):")
    print(f"Total size: {total_size / (1024**2):.1f} MB")
    print("\nBy file type:")
    
    # Sort by total size
    for ext, data in sorted(by_extension.items(), 
                           key=lambda x: x[1]['total_size'], 
                           reverse=True):
        count = len(data['files'])
        size_mb = data['total_size'] / (1024**2)
        ext_display = ext if ext else "(no extension)"
        
        print(f"  {ext_display}: {count} files, {size_mb:.1f} MB")
    
    # Find old files
    cutoff_date = datetime.now() - timedelta(days=30)
    old_files = []
    
    for file in downloads:
        date_str = file.get('Date Modified', '')
        if date_str:
            try:
                # Parse date (format may vary)
                file_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if file_date < cutoff_date:
                    old_files.append(file)
            except:
                pass
    
    if old_files:
        old_size = sum(f.get('Size', 0) for f in old_files)
        print(f"\nOld files (>30 days): {len(old_files)} files, {old_size / (1024**2):.1f} MB")
    
    return downloads, by_extension

downloads_analysis = analyze_downloads()
```

## Development Workflows

### Find Source Code Files

```python
def find_source_code(project_path=None):
    """Find source code files with statistics."""
    
    code_extensions = {
        'py': 'Python',
        'js': 'JavaScript', 'ts': 'TypeScript', 'jsx': 'React JSX', 'tsx': 'React TSX',
        'java': 'Java', 'kt': 'Kotlin',
        'cpp': 'C++', 'cc': 'C++', 'cxx': 'C++',
        'c': 'C', 'h': 'C Header',
        'cs': 'C#',
        'go': 'Go',
        'rs': 'Rust',
        'php': 'PHP',
        'rb': 'Ruby',
        'swift': 'Swift',
        'scala': 'Scala',
        'html': 'HTML', 'css': 'CSS', 'scss': 'SCSS', 'sass': 'SASS',
        'sql': 'SQL',
        'sh': 'Shell Script', 'bash': 'Bash',
        'ps1': 'PowerShell',
        'yml': 'YAML', 'yaml': 'YAML',
        'json': 'JSON', 'xml': 'XML',
        'md': 'Markdown', 'rst': 'reStructuredText'
    }
    
    code_stats = {}
    
    search_params = {
        'include_size': True,
        'include_full_path': True,
        'max_results': 5000
    }
    
    if project_path:
        search_params['path_filter'] = project_path
    
    print("Analyzing source code files...")
    
    for ext, language in code_extensions.items():
        files = es.search_by_extension(ext, **search_params)
        
        if files:
            total_size = sum(f.get('Size', 0) for f in files)
            code_stats[language] = {
                'extension': ext,
                'files': files,
                'count': len(files),
                'total_size': total_size
            }
    
    # Display results
    print(f"\nSource code analysis:")
    print("-" * 50)
    
    total_files = 0
    total_size = 0
    
    for language, stats in sorted(code_stats.items(), 
                                 key=lambda x: x[1]['count'], 
                                 reverse=True):
        count = stats['count']
        size = stats['total_size']
        ext = stats['extension']
        
        total_files += count
        total_size += size
        
        print(f"{language:15} ({ext:4}): {count:4} files, {size / 1024:.1f} KB")
    
    print("-" * 50)
    print(f"{'Total':15}      : {total_files:4} files, {total_size / 1024:.1f} KB")
    
    return code_stats

# Analyze all source code
all_code = find_source_code()

# Analyze specific project
project_code = find_source_code("C:\\projects\\myproject")
```

### Find Configuration Files

```python
def find_config_files():
    """Find configuration files across the system."""
    
    config_patterns = [
        "*.ini", "*.cfg", "*.conf", "*.config",
        "*.json", "*.xml", "*.yaml", "*.yml", "*.toml",
        ".env", ".env.*",
        "*.properties",
        "package.json", "composer.json", "pyproject.toml",
        "Dockerfile", "docker-compose.yml",
        "*.gitignore", ".gitconfig",
        "requirements.txt", "Pipfile", "poetry.lock"
    ]
    
    config_files = []
    
    for pattern in config_patterns:
        files = es.search(
            pattern,
            include_full_path=True,
            include_size=True,
            max_results=500
        )
        config_files.extend(files)
    
    # Group by directory
    by_directory = {}
    for file in config_files:
        path = file.get('Full Path & Name', '')
        if path:
            directory = os.path.dirname(path)
            if directory not in by_directory:
                by_directory[directory] = []
            by_directory[directory].append(file)
    
    print(f"Found {len(config_files)} configuration files in {len(by_directory)} directories:")
    
    # Show directories with most config files
    sorted_dirs = sorted(by_directory.items(), 
                        key=lambda x: len(x[1]), 
                        reverse=True)
    
    for directory, files in sorted_dirs[:20]:  # Top 20 directories
        print(f"\n{directory} ({len(files)} files):")
        for file in files[:5]:  # Show first 5 files
            name = file.get('Name', 'Unknown')
            size = file.get('Size', 0)
            print(f"  {name} ({size} bytes)")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")
    
    return config_files

config_files = find_config_files()
```

### Find Log Files and Analyze Patterns

```python
from datetime import datetime, timedelta

def analyze_log_files():
    """Find and analyze log files."""
    
    log_patterns = ["*.log", "*.log.*", "*.out", "*.err"]
    
    all_logs = []
    for pattern in log_patterns:
        logs = es.search(
            pattern,
            include_size=True,
            include_full_path=True,
            include_date_modified=True,
            max_results=1000
        )
        all_logs.extend(logs)
    
    if not all_logs:
        print("No log files found")
        return
    
    # Analyze by size
    total_size = sum(f.get('Size', 0) for f in all_logs)
    large_logs = [f for f in all_logs if f.get('Size', 0) > 10 * 1024 * 1024]  # >10MB
    
    print(f"Log file analysis:")
    print(f"Total log files: {len(all_logs)}")
    print(f"Total size: {total_size / (1024**2):.1f} MB")
    print(f"Large log files (>10MB): {len(large_logs)}")
    
    # Recent logs (last 24 hours)
    yesterday = datetime.now() - timedelta(days=1)
    recent_logs = []
    
    for log in all_logs:
        date_str = log.get('Date Modified', '')
        if date_str:
            try:
                log_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if log_date > yesterday:
                    recent_logs.append(log)
            except:
                pass
    
    print(f"Recent logs (24h): {len(recent_logs)}")
    
    # Show largest logs
    all_logs.sort(key=lambda x: x.get('Size', 0), reverse=True)
    
    print("\nLargest log files:")
    for log in all_logs[:10]:
        name = log.get('Name', 'Unknown')
        size = log.get('Size', 0)
        path = log.get('Full Path & Name', 'Unknown')
        
        print(f"  {name} - {size / (1024**2):.1f} MB")
        print(f"    {path}")
    
    return all_logs

log_analysis = analyze_log_files()
```

## Data Analysis

### File System Inventory

```python
import pandas as pd
from collections import defaultdict

def create_file_inventory(path_filter=None, max_files=10000):
    """Create comprehensive file system inventory."""
    
    search_params = {
        'include_size': True,
        'include_extension': True,
        'include_date_modified': True,
        'include_full_path': True,
        'max_results': max_files
    }
    
    if path_filter:
        search_params['path_filter'] = path_filter
    
    print(f"Creating inventory of up to {max_files} files...")
    files = es.search("", **search_params)
    
    if not files:
        print("No files found")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(files)
    
    # Basic statistics
    total_files = len(df)
    total_size = df['Size'].sum() if 'Size' in df.columns else 0
    
    print(f"\nFile System Inventory Report:")
    print(f"Total files analyzed: {total_files:,}")
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    
    # Analysis by extension
    if 'Extension' in df.columns:
        ext_stats = df.groupby('Extension').agg({
            'Size': ['count', 'sum', 'mean'],
            'Name': 'count'
        }).round(2)
        
        print("\nTop 10 file types by count:")
        top_by_count = df['Extension'].value_counts().head(10)
        for ext, count in top_by_count.items():
            ext_display = ext if ext else "(no extension)"
            total_ext_size = df[df['Extension'] == ext]['Size'].sum()
            print(f"  {ext_display:10}: {count:6,} files, {total_ext_size / (1024**2):8.1f} MB")
        
        print("\nTop 10 file types by total size:")
        ext_sizes = df.groupby('Extension')['Size'].sum().sort_values(ascending=False).head(10)
        for ext, size in ext_sizes.items():
            count = df[df['Extension'] == ext].shape[0]
            ext_display = ext if ext else "(no extension)"
            print(f"  {ext_display:10}: {size / (1024**2):8.1f} MB, {count:6,} files")
    
    # Size distribution
    print("\nFile size distribution:")
    size_ranges = [
        (0, 1024, "< 1KB"),
        (1024, 1024**2, "1KB - 1MB"),
        (1024**2, 10 * 1024**2, "1MB - 10MB"),
        (10 * 1024**2, 100 * 1024**2, "10MB - 100MB"),
        (100 * 1024**2, 1024**3, "100MB - 1GB"),
        (1024**3, float('inf'), "> 1GB")
    ]
    
    for min_size, max_size, label in size_ranges:
        if 'Size' in df.columns:
            count = df[(df['Size'] >= min_size) & (df['Size'] < max_size)].shape[0]
            total_range_size = df[(df['Size'] >= min_size) & (df['Size'] < max_size)]['Size'].sum()
            print(f"  {label:12}: {count:6,} files, {total_range_size / (1024**2):8.1f} MB")
    
    # Save to Excel for further analysis
    if path_filter:
        filename = f"inventory_{path_filter.replace(':', '').replace('\\\\', '_')}.xlsx"
    else:
        filename = "file_inventory.xlsx"
    
    df.to_excel(filename, index=False)
    print(f"\nDetailed inventory saved to: {filename}")
    
    return df

# Create inventory of entire system (limited)
inventory_df = create_file_inventory(max_files=50000)

# Create inventory of specific directory
project_inventory = create_file_inventory("C:\\projects", max_files=10000)
```

### Storage Analysis by Directory

```python
def analyze_directory_sizes(root_path="C:\\"):
    """Analyze storage usage by directory."""
    
    # Get all directories
    directories = es.search_folders(
        "",
        path_filter=root_path,
        include_full_path=True,
        max_results=1000
    )
    
    dir_stats = {}
    
    print(f"Analyzing directory sizes under {root_path}...")
    
    for directory in directories:
        dir_path = directory.get('Full Path & Name', '')
        if not dir_path:
            continue
        
        # Get files in this directory
        try:
            files = es.search(
                "",
                path_filter=dir_path,
                files_only=True,
                include_size=True,
                max_results=10000,
                timeout=30000
            )
            
            total_size = sum(f.get('Size', 0) for f in files)
            file_count = len(files)
            
            dir_stats[dir_path] = {
                'files': file_count,
                'size': total_size
            }
            
        except Exception as e:
            print(f"Error analyzing {dir_path}: {e}")
            continue
    
    # Sort by size
    sorted_dirs = sorted(dir_stats.items(), 
                        key=lambda x: x[1]['size'], 
                        reverse=True)
    
    print(f"\nDirectory size analysis (top {min(20, len(sorted_dirs))}):")
    print("-" * 80)
    
    total_analyzed_size = 0
    for dir_path, stats in sorted_dirs[:20]:
        size_gb = stats['size'] / (1024**3)
        file_count = stats['files']
        total_analyzed_size += stats['size']
        
        # Get directory name
        dir_name = os.path.basename(dir_path) or dir_path
        
        print(f"{dir_name[:40]:40} {size_gb:8.2f} GB  {file_count:8,} files")
        if len(dir_name) > 40:
            print(f"  Full path: {dir_path}")
    
    print("-" * 80)
    print(f"Total analyzed: {total_analyzed_size / (1024**3):.2f} GB")
    
    return dir_stats

# Analyze directories
dir_analysis = analyze_directory_sizes("C:\\Users")
```

## Media Management

### Organize Photo Collection

```python
from datetime import datetime
import os

def analyze_photo_collection():
    """Analyze photo collection by type, size, and date."""
    
    photo_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'raw', 'cr2', 'nef']
    
    all_photos = []
    
    print("Searching for photos...")
    for ext in photo_extensions:
        photos = es.search_by_extension(
            ext,
            include_size=True,
            include_full_path=True,
            include_date_modified=True,
            max_results=5000
        )
        all_photos.extend(photos)
    
    if not all_photos:
        print("No photos found")
        return
    
    # Statistics
    total_photos = len(all_photos)
    total_size = sum(p.get('Size', 0) for p in all_photos)
    
    print(f"\nPhoto Collection Analysis:")
    print(f"Total photos: {total_photos:,}")
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    print(f"Average size: {total_size / total_photos / (1024**2):.1f} MB per photo")
    
    # By extension
    by_extension = {}
    for photo in all_photos:
        ext = photo.get('Extension', '').lower()
        if ext not in by_extension:
            by_extension[ext] = {'count': 0, 'size': 0}
        by_extension[ext]['count'] += 1
        by_extension[ext]['size'] += photo.get('Size', 0)
    
    print("\nBy file type:")
    for ext, stats in sorted(by_extension.items(), key=lambda x: x[1]['count'], reverse=True):
        count = stats['count']
        size = stats['size']
        print(f"  {ext.upper():5}: {count:6,} photos, {size / (1024**2):8.1f} MB")
    
    # Find largest photos
    all_photos.sort(key=lambda x: x.get('Size', 0), reverse=True)
    
    print("\nLargest photos:")
    for photo in all_photos[:10]:
        name = photo.get('Name', 'Unknown')
        size = photo.get('Size', 0)
        path = photo.get('Full Path & Name', 'Unknown')
        
        print(f"  {name} - {size / (1024**2):.1f} MB")
        print(f"    {path}")
    
    # Group by directory
    by_directory = {}
    for photo in all_photos:
        path = photo.get('Full Path & Name', '')
        if path:
            directory = os.path.dirname(path)
            if directory not in by_directory:
                by_directory[directory] = []
            by_directory[directory].append(photo)
    
    print(f"\nPhotos distributed across {len(by_directory)} directories:")
    sorted_dirs = sorted(by_directory.items(), key=lambda x: len(x[1]), reverse=True)
    
    for directory, photos in sorted_dirs[:10]:
        count = len(photos)
        total_dir_size = sum(p.get('Size', 0) for p in photos)
        print(f"  {count:4} photos, {total_dir_size / (1024**2):6.1f} MB - {directory}")
    
    return all_photos

photo_analysis = analyze_photo_collection()
```

### Find and Analyze Video Files

```python
def analyze_video_collection():
    """Analyze video files by format, resolution, and size."""
    
    video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v', '3gp', 'mpg', 'mpeg']
    
    all_videos = []
    
    print("Searching for video files...")
    for ext in video_extensions:
        videos = es.search_by_extension(
            ext,
            include_size=True,
            include_full_path=True,
            include_date_modified=True,
            max_results=2000
        )
        all_videos.extend(videos)
    
    if not all_videos:
        print("No video files found")
        return
    
    # Statistics
    total_videos = len(all_videos)
    total_size = sum(v.get('Size', 0) for v in all_videos)
    
    print(f"\nVideo Collection Analysis:")
    print(f"Total videos: {total_videos:,}")
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    print(f"Average size: {total_size / total_videos / (1024**2):.1f} MB per video")
    
    # By format
    by_format = {}
    for video in all_videos:
        ext = video.get('Extension', '').lower()
        if ext not in by_format:
            by_format[ext] = {'count': 0, 'size': 0}
        by_format[ext]['count'] += 1
        by_format[ext]['size'] += video.get('Size', 0)
    
    print("\nBy format:")
    for ext, stats in sorted(by_format.items(), key=lambda x: x[1]['size'], reverse=True):
        count = stats['count']
        size = stats['size']
        avg_size = size / count if count > 0 else 0
        print(f"  {ext.upper():5}: {count:4} videos, {size / (1024**3):.2f} GB (avg: {avg_size / (1024**2):.1f} MB)")
    
    # Size categories
    size_categories = [
        (0, 100 * 1024**2, "< 100MB (clips)"),
        (100 * 1024**2, 700 * 1024**2, "100MB - 700MB (TV episodes)"),
        (700 * 1024**2, 2 * 1024**3, "700MB - 2GB (movies SD)"),
        (2 * 1024**3, 8 * 1024**3, "2GB - 8GB (movies HD)"),
        (8 * 1024**3, float('inf'), "> 8GB (movies 4K)")
    ]
    
    print("\nBy size category:")
    for min_size, max_size, label in size_categories:
        category_videos = [v for v in all_videos 
                          if min_size <= v.get('Size', 0) < max_size]
        count = len(category_videos)
        total_category_size = sum(v.get('Size', 0) for v in category_videos)
        
        if count > 0:
            print(f"  {label:25}: {count:4} videos, {total_category_size / (1024**3):.2f} GB")
    
    # Largest videos
    all_videos.sort(key=lambda x: x.get('Size', 0), reverse=True)
    
    print("\nLargest video files:")
    for video in all_videos[:10]:
        name = video.get('Name', 'Unknown')
        size = video.get('Size', 0)
        path = video.get('Full Path & Name', 'Unknown')
        
        print(f"  {name[:50]:50} {size / (1024**3):6.2f} GB")
        if len(name) > 50:
            print(f"    Full name: {name}")
    
    return all_videos

video_analysis = analyze_video_collection()
```

## System Administration

### Security Audit - Find Executable Files

```python
def security_audit_executables():
    """Find executable files for security review."""
    
    executable_extensions = ['exe', 'msi', 'bat', 'cmd', 'ps1', 'vbs', 'scr', 'com', 'pif']
    
    all_executables = []
    
    print("Scanning for executable files...")
    for ext in executable_extensions:
        executables = es.search_by_extension(
            ext,
            include_size=True,
            include_full_path=True,
            include_date_modified=True,
            max_results=5000
        )
        all_executables.extend(executables)
    
    if not all_executables:
        print("No executable files found")
        return
    
    # Analyze by location
    system_paths = ['C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)']
    user_paths = ['C:\\Users']
    temp_paths = ['C:\\Temp', 'C:\\Windows\\Temp', 'AppData\\Local\\Temp']
    
    categorized = {
        'system': [],
        'programs': [],
        'user': [],
        'temp': [],
        'other': []
    }
    
    for exe in all_executables:
        path = exe.get('Full Path & Name', '').lower()
        
        if any(sys_path.lower() in path for sys_path in system_paths):
            if 'program files' in path:
                categorized['programs'].append(exe)
            else:
                categorized['system'].append(exe)
        elif any(user_path.lower() in path for user_path in user_paths):
            categorized['user'].append(exe)
        elif any(temp_path.lower() in path for temp_path in temp_paths):
            categorized['temp'].append(exe)
        else:
            categorized['other'].append(exe)
    
    print(f"\nExecutable Files Security Audit:")
    print(f"Total executables found: {len(all_executables)}")
    
    for category, files in categorized.items():
        if files:
            total_size = sum(f.get('Size', 0) for f in files)
            print(f"  {category.capitalize():10}: {len(files):4} files, {total_size / (1024**2):.1f} MB")
    
    # Flag potentially suspicious files
    suspicious_indicators = [
        ('temp', 'Temporary directory executables'),
        ('download', 'Downloaded executables'),
        ('desktop', 'Desktop executables'),
        ('appdata\\local\\temp', 'User temp executables')
    ]
    
    suspicious_files = []
    for indicator, description in suspicious_indicators:
        for exe in all_executables:
            path = exe.get('Full Path & Name', '').lower()
            if indicator in path:
                suspicious_files.append((exe, description))
    
    if suspicious_files:
        print(f"\nPotentially suspicious executable locations:")
        for exe, reason in suspicious_files[:20]:  # Show first 20
            name = exe.get('Name', 'Unknown')
            path = exe.get('Full Path & Name', 'Unknown')
            size = exe.get('Size', 0)
            
            print(f"  {name} ({reason})")
            print(f"    {path} ({size / 1024:.1f} KB)")
    
    # Recent executables (last 7 days)
    from datetime import datetime, timedelta
    recent_cutoff = datetime.now() - timedelta(days=7)
    recent_executables = []
    
    for exe in all_executables:
        date_str = exe.get('Date Modified', '')
        if date_str:
            try:
                exe_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if exe_date > recent_cutoff:
                    recent_executables.append(exe)
            except:
                pass
    
    if recent_executables:
        print(f"\nRecently modified executables (last 7 days): {len(recent_executables)}")
        for exe in recent_executables[:10]:
            name = exe.get('Name', 'Unknown')
            path = exe.get('Full Path & Name', 'Unknown')
            date = exe.get('Date Modified', 'Unknown')
            
            print(f"  {name} - {date}")
            print(f"    {path}")
    
    return all_executables, categorized

exe_audit = security_audit_executables()
```

### System Cleanup Recommendations

```python
def system_cleanup_recommendations():
    """Generate system cleanup recommendations."""
    
    cleanup_categories = {
        'Browser Cache': [
            'AppData\\Local\\Google\\Chrome\\User Data\\*\\Cache',
            'AppData\\Local\\Mozilla\\Firefox\\Profiles\\*\\cache2',
            'AppData\\Local\\Microsoft\\Edge\\User Data\\*\\Cache',
        ],
        'Temporary Files': [
            '*.tmp', '*.temp', '*~', '*.bak', '*.old'
        ],
        'Log Files': [
            '*.log', '*.log.*'
        ],
        'Crash Dumps': [
            '*.dmp', '*.mdmp'
        ],
        'Backup Files': [
            '*.backup', '*.bck', '*_backup.*'
        ]
    }
    
    recommendations = {}
    total_cleanup_size = 0
    
    print("Generating system cleanup recommendations...")
    
    for category, patterns in cleanup_categories.items():
        category_files = []
        category_size = 0
        
        for pattern in patterns:
            try:
                if 'AppData' in pattern:
                    # Handle AppData patterns specially
                    files = es.search(
                        "",
                        path_filter="C:\\Users",
                        include_size=True,
                        include_full_path=True,
                        max_results=1000,
                        timeout=30000
                    )
                    # Filter by pattern in path
                    filtered_files = [f for f in files 
                                    if pattern.lower().replace('*', '') in 
                                    f.get('Full Path & Name', '').lower()]
                else:
                    filtered_files = es.search(
                        pattern,
                        include_size=True,
                        include_full_path=True,
                        max_results=1000
                    )
                
                category_files.extend(filtered_files)
                
            except Exception as e:
                print(f"Error searching {pattern}: {e}")
                continue
        
        if category_files:
            category_size = sum(f.get('Size', 0) for f in category_files)
            total_cleanup_size += category_size
            
            recommendations[category] = {
                'files': category_files,
                'count': len(category_files),
                'size': category_size
            }
    
    # Display recommendations
    print(f"\nSystem Cleanup Recommendations:")
    print(f"Total potential cleanup space: {total_cleanup_size / (1024**3):.2f} GB")
    print("-" * 60)
    
    for category, data in sorted(recommendations.items(), 
                                key=lambda x: x[1]['size'], 
                                reverse=True):
        count = data['count']
        size = data['size']
        
        print(f"{category}:")
        print(f"  Files: {count:,}")
        print(f"  Size: {size / (1024**2):.1f} MB")
        print(f"  Potential savings: {size / (1024**3):.2f} GB")
        
        # Show largest files in category
        largest_files = sorted(data['files'], 
                              key=lambda x: x.get('Size', 0), 
                              reverse=True)[:3]
        
        if largest_files:
            print("  Largest files:")
            for file in largest_files:
                name = file.get('Name', 'Unknown')
                file_size = file.get('Size', 0)
                print(f"    {name} ({file_size / (1024**2):.1f} MB)")
        print()
    
    return recommendations

cleanup_recs = system_cleanup_recommendations()
```

## Integration Examples

### Export Data to Different Formats

```python
import json
import csv
from pathlib import Path

def export_search_results():
    """Export search results to various formats."""
    
    # Search for recent large files
    large_recent = es.search(
        "",
        include_size=True,
        include_full_path=True,
        include_date_modified=True,
        include_extension=True,
        max_results=500
    )
    
    # Filter for files larger than 10MB modified in last 30 days
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.now() - timedelta(days=30)
    filtered_files = []
    
    for file in large_recent:
        size = file.get('Size', 0)
        if size > 10 * 1024 * 1024:  # >10MB
            date_str = file.get('Date Modified', '')
            if date_str:
                try:
                    file_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    if file_date > cutoff_date:
                        filtered_files.append(file)
                except:
                    pass
    
    print(f"Exporting {len(filtered_files)} large recent files...")
    
    # Export to JSON
    with open('large_recent_files.json', 'w') as f:
        json.dump(filtered_files, f, indent=2)
    
    # Export to CSV
    if filtered_files:
        fieldnames = filtered_files[0].keys()
        with open('large_recent_files.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_files)
    
    # Export to Excel with pandas
    try:
        import pandas as pd
        df = pd.DataFrame(filtered_files)
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter('large_recent_files.xlsx') as writer:
            df.to_excel(writer, sheet_name='All Files', index=False)
            
            # Group by extension
            if 'Extension' in df.columns:
                for ext in df['Extension'].unique():
                    if ext:  # Skip empty extensions
                        ext_data = df[df['Extension'] == ext]
                        sheet_name = f'{ext.upper()} Files'
                        ext_data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print("Exported to Excel with multiple sheets")
        
    except ImportError:
        print("Pandas not available, skipping Excel export")
    
    # Create summary report
    with open('export_summary.txt', 'w') as f:
        f.write("Large Recent Files Export Summary\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total files: {len(filtered_files)}\n")
        
        if filtered_files:
            total_size = sum(file.get('Size', 0) for file in filtered_files)
            f.write(f"Total size: {total_size / (1024**3):.2f} GB\n")
            f.write(f"Average size: {total_size / len(filtered_files) / (1024**2):.1f} MB\n\n")
            
            # By extension
            by_ext = {}
            for file in filtered_files:
                ext = file.get('Extension', 'no extension')
                if ext not in by_ext:
                    by_ext[ext] = []
                by_ext[ext].append(file)
            
            f.write("Files by extension:\n")
            for ext, files in sorted(by_ext.items(), key=lambda x: len(x[1]), reverse=True):
                ext_size = sum(file.get('Size', 0) for file in files)
                f.write(f"  {ext}: {len(files)} files, {ext_size / (1024**2):.1f} MB\n")
    
    print("Export complete! Files created:")
    print("  - large_recent_files.json")
    print("  - large_recent_files.csv")
    print("  - large_recent_files.xlsx")
    print("  - export_summary.txt")

export_search_results()
```

### Integration with Git Repositories

```python
import subprocess
import os
from pathlib import Path

def analyze_git_repositories():
    """Find and analyze Git repositories."""
    
    # Find all .git directories
    git_dirs = es.search_folders(
        ".git",
        include_full_path=True,
        max_results=100
    )
    
    repositories = []
    
    print("Analyzing Git repositories...")
    
    for git_dir in git_dirs:
        git_path = git_dir.get('Full Path & Name', '')
        if not git_path:
            continue
        
        # Repository is parent directory of .git
        repo_path = Path(git_path).parent
        
        try:
            # Get repository information
            repo_info = {
                'path': str(repo_path),
                'name': repo_path.name,
                'size': 0,
                'files': 0,
                'status': 'unknown',
                'branches': [],
                'remotes': []
            }
            
            # Get repository size and file count
            repo_files = es.search(
                "",
                path_filter=str(repo_path),
                include_size=True,
                max_results=10000,
                timeout=30000
            )
            
            repo_info['files'] = len(repo_files)
            repo_info['size'] = sum(f.get('Size', 0) for f in repo_files)
            
            # Get Git status (requires git command)
            try:
                # Get current branch
                branch_result = subprocess.run(
                    ['git', 'branch', '--show-current'],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if branch_result.returncode == 0:
                    current_branch = branch_result.stdout.strip()
                    repo_info['current_branch'] = current_branch
                
                # Get all branches
                branches_result = subprocess.run(
                    ['git', 'branch', '-a'],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if branches_result.returncode == 0:
                    branches = [b.strip().replace('* ', '') for b in branches_result.stdout.split('\n') if b.strip()]
                    repo_info['branches'] = branches
                
                # Get status
                status_result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if status_result.returncode == 0:
                    if status_result.stdout.strip():
                        repo_info['status'] = 'dirty'
                    else:
                        repo_info['status'] = 'clean'
                
                # Get remotes
                remotes_result = subprocess.run(
                    ['git', 'remote', '-v'],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if remotes_result.returncode == 0:
                    remotes = []
                    for line in remotes_result.stdout.split('\n'):
                        if line.strip() and '(fetch)' in line:
                            parts = line.split()
                            if len(parts) >= 2:
                                remotes.append(f"{parts[0]}: {parts[1]}")
                    repo_info['remotes'] = remotes
                
            except subprocess.TimeoutExpired:
                repo_info['status'] = 'timeout'
            except Exception as e:
                repo_info['status'] = f'error: {str(e)}'
            
            repositories.append(repo_info)
            
        except Exception as e:
            print(f"Error analyzing {repo_path}: {e}")
            continue
    
    # Display results
    print(f"\nGit Repository Analysis:")
    print(f"Found {len(repositories)} repositories")
    print("-" * 80)
    
    # Sort by size
    repositories.sort(key=lambda x: x['size'], reverse=True)
    
    for repo in repositories:
        print(f"Repository: {repo['name']}")
        print(f"  Path: {repo['path']}")
        print(f"  Size: {repo['size'] / (1024**2):.1f} MB")
        print(f"  Files: {repo['files']:,}")
        print(f"  Status: {repo['status']}")
        
        if repo.get('current_branch'):
            print(f"  Current branch: {repo['current_branch']}")
        
        if repo['branches']:
            branch_count = len([b for b in repo['branches'] if not b.startswith('remotes/')])
            remote_count = len([b for b in repo['branches'] if b.startswith('remotes/')])
            print(f"  Branches: {branch_count} local, {remote_count} remote")
        
        if repo['remotes']:
            print(f"  Remotes: {', '.join(repo['remotes'])}")
        
        print()
    
    # Summary
    total_size = sum(repo['size'] for repo in repositories)
    total_files = sum(repo['files'] for repo in repositories)
    dirty_repos = [repo for repo in repositories if repo['status'] == 'dirty']
    
    print(f"Summary:")
    print(f"  Total repositories: {len(repositories)}")
    print(f"  Total size: {total_size / (1024**3):.2f} GB")
    print(f"  Total files: {total_files:,}")
    print(f"  Repositories with changes: {len(dirty_repos)}")
    
    if dirty_repos:
        print(f"\nRepositories with uncommitted changes:")
        for repo in dirty_repos:
            print(f"  {repo['name']} - {repo['path']}")
    
    return repositories

git_analysis = analyze_git_repositories()
```

## Advanced Patterns

### Asynchronous File Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from everything_search import EverythingSearch

async def async_file_processor():
    """Process files asynchronously using thread pool."""
    
    def search_extension(extension):
        """Thread worker function."""
        es = EverythingSearch()  # Create instance per thread
        return es.search_by_extension(
            extension,
            include_size=True,
            include_full_path=True,
            max_results=1000
        )
    
    # Extensions to search for
    extensions = ['py', 'js', 'html', 'css', 'json', 'xml', 'md', 'txt']
    
    # Create thread pool executor
    with ThreadPoolExecutor(max_workers=4) as executor:
        loop = asyncio.get_event_loop()
        
        # Create tasks for each extension
        tasks = []
        for ext in extensions:
            task = loop.run_in_executor(executor, search_extension, ext)
            tasks.append((ext, task))
        
        # Wait for all tasks to complete
        print("Searching for multiple file types asynchronously...")
        results = {}
        
        for ext, task in tasks:
            try:
                files = await task
                results[ext] = files
                print(f"Found {len(files)} {ext.upper()} files")
            except Exception as e:
                print(f"Error searching {ext}: {e}")
                results[ext] = []
    
    # Process results
    total_files = sum(len(files) for files in results.values())
    total_size = sum(sum(f.get('Size', 0) for f in files) for files in results.values())
    
    print(f"\nAsync search completed:")
    print(f"Total files found: {total_files:,}")
    print(f"Total size: {total_size / (1024**2):.1f} MB")
    
    return results

# Run async function
async_results = asyncio.run(async_file_processor())
```

### Custom File Categorization

```python
def categorize_files_by_purpose():
    """Categorize files by their likely purpose."""
    
    categories = {
        'Source Code': {
            'extensions': ['py', 'js', 'ts', 'jsx', 'tsx', 'java', 'cpp', 'c', 'cs', 'go', 'rs', 'php', 'rb'],
            'files': []
        },
        'Web Assets': {
            'extensions': ['html', 'css', 'scss', 'sass', 'less'],
            'files': []
        },
        'Data Files': {
            'extensions': ['json', 'xml', 'yaml', 'yml', 'csv', 'sql'],
            'files': []
        },
        'Documentation': {
            'extensions': ['md', 'rst', 'txt', 'doc', 'docx', 'pdf'],
            'files': []
        },
        'Images': {
            'extensions': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'ico'],
            'files': []
        },
        'Audio': {
            'extensions': ['mp3', 'wav', 'flac', 'aac', 'm4a', 'ogg'],
            'files': []
        },
        'Video': {
            'extensions': ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'webm'],
            'files': []
        },
        'Archives': {
            'extensions': ['zip', 'rar', '7z', 'tar', 'gz', 'bz2'],
            'files': []
        },
        'Configuration': {
            'extensions': ['ini', 'cfg', 'conf', 'config', 'toml', 'properties'],
            'files': []
        },
        'Executables': {
            'extensions': ['exe', 'msi', 'deb', 'rpm', 'dmg', 'pkg'],
            'files': []
        }
    }
    
    print("Categorizing files by purpose...")
    
    # Search for each category
    for category_name, category_data in categories.items():
        print(f"Searching {category_name}...")
        
        for ext in category_data['extensions']:
            files = es.search_by_extension(
                ext,
                include_size=True,
                include_full_path=True,
                max_results=2000
            )
            category_data['files'].extend(files)
    
    # Generate report
    print(f"\nFile Categorization Report:")
    print("=" * 50)
    
    total_files = 0
    total_size = 0
    
    for category_name, category_data in sorted(categories.items()):
        files = category_data['files']
        if files:
            category_size = sum(f.get('Size', 0) for f in files)
            file_count = len(files)
            
            total_files += file_count
            total_size += category_size
            
            print(f"{category_name}:")
            print(f"  Files: {file_count:,}")
            print(f"  Size: {category_size / (1024**2):.1f} MB")
            print(f"  Average: {category_size / file_count / 1024:.1f} KB per file")
            
            # Show file type breakdown
            by_ext = {}
            for file in files:
                ext = file.get('Extension', '').lower()
                if ext not in by_ext:
                    by_ext[ext] = 0
                by_ext[ext] += 1
            
            if len(by_ext) > 1:
                print("  Breakdown:", ', '.join(f"{ext}: {count}" for ext, count in sorted(by_ext.items())))
            
            print()
    
    print(f"Total categorized files: {total_files:,}")
    print(f"Total size: {total_size / (1024**2):.1f} MB")
    
    # Find largest files in each category
    print("\nLargest files by category:")
    for category_name, category_data in categories.items():
        files = category_data['files']
        if files:
            largest = max(files, key=lambda x: x.get('Size', 0))
            size = largest.get('Size', 0)
            name = largest.get('Name', 'Unknown')
            
            if size > 1024 * 1024:  # > 1MB
                print(f"  {category_name}: {name} ({size / (1024**2):.1f} MB)")
    
    return categories

file_categories = categorize_files_by_purpose()
```

These examples demonstrate the versatility of the Everything Search Python wrapper for various file management, analysis, and automation tasks. Each example can be adapted and extended based on specific needs and requirements.