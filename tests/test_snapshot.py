"""
Tests for snapshotplot package.

This module contains basic tests to verify the core functionality.
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from snapshotplot import snapshot, SnapshotContext
from snapshotplot.timestamp import get_timestamp, reset_timestamp
from snapshotplot.code_capture import get_calling_info
from snapshotplot.file_manager import create_output_directory, get_file_paths


class TestTimestamp:
    """Test timestamp functionality."""
    
    def test_timestamp_generation(self):
        """Test that timestamps are generated correctly."""
        reset_timestamp()
        timestamp1 = get_timestamp()
        timestamp2 = get_timestamp()
        
        # Same timestamp should be returned until reset
        assert timestamp1 == timestamp2
        
        # Timestamp should have correct format
        assert len(timestamp1) == 19  # YYYYMMDD_HHMMSS_milliseconds (3 digits)
        assert timestamp1[8] == '_'
        assert timestamp1[15] == '_'
    
    def test_timestamp_reset(self):
        """Test that timestamps reset correctly."""
        timestamp1 = get_timestamp()
        reset_timestamp()
        timestamp2 = get_timestamp()
        
        # Different timestamps after reset
        assert timestamp1 != timestamp2


class TestCodeCapture:
    """Test code capture functionality."""
    
    def test_get_calling_info(self):
        """Test that calling info is captured correctly."""
        info = get_calling_info()
        
        # Should have required keys
        required_keys = ['function_name', 'filename', 'source_code']
        for key in required_keys:
            assert key in info
        
        # Should have valid values
        assert isinstance(info['function_name'], str)
        assert isinstance(info['filename'], str)
        assert isinstance(info['source_code'], str)


class TestFileManager:
    """Test file management functionality."""
    
    def test_create_output_directory(self, tmp_path):
        """Test output directory creation."""
        base_dir = str(tmp_path)
        filename = "test_file.py"
        
        output_dir = create_output_directory(base_dir, filename)
        
        # Should create directory
        assert os.path.exists(output_dir)
        assert os.path.isdir(output_dir)
        
        # Should have correct name
        expected_name = "snapshot_test_file"
        assert os.path.basename(output_dir) == expected_name
    
    def test_get_file_paths(self, tmp_path):
        """Test file path generation."""
        output_dir = str(tmp_path)
        filename = "test.py"
        timestamp = "20241201_143022_123456"
        
        paths = get_file_paths(output_dir, filename, timestamp)
        
        # Should have all required paths
        required_paths = ['code', 'plot', 'html']
        for path_type in required_paths:
            assert path_type in paths
        
        # Should have correct filenames
        assert paths['code'].endswith(f"{timestamp}_code.py")
        assert paths['plot'].endswith(f"{timestamp}_plot.png")
        assert paths['html'].endswith(f"{timestamp}_snapshot.html")


class TestSnapshotContext:
    """Test SnapshotContext functionality."""
    
    def test_context_manager_creation(self):
        """Test that SnapshotContext can be created."""
        context = SnapshotContext()
        assert context is not None
        assert hasattr(context, 'config')
    
    def test_context_manager_with_custom_config(self):
        """Test SnapshotContext with custom configuration."""
        context = SnapshotContext(
            output_dir="custom_dir",
            title="Test Title",
            author="Test Author",
            notes="Test Notes"
        )
        
        assert context.config['output_dir'] == "custom_dir"
        assert context.config['title'] == "Test Title"
        assert context.config['author'] == "Test Author"
        assert context.config['notes'] == "Test Notes"


class TestSnapshotDecorator:
    """Test snapshot decorator functionality."""
    
    def test_decorator_creation(self):
        """Test that snapshot decorator can be created."""
        decorator = snapshot()
        assert callable(decorator)
    
    def test_decorator_with_custom_config(self):
        """Test snapshot decorator with custom configuration."""
        decorator = snapshot(
            output_dir="test_dir",
            title="Test Title",
            author="Test Author"
        )
        assert callable(decorator)


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    @patch('matplotlib.pyplot.gcf')
    @patch('matplotlib.pyplot.savefig')
    def test_basic_snapshot_workflow(self, mock_savefig, mock_gcf, tmp_path):
        """Test basic snapshot workflow with mocked matplotlib."""
        # Mock matplotlib figure
        mock_fig = MagicMock()
        mock_fig.axes = [MagicMock()]  # Simulate axes
        mock_gcf.return_value = mock_fig
        
        # Create temporary directory
        test_dir = str(tmp_path / "test_snapshots")
        
        # Test context manager
        with SnapshotContext(output_dir=test_dir):
            # Simulate some code execution
            pass
        
        # Check that directory was created
        assert os.path.exists(test_dir)
        
        # Check that files were created (at least HTML and code)
        files = os.listdir(test_dir)
        assert len(files) > 0
        
        # Should have at least one snapshot directory
        snapshot_dirs = [f for f in files if f.startswith('snapshot_')]
        assert len(snapshot_dirs) > 0


if __name__ == "__main__":
    pytest.main([__file__]) 