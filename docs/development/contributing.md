# Contributing Guide

## Welcome Contributors

Thank you for your interest in contributing to Everything Search Python! This guide will help you get started with development, testing, and submitting contributions.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Poetry (recommended) or pip
- Everything Search installed and running
- Git for version control

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/pakkio/es.git
cd es

# Install dependencies with Poetry
poetry install --with dev

# Or with pip
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Development Environment

```bash
# Activate virtual environment (Poetry)
poetry shell

# Or create virtual environment (pip)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install in development mode
pip install -e .
```

## Project Structure

```
es/
├── everything_search.py    # Core wrapper class
├── mcp_server.py          # MCP server implementation
├── start_mcp_server.py    # MCP server launcher
├── tests/                 # Unit tests
│   ├── test_everything_search.py
│   └── __init__.py
├── docs/                  # Documentation
│   ├── api/
│   ├── guides/
│   └── development/
├── pyproject.toml         # Project configuration
├── README.md             # Main readme
├── CLAUDE.md             # Development context
└── LICENSE               # MIT license
```

## Code Standards

### Code Style

We use Black for code formatting and isort for import sorting:

```bash
# Format code
black .
isort .

# Check formatting
black --check .
isort --check-only .
```

### Type Hints

All public functions must have type hints:

```python
def search_files(
    self, 
    query: str = "", 
    **kwargs
) -> List[Dict[str, Union[str, int]]]:
    """Search for files with type hints."""
    pass
```

### Documentation

All public methods require docstrings:

```python
def search_by_size(self, size_filter: str, **kwargs) -> List[Dict[str, Union[str, int]]]:
    """
    Search for files by size.

    Args:
        size_filter: Size filter (e.g., ">100MB", "<1KB", "1GB..5GB")
        **kwargs: Additional search parameters

    Returns:
        List of dictionaries containing search results

    Raises:
        RuntimeError: If Everything Search fails
        TimeoutError: If search exceeds timeout

    Example:
        >>> es = EverythingSearch()
        >>> large_files = es.search_by_size(">1GB", max_results=10)
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=everything_search --cov-report=html

# Run specific test file
pytest tests/test_everything_search.py

# Run with verbose output
pytest -v
```

### Test Categories

1. **Unit Tests** - Test individual methods
2. **Integration Tests** - Test with real Everything Search
3. **MCP Tests** - Test MCP server functionality

### Writing Tests

```python
import pytest
from everything_search import EverythingSearch

class TestEverythingSearch:
    """Test suite for EverythingSearch class."""
    
    def test_initialization(self):
        """Test class initialization."""
        es = EverythingSearch()
        assert es.es_path.endswith("es.exe")
    
    def test_search_basic(self):
        """Test basic search functionality."""
        es = EverythingSearch()
        results = es.search("*.py", max_results=5)
        assert isinstance(results, list)
        assert len(results) <= 5
    
    @pytest.mark.integration
    def test_search_with_everything_running(self):
        """Integration test requiring Everything Search."""
        # This test requires Everything Search to be running
        pass
```

### Test Fixtures

Use pytest fixtures for common setup:

```python
@pytest.fixture
def es_instance():
    """Provide EverythingSearch instance for tests."""
    return EverythingSearch()

@pytest.fixture
def sample_search_results():
    """Provide sample search results for testing."""
    return [
        {"Name": "test.py", "Size": 1024},
        {"Name": "example.txt", "Size": 512}
    ]

def test_with_fixture(es_instance, sample_search_results):
    """Test using fixtures."""
    assert len(sample_search_results) == 2
```

## MCP Server Development

### Testing MCP Server

```bash
# Test MCP server directly
python test_mcp.py

# Start MCP server manually
python start_mcp_server.py

# Test individual MCP tools
python -c "
from mcp_server import search_files
result = search_files('*.py', max_results=5)
print(result)
"
```

### Adding New MCP Tools

1. **Add tool to mcp_server.py**:

```python
@mcp.tool()
def new_search_tool(
    parameter: str,
    max_results: int = 20,
    timeout: int = 30000,
) -> str:
    """
    Description of the new tool.
    
    Args:
        parameter: Description of parameter
        max_results: Maximum results to return
        timeout: Search timeout in milliseconds
    
    Returns:
        JSON string containing search results
    """
    try:
        es = get_everything_search()
        results = es.some_method(parameter, max_results=max_results, timeout=timeout)
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})
```

2. **Add corresponding method to EverythingSearch class**:

```python
def some_method(self, parameter: str, **kwargs) -> List[Dict[str, Union[str, int]]]:
    """Implementation of the new search functionality."""
    # Implementation here
    pass
```

3. **Add tests**:

```python
def test_new_search_tool():
    """Test the new search functionality."""
    # Test implementation
    pass
```

## Performance Considerations

### Optimization Guidelines

