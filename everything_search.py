import csv
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union


class EverythingSearch:
    """
    Python wrapper for Everything Search (es.exe) command-line tool.

    This class provides a Pythonic interface to Everything Search functionality,
    allowing you to search for files and folders using various filters and options.
    """

    def __init__(self, es_path: str = "/mnt/c/Program Files/Everything/es.exe"):
        """
        Initialize the Everything Search wrapper.

        Args:
            es_path: Path to the es.exe executable
        """
        self.es_path = es_path
        if not os.path.exists(self.es_path):
            raise FileNotFoundError(
                f"Everything Search executable not found at: {self.es_path}"
            )

    def search(
        self,
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
    ) -> List[Dict[str, Union[str, int]]]:
        """
        Search for files and folders using Everything Search.

        Args:
            query: Search query string
            regex: Use regular expressions
            case_sensitive: Match case
            whole_words: Match whole words only
            match_path: Match full path and file name
            match_diacritics: Match diacritical marks
            max_results: Maximum number of results to return
            offset: Starting offset for results
            path_filter: Search within specific path
            parent_path: Search in parent of specified path
            parent: Search for files with specified parent path
            folders_only: Return only folders
            files_only: Return only files
            attributes: DIR style attributes filter (e.g., "RHSD")
            sort_by: Sort results by field (name, path, size, extension, etc.)
            sort_ascending: Sort in ascending order
            include_name: Include name in results
            include_path: Include path column
            include_full_path: Include full path and name
            include_extension: Include file extension
            include_size: Include file size
            include_date_created: Include creation date
            include_date_modified: Include modification date
            include_date_accessed: Include access date
            include_attributes: Include file attributes
            timeout: Timeout in milliseconds

        Returns:
            List of dictionaries containing search results
        """
        cmd = [self.es_path]

        # Search options
        if regex:
            cmd.extend(["-regex", query])
        else:
            cmd.append(query)

        if case_sensitive:
            cmd.append("-case")
        if whole_words:
            cmd.append("-whole-words")
        if match_path:
            cmd.append("-match-path")
        if match_diacritics:
            cmd.append("-diacritics")

        # Limit and offset
        if max_results is not None:
            cmd.extend(["-max-results", str(max_results)])
        if offset > 0:
            cmd.extend(["-offset", str(offset)])

        # Path filters
        if path_filter:
            cmd.extend(["-path", path_filter])
        if parent_path:
            cmd.extend(["-parent-path", parent_path])
        if parent:
            cmd.extend(["-parent", parent])

        # File type filters
        if folders_only:
            cmd.append("/ad")
        elif files_only:
            cmd.append("/a-d")

        if attributes:
            cmd.append(f"/a{attributes}")

        # Sorting
        if sort_by:
            sort_order = "ascending" if sort_ascending else "descending"
            cmd.extend(["-sort", f"{sort_by}-{sort_order}"])

        # Display options
        if include_name:
            cmd.append("-name")
        if include_path:
            cmd.append("-path-column")
        if include_full_path:
            cmd.append("-full-path-and-name")
        if include_extension:
            cmd.append("-extension")
        if include_size:
            cmd.append("-size")
        if include_date_created:
            cmd.append("-date-created")
        if include_date_modified:
            cmd.append("-date-modified")
        if include_date_accessed:
            cmd.append("-date-accessed")
        if include_attributes:
            cmd.append("-attributes")

        # Output format
        cmd.append("-csv")
        cmd.extend(["-timeout", str(timeout)])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
            )

            if result.returncode != 0:
                raise RuntimeError(f"Everything Search failed: {result.stderr}")

            return self._parse_csv_output(result.stdout)

        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Search timed out after {timeout}ms")
        except Exception as e:
            raise RuntimeError(f"Error executing search: {str(e)}")

    def _parse_csv_output(self, csv_output: str) -> List[Dict[str, Union[str, int]]]:
        """Parse CSV output from es.exe into list of dictionaries."""
        if not csv_output.strip():
            return []

        lines = csv_output.strip().split("\n")
        if len(lines) < 2:
            return []

        reader = csv.DictReader(lines)
        results = []

        for row in reader:
            # Convert size to int if present
            if "Size" in row and row["Size"].isdigit():
                row["Size"] = int(row["Size"])
            results.append(dict(row))

        return results

    def search_files(
        self, query: str = "", **kwargs
    ) -> List[Dict[str, Union[str, int]]]:
        """Search for files only."""
        return self.search(query, files_only=True, **kwargs)

    def search_folders(
        self, query: str = "", **kwargs
    ) -> List[Dict[str, Union[str, int]]]:
        """Search for folders only."""
        return self.search(query, folders_only=True, **kwargs)

    def search_by_extension(
        self, extension: str, **kwargs
    ) -> List[Dict[str, Union[str, int]]]:
        """Search for files with specific extension."""
        query = f"ext:{extension}"
        return self.search(query, files_only=True, **kwargs)

    def search_by_size(
        self, size_filter: str, **kwargs
    ) -> List[Dict[str, Union[str, int]]]:
        """
        Search for files by size.

        Args:
            size_filter: Size filter (e.g., ">1MB", "<100KB", "1GB..2GB")
        """
        query = f"size:{size_filter}"
        kwargs.setdefault("include_size", True)
        return self.search(query, files_only=True, **kwargs)

    def search_recent(
        self, days: int = 7, **kwargs
    ) -> List[Dict[str, Union[str, int]]]:
        """Search for recently modified files."""
        query = f"datemodified:last{days}days"
        kwargs.setdefault("include_date_modified", True)
        return self.search(query, **kwargs)

    def get_version(self) -> str:
        """Get Everything Search version."""
        try:
            result = subprocess.run(
                [self.es_path, "-version"], capture_output=True, text=True
            )
            return result.stdout.strip()
        except Exception as e:
            raise RuntimeError(f"Error getting version: {str(e)}")

    def get_result_count(self, query: str) -> int:
        """Get the total number of results for a query without retrieving them."""
        cmd = [self.es_path, "-get-result-count", query]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return int(result.stdout.strip())
            return 0
        except Exception:
            return 0

    def export_results(
        self, query: str, output_file: str, format: str = "csv", **kwargs
    ):
        """
        Export search results to a file.

        Args:
            query: Search query
            output_file: Output file path
            format: Export format (csv, txt, efu, m3u, m3u8, tsv)
        """
        cmd = [self.es_path, query, f"-export-{format}", output_file]

        # Add other search options
        if kwargs.get("regex"):
            cmd.extend(["-regex"])
        if kwargs.get("case_sensitive"):
            cmd.extend(["-case"])
        if kwargs.get("max_results"):
            cmd.extend(["-max-results", str(kwargs["max_results"])])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Export failed: {result.stderr}")
        except Exception as e:
            raise RuntimeError(f"Error exporting results: {str(e)}")
