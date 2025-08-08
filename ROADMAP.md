# SnapshotPlot Roadmap

## Current Status Analysis (July 2025)

### Dependencies Status ✅
All core dependencies are current and compatible:
- matplotlib 3.10.3 ✅
- jinja2 3.1.6 ✅  
- pygments 2.19.2 ✅

### Critical Issues

#### 🚨 Python 3.8 End of Life
**Status**: Critical - Immediate Action Required
**Issue**: Python 3.8 reached end-of-life in October 2024
**Impact**: Security vulnerabilities will not be patched
**Action**: Update minimum Python requirement to 3.9+

## Immediate Updates Required

### 1. Python Version Requirements
**Priority**: Critical
**Files**: `pyproject.toml`
- Update `requires-python = ">=3.8"` to `requires-python = ">=3.9"`
- Update classifiers to remove Python 3.8 support
- Add Python 3.13 support in classifiers

### 2. Dependency Minimum Versions
**Priority**: High
**Files**: `pyproject.toml`
Update to leverage newer features and security fixes:
- `matplotlib>=3.7.0` (current: `>=3.5.0`)
- `jinja2>=3.1.0` (current: `>=3.0.0`)
- `pygments>=2.15.0` (current: `>=2.10.0`)

### 3. Test and Docs Alignment
**Priority**: High
**Files**: `tests/test_snapshot.py`, `README.md`
- Align snapshot filename convention between tests and implementation
- Update README to mark `%snapshot` line magic as experimental or implement it

### 4. Code Modernization

#### Path Handling Modernization
**Priority**: High
**Files**: `snapshotplot/file_manager.py`
**Issue**: Using deprecated `os.path` instead of modern `pathlib.Path`
**Impact**: Better cross-platform compatibility and cleaner code

**Current Code**:
```python
output_dir = os.path.join(base_dir, dir_name)
'code': os.path.join(output_dir, generate_filename('py', timestamp))
```

**Recommended Fix**:
```python
from pathlib import Path
output_dir = Path(base_dir) / dir_name
'code': output_dir / generate_filename('py', timestamp)
```

#### Type Hints Completion
**Priority**: Medium
**Files**: `snapshotplot/snapshot.py`
**Issue**: Missing type hints in magic methods

**Current Code**:
```python
def __enter__(self):
def __exit__(self, exc_type, exc_val, exc_tb):
```

**Recommended Fix**:
```python
def __enter__(self) -> 'SnapshotContext':
def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
```

#### Security Enhancement
**Priority**: High
**Files**: `snapshotplot/html_writer.py`
**Issue**: Jinja2 templates should use `autoescape=True` for security

**Current Code**:
```python
template = Template(HTML_TEMPLATE)
```

**Recommended Fix**:
```python
from jinja2 import Environment, BaseLoader
env = Environment(loader=BaseLoader(), autoescape=True)
template = env.from_string(HTML_TEMPLATE)
```

#### Global State Management
**Priority**: Medium
**Files**: `snapshotplot/timestamp.py`
**Issue**: Global variables could cause issues in multi-threaded environments

**Current Code**:
```python
_GLOBAL_TIMESTAMP: Optional[str] = None
_GLOBAL_DATETIME: Optional[datetime] = None
```

**Recommended Fix**:
```python
import threading
_thread_local = threading.local()
```

## Feature Enhancements

### Phase 1: Core Improvements (1-2 weeks)
1. **Multi-plot Support**
   - Currently only captures single matplotlib figures
   - Add support for multiple figures in a single snapshot
   - Modify `utils.py` to detect and save all active figures

2. **Enhanced Error Handling**
   - Replace generic `warnings.warn()` with proper logging
   - Add specific exception types with helpful messages
   - Implement detailed error messages with suggested fixes

3. **Configuration System**
   - Add support for `.snapshotplot.toml` project-level configuration
   - Implement pydantic models for configuration validation
   - Better configuration defaults and validation