1. **Subprocess Efficiency**
   - Minimize subprocess calls
   - Use appropriate timeouts
   - Handle encoding properly

2. **Memory Management**
   - Use generators for large result sets
   - Implement pagination
   - Clean up temporary files

3. **Error Handling**
   - Provide meaningful error messages
   - Handle edge cases gracefully
   - Log errors appropriately

### Benchmarking

```python
import time
from everything_search import EverythingSearch

def benchmark_search(query, iterations=10):
    """Benchmark search performance."""
    es = EverythingSearch()
    
    times = []
    for _ in range(iterations):
        start = time.time()
        results = es.search(query, max_results=100)
        end = time.time()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    print(f"Average search time: {avg_time:.3f}s")
    print(f"Results per second: {100 / avg_time:.1f}")

# Usage
benchmark_search("*.py")
```

## Contribution Workflow

### 1. Issue Creation

Before coding, create an issue describing:
- Problem or feature request
- Expected behavior
- Current behavior (if bug)
- Proposed solution

### 2. Branch Creation

```bash
# Create feature branch
git checkout -b feature/description

# Or bug fix branch
git checkout -b fix/issue-number
```

### 3. Development

```bash
# Make changes
# Write tests
# Update documentation

# Run tests
pytest

# Check code quality
black --check .
isort --check-only .
mypy everything_search.py
flake8
```

### 4. Commit Guidelines

Use conventional commit messages:

```bash
# Feature
git commit -m "feat: add search by date range functionality"

# Bug fix
git commit -m "fix: handle UTF-8 encoding in file names"

# Documentation
git commit -m "docs: update API documentation for new methods"

# Tests
git commit -m "test: add integration tests for MCP server"

# Refactor
git commit -m "refactor: improve error handling in search method"
```

### 5. Pull Request

1. **Create PR** with clear description
2. **Link related issues**
3. **Provide test results**
4. **Update documentation** if needed

#### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes (or marked as such)
```

## Code Review Process

### For Contributors

1. **Self-review**: Check your own code first
2. **Test coverage**: Ensure adequate test coverage
3. **Documentation**: Update docs for public API changes
4. **Breaking changes**: Mark and document breaking changes

### For Reviewers

1. **Functionality**: Does it work as intended?
2. **Code quality**: Follows project standards?
3. **Tests**: Adequate test coverage?
4. **Documentation**: Clear and complete?
5. **Performance**: No performance regressions?

## Release Process

### Version Numbering

We use semantic versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Release Checklist

1. **Update version** in `pyproject.toml`
2. **Update changelog** with new features/fixes
3. **Run full test suite**
4. **Build package**: `poetry build`
5. **Create release tag**: `git tag v1.2.3`
6. **Push to repository**: `git push --tags`
7. **Publish to PyPI**: `poetry publish`

## Security Guidelines

### Secure Coding Practices

1. **Input validation**: Sanitize all user inputs
2. **Path traversal**: Prevent directory traversal attacks
3. **Command injection**: Use subprocess safely
4. **Error handling**: Don't expose sensitive information

### Security Review

```python
# Example of secure subprocess usage
def safe_subprocess_call(command_args):
    """Safely execute subprocess command."""
    try:
        # Use list format, not string
        result = subprocess.run(
            command_args,  # List, not string
            capture_output=True,
            text=True,
            timeout=30,  # Always set timeout
            check=True   # Raise on non-zero exit
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise TimeoutError("Command timed out")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e}")
```

## Documentation

### Documentation Standards

1. **API docs**: Complete parameter descriptions
2. **Examples**: Working code examples
3. **Error handling**: Document exceptions
4. **Type hints**: Include in all signatures

### Building Documentation

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme

# Build documentation
cd docs
make html

# View locally
open _build/html/index.html
```

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's coding standards

### Getting Help

- **Documentation**: Check existing docs first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions for questions
- **Code review**: Ask for specific feedback

### Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- GitHub contributors page

## Troubleshooting Development Issues

### Common Issues

1. **Tests fail on Windows/WSL**
   - Ensure Everything Search is running
   - Check file paths in tests
   - Verify WSL mount points

2. **Import errors**
   - Check virtual environment activation
   - Reinstall in development mode: `pip install -e .`

3. **Pre-commit hooks fail**
   - Run formatters manually: `black . && isort .`
   - Fix linting issues: `flake8`

4. **MCP server connection issues**
   - Check Python path in config
   - Verify file permissions
   - Test server manually

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from everything_search import EverythingSearch
es = EverythingSearch()
# Debug output will show subprocess calls
```

## Next Steps

After setting up development environment:

1. **Pick an issue** from GitHub Issues
2. **Join discussions** in GitHub Discussions
3. **Read the code** to understand architecture
4. **Write tests** for your changes
5. **Submit a PR** following guidelines

Thank you for contributing to Everything Search Python! 🎉