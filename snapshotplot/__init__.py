"""
SnapshotPlot - Capture Python code, Matplotlib plots, and HTML documentation in one step.

This package provides a simple way to automatically capture and document your plotting code
with unified timestamping and beautiful HTML output.
"""

from .snapshot import snapshot, SnapshotContext

__version__ = "0.1.0"
__author__ = "SnapshotPlot Team"
__email__ = "team@snapshotplot.dev"

__all__ = ["snapshot", "SnapshotContext"]

# Optional Jupyter integration
try:
    from .jupyter_integration import (
        notebook_snapshot, 
        load_ipython_extension,
        is_notebook
    )
    __all__.extend(['notebook_snapshot', 'load_ipython_extension', 'is_notebook'])
except ImportError:
    # Jupyter/IPython not available
    pass 