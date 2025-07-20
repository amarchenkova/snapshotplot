"""
Jupyter notebook integration for snapshotplot.

This module provides IPython magic commands and notebook-specific functionality
for capturing code cells, outputs, and plots in Jupyter environments.
"""

import os
import sys
from typing import Optional, Dict, Any
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display, HTML

from .snapshot import SnapshotContext
from .timestamp import get_timestamp
from .file_manager import create_output_directory, get_file_paths, get_default_output_dir
from .html_writer import create_html_snapshot
from .utils import save_current_plot, has_active_figure, format_timestamp_for_display


def is_notebook() -> bool:
    """Check if code is running in a Jupyter notebook."""
    try:
        from IPython import get_ipython
        if 'IPKernelApp' in get_ipython().config:
            return True
    except (AttributeError, ImportError):
        pass
    return False


def get_notebook_info() -> Dict[str, Any]:
    """Get information about the current notebook."""
    try:
        from IPython import get_ipython
        ipython = get_ipython()
        
        # Try to get notebook name
        notebook_name = "Untitled"
        try:
            import ipykernel
            import json
            from pathlib import Path
            
            # Get the kernel connection file
            connection_file = Path(ipykernel.get_connection_file()).stem
            # Parse the kernel ID
            kernel_id = connection_file.split('-', 1)[1]
            
            # Try to get notebook name from Jupyter server
            try:
                from notebook import notebookapp
                servers = list(notebookapp.list_running_servers())
                for server in servers:
                    # This is a simplified approach - in practice you'd need to
                    # query the server API to match kernel_id to notebook name
                    pass
            except ImportError:
                pass
                
        except Exception:
            pass
        
        return {
            'name': notebook_name,
            'kernel': ipython.kernel.kernel_info['implementation'],
            'kernel_version': ipython.kernel.kernel_info['implementation_version']
        }
    except Exception:
        return {'name': 'Untitled', 'kernel': 'unknown', 'kernel_version': 'unknown'}


