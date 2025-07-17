"""
File management utilities for snapshotplot.

This module handles creating output directories, generating file names,
and managing the file structure for snapshot outputs.
"""

import os
from pathlib import Path
from typing import Optional


def create_output_directory(base_dir: str, filename: str) -> str:
    """
    Create the output directory for a snapshot.
    
    Args:
        base_dir: Base directory for outputs
        filename: Name of the source file (without extension)
        
    Returns:
        str: Path to the created directory
    """
    # Clean filename (remove .py extension if present)
    if filename.endswith('.py'):
        filename = filename[:-3]
    
    # Create directory name
    dir_name = f"snapshot_{filename}"
    
    # Create full path
    output_dir = os.path.join(base_dir, dir_name)
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    return output_dir


def generate_filename(extension: str, timestamp: str) -> str:
    """
    Generate a filename with timestamp first, then type.
    
    Args:
        extension: File extension (e.g., 'py', 'png', 'html')
        timestamp: Timestamp string
        
    Returns:
        str: Generated filename
    """
    if extension == 'py':
        return f"{timestamp}_code.py"
    elif extension == 'png':
        return f"{timestamp}_plot.png"
    elif extension == 'html':
        return f"{timestamp}_snapshot.html"
    else:
        return f"{timestamp}.{extension}"


def get_file_paths(output_dir: str, filename: str, timestamp: str) -> dict:
    """
    Generate all file paths for a snapshot.
    
    Args:
        output_dir: Output directory path
        filename: Source filename
        timestamp: Timestamp string
        
    Returns:
        dict: Dictionary with paths for code, plot, and HTML files
    """
    return {
        'code': os.path.join(output_dir, generate_filename('py', timestamp)),
        'plot': os.path.join(output_dir, generate_filename('png', timestamp)),
        'html': os.path.join(output_dir, generate_filename('html', timestamp))
    }


def ensure_directory_exists(path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists
    """
    os.makedirs(path, exist_ok=True)


def get_relative_path(file_path: str, base_dir: str) -> str:
    """
    Get relative path from base directory.
    
    Args:
        file_path: Full file path
        base_dir: Base directory
        
    Returns:
        str: Relative path
    """
    try:
        return os.path.relpath(file_path, base_dir)
    except ValueError:
        # If on different drives (Windows), return absolute path
        return file_path


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be safe for filesystem and URLs.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove or replace problematic characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Replace spaces with dashes for URL-friendly names
    filename = filename.replace(' ', '-')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure it's not empty
    if not filename:
        filename = 'unnamed'
    
    return filename


def get_default_output_dir() -> str:
    """
    Get the default output directory.
    
    Returns:
        str: Default output directory path
    """
    return os.path.join(os.getcwd(), 'snapshots')


def is_valid_path(path: str) -> bool:
    """
    Check if a path is valid for the current filesystem.
    
    Args:
        path: Path to check
        
    Returns:
        bool: True if path is valid
    """
    try:
        Path(path)
        return True
    except (OSError, ValueError):
        return False 