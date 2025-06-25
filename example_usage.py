#!/usr/bin/env python3
"""
Example usage of the Everything Search Python wrapper.
"""

from everything_search import EverythingSearch


def main():
    # Initialize the Everything Search wrapper
    es = EverythingSearch()

    print("Everything Search Python Wrapper - Examples\n")

    try:
        # Get version
        print(f"Version: {es.get_version()}\n")

        # Basic search
        print("1. Basic search for 'python' files:")
        results = es.search(
            "python", max_results=5, include_full_path=True, include_size=True
        )
        for result in results:
            print(
                f"  {result.get('Filename', 'N/A')} - {result.get('Size', 'N/A')} bytes"
            )
        print()

        # Search by extension
        print("2. Search for .exe files:")
        exe_files = es.search_by_extension("exe", max_results=3, include_full_path=True)
        for file in exe_files:
            print(f"  {file.get('Filename', 'N/A')}")
        print()

        # Search folders only
        print("3. Search for folders containing 'temp':")
        folders = es.search_folders("temp", max_results=3, include_full_path=True)
        for folder in folders:
            print(f"  {folder.get('Filename', 'N/A')}")
        print()

        # Search by size
        print("4. Search for large files (>100MB):")
        large_files = es.search_by_size(
            ">100MB", max_results=3, include_full_path=True, include_size=True
        )
        for file in large_files:
            size_mb = (
                file.get("Size", 0) / (1024 * 1024)
                if isinstance(file.get("Size"), int)
                else 0
            )
            print(f"  {file.get('Filename', 'N/A')} - {size_mb:.2f} MB")
        print()

        # Search recent files
        print("5. Recently modified files (last 7 days):")
        recent_files = es.search_recent(
            days=7, max_results=3, include_full_path=True, include_date_modified=True
        )
        for file in recent_files:
            print(
                f"  {file.get('Filename', 'N/A')} - {file.get('Date Modified', 'N/A')}"
            )
        print()

        # Case sensitive search
        print("6. Case sensitive search for 'Python':")
        case_results = es.search(
            "Python", case_sensitive=True, max_results=3, include_full_path=True
        )
        for result in case_results:
            print(f"  {result.get('Filename', 'N/A')}")
        print()

        # Regex search
        print("7. Regex search for files ending with numbers:")
        regex_results = es.search(
            r".*\d+\.(txt|log)$", regex=True, max_results=3, include_full_path=True
        )
        for result in regex_results:
            print(f"  {result.get('Filename', 'N/A')}")
        print()

        # Get result count
        print("8. Total number of .txt files:")
        txt_count = es.get_result_count("ext:txt")
        print(f"  Found {txt_count} .txt files")
        print()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