### Phase 2: Extended Features (1 month)
1. **Interactive Plot Support**
   - Add support for Plotly, Bokeh, and other interactive plotting libraries
   - Create plugin architecture for different plot types
   - Maintain backward compatibility with matplotlib

2. **Enhanced Code Context**
   - Capture relevant code blocks, imports, and dependencies
   - Use AST analysis for better code understanding
   - Include environment details and package versions

3. **Template System**
   - Support for custom HTML templates and themes
   - Extend `html_writer.py` with template engine
   - Dark/light mode options

### Phase 3: Advanced Features (2-3 months)
1. **Export Formats**
   - Add PDF, Markdown, and Jupyter notebook export options
   - Create export plugin system
   - Maintain HTML as primary format

2. **CLI Interface**
   - Command-line tool for batch processing
   - Configuration management via CLI
   - Progress indicators for long-running operations

3. **Performance Optimizations**
   - Lazy loading for heavy dependencies
   - Async support for file operations
   - Memory management for matplotlib figures

### Phase 4: Integrations (3-6 months)
1. **Jupyter Notebook Integration**
   - Native Jupyter support for cell-level snapshots
   - Jupyter magic commands
   - Seamless integration with data science workflows

2. **Version Control Integration**
   - Git hooks for automatic snapshot creation
   - Automatic documentation of plot changes
   - Integration with CI/CD pipelines

3. **Cloud Storage Integration**
   - Direct upload to S3, GCS, Azure Blob
   - Centralized snapshot storage and sharing
   - Team collaboration features

## Testing & Quality Improvements

### Immediate Testing Needs
1. **Integration Tests**
   - Comprehensive integration tests between modules
   - End-to-end testing scenarios
   - Cross-platform compatibility tests

2. **Performance Tests**
   - Performance regression tests
   - Memory usage optimization
   - Benchmarking against large datasets

3. **Security Tests**
   - Template injection prevention
   - Path traversal attack prevention
   - Input validation testing

### Code Quality
1. **Documentation**
   - Add Sphinx documentation with full API reference
   - Comprehensive tutorials and examples
   - Best practices guide

2. **Type Safety**
   - Complete type hint coverage
   - mypy configuration improvements
   - Runtime type checking options

## Migration Guide

### For Users
1. **Python Version Update**
   - Ensure Python 3.9+ is installed
   - Test existing code with new version
   - Update CI/CD pipelines

2. **API Changes**
   - Most changes will be backward compatible
   - New features will be opt-in
   - Deprecation warnings for removed features

### For Contributors
1. **Development Environment**
   - Update Python version requirements
   - New pre-commit hooks for code quality
   - Enhanced testing requirements

2. **Code Standards**
   - Use `pathlib.Path` for all file operations
   - Complete type hints required
   - Security-first approach for templates

## Timeline Summary

| Phase | Timeline | Focus |
|-------|----------|--------|
| **Critical Updates** | 1-2 weeks | Python 3.9+, security fixes, path handling |
| **Phase 1** | 1 month | Multi-plot, error handling, configuration |
| **Phase 2** | 2 months | Interactive plots, enhanced context, templates |
| **Phase 3** | 3 months | Export formats, CLI, performance |
| **Phase 4** | 6 months | Jupyter integration, version control, cloud |

## Success Metrics

- **Security**: All templates use autoescape, no security vulnerabilities
- **Performance**: 50% faster file operations with pathlib
- **Usability**: Support for 3+ plotting libraries beyond matplotlib
- **Adoption**: CLI tool and Jupyter integration increase user base
- **Quality**: 95%+ test coverage, comprehensive documentation

## Breaking Changes

### Version 0.2.0 (Next Release)
- **Python 3.8 support dropped** (EOL)
- **Minimum dependency versions updated**
- **Path handling changes** (internal, should not affect users)
- **Template security improvements** (may affect custom templates)

### Version 0.3.0 (Future)
- **New configuration system** (backward compatible)
- **Enhanced API for multi-plot support**
- **Plugin architecture for plot types**

---

*This roadmap is a living document and will be updated as features are implemented and priorities change.*