@magics_class
class SnapshotMagics(Magics):
    """IPython magic commands for snapshotplot."""
    
    @magic_arguments()
    @argument('-o', '--output-dir', help='Output directory for snapshots')
    @argument('-t', '--title', help='Title for the snapshot')
    @argument('-a', '--author', help='Author name')
    @argument('-n', '--notes', help='Additional notes')
    @argument('--dpi', type=int, default=300, help='DPI for plots')
    @argument('--site', help='Site directory for static site generation')
    @argument('--collection', help='Collection name for organizing plots')
    @argument('--tags', nargs='*', help='Tags for categorizing plots')
    @argument('--description', help='Description for the plot')
    @line_magic
    def snapshot(self, line):
        """
        Line magic to snapshot the previous cell's output.
        
        Usage:
            %snapshot -t "My Plot" -a "John Doe"
        """
        args = parse_argstring(self.snapshot, line)
        
        # Get the last executed cell
        ipython = get_ipython()
        history = list(ipython.history_manager.get_range(
            ipython.history_manager.get_last_session_id(), 
            start=-2, stop=-1
        ))
        
        if not history:
            print("No previous cell found to snapshot")
            return
        
        _, _, cell_code = history[0]
        
        # Create snapshot for the previous cell
        self._create_cell_snapshot(
            cell_code=cell_code,
            args=args,
            cell_type='previous'
        )
    
    @magic_arguments()
    @argument('-o', '--output-dir', help='Output directory for snapshots')
    @argument('-t', '--title', help='Title for the snapshot')
    @argument('-a', '--author', help='Author name')
    @argument('-n', '--notes', help='Additional notes')
    @argument('--dpi', type=int, default=300, help='DPI for plots')
    @argument('--site', help='Site directory for static site generation')
    @argument('--collection', help='Collection name for organizing plots')
    @argument('--tags', nargs='*', help='Tags for categorizing plots')
    @argument('--description', help='Description for the plot')
    @cell_magic
    def snapshot(self, line, cell):
        """
        Cell magic to snapshot the current cell.
        
        Usage:
            %%snapshot -t "My Analysis" -a "John Doe"
            import matplotlib.pyplot as plt
            plt.plot([1, 2, 3], [1, 4, 9])
            plt.show()
        """
        args = parse_argstring(self.snapshot, line)
        
        # Execute the cell first
        ipython = get_ipython()
        result = ipython.run_cell(cell)
        
        # Create snapshot after execution
        if result.success:
            self._create_cell_snapshot(
                cell_code=cell,
                args=args,
                cell_type='current'
            )
        else:
            print("Cell execution failed, snapshot not created")
    
    def _create_cell_snapshot(self, cell_code: str, args, cell_type: str):
        """Create a snapshot for a notebook cell."""
        # Get notebook info
        notebook_info = get_notebook_info()
        
        # Prepare configuration
        config = {
            'output_dir': args.output_dir,
            'title': args.title,
            'author': args.author,
            'notes': args.notes,
            'dpi': args.dpi,
            'site': args.site,
            'collection': args.collection,
            'tags': args.tags or [],
            'description': args.description
        }
        
        # Remove None values
        config = {k: v for k, v in config.items() if v is not None}
        
        # Get timestamp
        timestamp = get_timestamp()
        
        # Set up output directory
        output_dir = config.get('output_dir') or get_default_output_dir()
        snapshot_dir = create_output_directory(output_dir, notebook_info['name'])
        file_paths = get_file_paths(snapshot_dir, notebook_info['name'], timestamp)
        
        # Save cell code
        with open(file_paths['code'], 'w', encoding='utf-8') as f:
            f.write(cell_code)
        
        # Save plot if available
        plot_saved = False
        if has_active_figure():
            try:
                save_current_plot(
                    file_paths['plot'],
                    dpi=config.get('dpi', 300),
                    bbox_inches='tight'
                )
                plot_saved = True
            except Exception as e:
                print(f"Failed to save plot: {e}")
        
        # Create HTML documentation
        metadata = {
            'function_name': f'Cell from {notebook_info["name"]}',
            'filename': notebook_info['name'],
            'date': format_timestamp_for_display(timestamp),
            'notebook': True,
            'kernel': notebook_info['kernel'],
            'kernel_version': notebook_info['kernel_version']
        }
        
        plot_path = file_paths['plot'] if plot_saved else ''
        create_html_snapshot(
            code=cell_code,
            plot_path=plot_path,
            html_path=file_paths['html'],
            metadata=metadata,
            title=config.get('title'),
            author=config.get('author'),
            notes=config.get('notes')
        )
        
        # Display success message with link
        display(HTML(f'''
        <div style="background: #2a2a2a; color: #e0e0e0; padding: 10px; border-radius: 5px; margin: 10px 0;">
            📸 Snapshot created: <a href="{file_paths['html']}" target="_blank" style="color: #4CAF50;">
            {os.path.basename(file_paths['html'])}</a>
        </div>
        '''))


def load_ipython_extension(ipython):
    """Load the IPython extension."""
    ipython.register_magic_function(SnapshotMagics(ipython).snapshot, 'line_cell')


def unload_ipython_extension(ipython):
    """Unload the IPython extension."""
    pass


class NotebookSnapshot(SnapshotContext):
    """
    Enhanced snapshot context for Jupyter notebooks.
    
    Automatically captures cell metadata and handles notebook-specific features.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notebook_info = get_notebook_info() if is_notebook() else None
    
    def __enter__(self):
        """Enhanced enter for notebook context."""
        # If in notebook, capture current cell info
        if self.notebook_info:
            # Store the fact that we're in a notebook
            self.calling_info = {
                'function_name': f'Notebook: {self.notebook_info["name"]}',
                'filename': self.notebook_info['name'],
                'source_code': self._get_current_cell_code()
            }
        return super().__enter__()
    
    def _get_current_cell_code(self) -> str:
        """Get the code from the currently executing cell."""
        try:
            from IPython import get_ipython
            ipython = get_ipython()
            
            # Get the current cell's input
            # This is a simplified approach - in practice you might need
            # more sophisticated cell tracking
            if hasattr(ipython, 'user_ns') and '__code__' in ipython.user_ns:
                return ipython.user_ns['__code__']
            
            # Fallback to last input
            return ipython.history_manager.input_hist_parsed[-1]
        except Exception:
            return "# Could not capture cell code"


def notebook_snapshot(*args, **kwargs):
    """
    Create a notebook-aware snapshot context.
    
    This function automatically detects if running in a Jupyter notebook
    and provides enhanced functionality for that environment.
    """
    if is_notebook():
        return NotebookSnapshot(*args, **kwargs)
    else:
        # Fall back to regular snapshot
        from .snapshot import snapshot
        return snapshot(*args, **kwargs)