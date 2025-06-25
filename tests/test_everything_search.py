"""
Tests for EverythingSearch wrapper.
"""

import os
import tempfile
from unittest.mock import MagicMock, Mock, patch

import pytest

from everything_search import EverythingSearch


class TestEverythingSearch:
    """Test cases for EverythingSearch class."""

    def test_initialization_with_default_path(self):
        """Test initialization with default es.exe path."""
        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            assert es.es_path == "/mnt/c/Program Files/Everything/es.exe"

    def test_initialization_with_custom_path(self):
        """Test initialization with custom es.exe path."""
        custom_path = "/custom/path/es.exe"
        with patch("os.path.exists", return_value=True):
            es = EverythingSearch(custom_path)
            assert es.es_path == custom_path

    def test_initialization_file_not_found(self):
        """Test initialization raises FileNotFoundError when es.exe not found."""
        with patch("os.path.exists", return_value=False):
            with pytest.raises(FileNotFoundError):
                EverythingSearch("/nonexistent/path/es.exe")

    @patch("subprocess.run")
    def test_get_version(self, mock_run):
        """Test get_version method."""
        mock_run.return_value = Mock(stdout="1.1.0.30", returncode=0)

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            version = es.get_version()

        assert version == "1.1.0.30"
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_get_result_count(self, mock_run):
        """Test get_result_count method."""
        mock_run.return_value = Mock(stdout="42", returncode=0)

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            count = es.get_result_count("*.txt")

        assert count == 42
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_search_basic(self, mock_run):
        """Test basic search functionality."""
        csv_output = "Filename\ntest.txt\nexample.py"
        mock_run.return_value = Mock(stdout=csv_output, returncode=0, stderr="")

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            results = es.search("test")

        assert len(results) == 2
        assert results[0]["Filename"] == "test.txt"
        assert results[1]["Filename"] == "example.py"

    @patch("subprocess.run")
    def test_search_with_options(self, mock_run):
        """Test search with various options."""
        csv_output = "Filename,Size\ntest.txt,1024"
        mock_run.return_value = Mock(stdout=csv_output, returncode=0, stderr="")

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            results = es.search(
                "test", case_sensitive=True, max_results=10, include_size=True
            )

        assert len(results) == 1
        assert results[0]["Filename"] == "test.txt"
        assert results[0]["Size"] == 1024

    @patch("subprocess.run")
    def test_search_files_only(self, mock_run):
        """Test search_files method."""
        csv_output = "Filename\ntest.txt"
        mock_run.return_value = Mock(stdout=csv_output, returncode=0, stderr="")

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            results = es.search_files("test")

        assert len(results) == 1
        assert results[0]["Filename"] == "test.txt"

    @patch("subprocess.run")
    def test_search_folders_only(self, mock_run):
        """Test search_folders method."""
        csv_output = "Filename\ntest_folder"
        mock_run.return_value = Mock(stdout=csv_output, returncode=0, stderr="")

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            results = es.search_folders("test")

        assert len(results) == 1
        assert results[0]["Filename"] == "test_folder"

    @patch("subprocess.run")
    def test_search_by_extension(self, mock_run):
        """Test search_by_extension method."""
        csv_output = "Filename\ntest.py\nexample.py"
        mock_run.return_value = Mock(stdout=csv_output, returncode=0, stderr="")

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            results = es.search_by_extension("py")

        assert len(results) == 2
        assert results[0]["Filename"] == "test.py"
        assert results[1]["Filename"] == "example.py"

    def test_parse_csv_output_empty(self):
        """Test _parse_csv_output with empty input."""
        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            results = es._parse_csv_output("")

        assert results == []

    def test_parse_csv_output_with_size(self):
        """Test _parse_csv_output with size conversion."""
        csv_output = "Filename,Size\ntest.txt,1024\nexample.py,abc"

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            results = es._parse_csv_output(csv_output)

        assert len(results) == 2
        assert results[0]["Size"] == 1024
        assert results[1]["Size"] == "abc"  # Non-numeric size stays as string

    @patch("subprocess.run")
    def test_search_error_handling(self, mock_run):
        """Test error handling in search method."""
        mock_run.return_value = Mock(returncode=1, stderr="Error occurred")

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            with pytest.raises(RuntimeError, match="Everything Search failed"):
                es.search("test")

    @patch("subprocess.run")
    def test_export_results(self, mock_run):
        """Test export_results method."""
        mock_run.return_value = Mock(returncode=0, stderr="")

        with patch("os.path.exists", return_value=True):
            es = EverythingSearch()
            es.export_results("*.txt", "/tmp/output.csv", "csv")

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "-export-csv" in args
        assert "/tmp/output.csv" in args
