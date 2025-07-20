"""
Static site generator for SnapshotPlot.
"""

import os
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown


class SiteGenerator:
    """Generate static site from plot collections."""
    
    def __init__(self, site_dir: str):
        self.site_dir = Path(site_dir)
        self.config_path = self.site_dir / '_config.yml'
        self.config = self._load_config()
        
        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader([
                str(self.site_dir / '_layouts'),
                str(self.site_dir / '_includes')
            ]),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Add custom filters
        self.env.filters['dateformat'] = self._date_format
        self.env.filters['slugify'] = self._slugify
    
    def _load_config(self) -> Dict[str, Any]:
        """Load site configuration."""
        if not self.config_path.exists():
            return {}
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    
    def _date_format(self, date_str: str, format: str = '%B %d, %Y') -> str:
        """Format date string."""
        if isinstance(date_str, str):
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            date_obj = date_str
        return date_obj.strftime(format)
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        import re
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        return re.sub(r'[-\s]+', '-', text)
    
    def get_all_plots(self) -> List[Dict[str, Any]]:
        """Get all plots from all collections."""
        plots = []
        collections_dir = self.site_dir / 'collections'
        
        if not collections_dir.exists():
            return plots
        
        for collection_dir in collections_dir.iterdir():
            if not collection_dir.is_dir():
                continue
                
            collection_name = collection_dir.name
            
            for plot_dir in collection_dir.iterdir():
                if not plot_dir.is_dir() or plot_dir.name.startswith('_'):
                    continue
                
                plot_metadata = self._load_plot_metadata(plot_dir)
                if plot_metadata:
                    plot_metadata['collection'] = collection_name
                    plot_metadata['slug'] = plot_dir.name
                    plots.append(plot_metadata)
        
        # Sort by date (newest first)
        plots.sort(key=lambda x: x.get('date', ''), reverse=True)
        return plots
    
    def _load_plot_metadata(self, plot_dir: Path) -> Optional[Dict[str, Any]]:
        """Load metadata for a single plot."""
        index_file = plot_dir / 'index.md'
        
        if not index_file.exists():
            # Try to auto-generate from files
            return self._auto_generate_metadata(plot_dir)
        
        with open(index_file, 'r') as f:
            content = f.read()
        
        # Parse front matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = yaml.safe_load(parts[1])
                markdown_content = parts[2].strip()
                
                # Process markdown
                front_matter['content'] = markdown.markdown(markdown_content)
                return front_matter
        
        return None
    
    def _auto_generate_metadata(self, plot_dir: Path) -> Optional[Dict[str, Any]]:
        """Auto-generate metadata from plot directory."""
        # Look for common file patterns
        plot_files = list(plot_dir.glob('*.png')) + list(plot_dir.glob('*.jpg'))
        code_files = list(plot_dir.glob('*.py')) + list(plot_dir.glob('*.ipynb'))
        
        if not plot_files:
            return None
        
        # Extract timestamp from directory name
        dir_name = plot_dir.name
        timestamp_parts = dir_name.split('_')
        
        if len(timestamp_parts) >= 2:
            try:
                date_str = timestamp_parts[0]
                time_str = timestamp_parts[1]
                datetime_obj = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                date_iso = datetime_obj.isoformat()
            except ValueError:
                date_iso = datetime.now().isoformat()
        else:
            date_iso = datetime.now().isoformat()
        
        return {
            'title': dir_name.replace('_', ' ').title(),
            'date': date_iso,
            'plot_image': plot_files[0].name,
            'code_file': code_files[0].name if code_files else None,
            'auto_generated': True
        }
    
    def build(self, output_dir: str = 'docs', verbose: bool = False):
        """Build the static site."""
        output_path = Path(output_dir)
        
        # Clean output directory
        if output_path.exists():
            shutil.rmtree(output_path)
        output_path.mkdir(parents=True)
        
        # Copy assets
        self._copy_assets(output_path)
        
        # Get all plots
        plots = self.get_all_plots()
        
        # Build index page
        self._build_index(plots, output_path, verbose)
        
        # Build collection pages
        self._build_collections(plots, output_path, verbose)
        
        # Build individual plot pages
        self._build_plot_pages(plots, output_path, verbose)
        
        if verbose:
            print(f"✅ Built {len(plots)} plots across {len(self.config.get('collections', {}))} collections")
    
    def _copy_assets(self, output_path: Path):
        """Copy static assets to output directory."""
        assets_dir = self.site_dir / 'assets'
        if assets_dir.exists():
            shutil.copytree(assets_dir, output_path / 'assets', dirs_exist_ok=True)
        
        # Copy plot images and files
        collections_dir = self.site_dir / 'collections'
        if collections_dir.exists():
            for collection_dir in collections_dir.iterdir():
                if not collection_dir.is_dir():
                    continue
                
                collection_output = output_path / collection_dir.name
                collection_output.mkdir(parents=True, exist_ok=True)
                
                for plot_dir in collection_dir.iterdir():
                    if not plot_dir.is_dir() or plot_dir.name.startswith('_'):
                        continue
                    
                    plot_output = collection_output / plot_dir.name
                    plot_output.mkdir(parents=True, exist_ok=True)
                    
                    # Copy plot files
                    for file in plot_dir.iterdir():
                        if file.is_file() and not file.name.endswith('.md'):
                            shutil.copy2(file, plot_output / file.name)
    
    def _build_index(self, plots: List[Dict[str, Any]], output_path: Path, verbose: bool):
        """Build the main index page."""
        template = self.env.get_template('default.html')
        
        # Group plots by collection
        collections = {}
        for plot in plots:
            collection = plot['collection']
            if collection not in collections:
                collections[collection] = []
            collections[collection].append(plot)
        
        html = template.render(
            site=self.config,
            plots=plots[:12],  # Show latest 12 plots
            collections=collections,
            page_title="Home",
            is_index=True,
            base_path=""
        )
        
        with open(output_path / 'index.html', 'w') as f:
            f.write(html)
        
        if verbose:
            print(f"✅ Built index page with {len(plots)} plots")
    
    def _build_collections(self, plots: List[Dict[str, Any]], output_path: Path, verbose: bool):
        """Build collection gallery pages."""
        template = self.env.get_template('gallery.html')
        
        # Group plots by collection
        collections = {}
        for plot in plots:
            collection = plot['collection']
            if collection not in collections:
                collections[collection] = []
            collections[collection].append(plot)
        
        for collection_name, collection_plots in collections.items():
            # Load collection metadata
            collection_meta = self._load_collection_metadata(collection_name)
            
            html = template.render(
                site=self.config,
                collection=collection_meta,
                plots=collection_plots,
                page_title=collection_meta.get('title', collection_name),
                base_path=".."
            )
            
            collection_output = output_path / collection_name
            collection_output.mkdir(parents=True, exist_ok=True)
            
            with open(collection_output / 'index.html', 'w') as f:
                f.write(html)
            
            if verbose:
                print(f"✅ Built collection '{collection_name}' with {len(collection_plots)} plots")
    
    def _load_collection_metadata(self, collection_name: str) -> Dict[str, Any]:
        """Load metadata for a collection."""
        collection_dir = self.site_dir / 'collections' / collection_name
        index_file = collection_dir / '_index.md'
        
        if index_file.exists():
            with open(index_file, 'r') as f:
                content = f.read()
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    metadata = yaml.safe_load(parts[1])
                    metadata['content'] = markdown.markdown(parts[2].strip())
                    return metadata
        
        # Default metadata
        return {
            'title': collection_name.replace('-', ' ').title(),
            'description': f'Plot collection for {collection_name}',
            'name': collection_name
        }
    
    def _build_plot_pages(self, plots: List[Dict[str, Any]], output_path: Path, verbose: bool):
        """Build individual plot pages."""
        template = self.env.get_template('plot.html')
        
        for plot in plots:
            collection = plot['collection']
            slug = plot['slug']
            
            # Load full plot data
            plot_dir = self.site_dir / 'collections' / collection / slug
            plot_data = self._load_full_plot_data(plot_dir, plot)
            
            html = template.render(
                site=self.config,
                plot=plot_data,
                page_title=plot_data.get('title', slug),
                base_path="../.."
            )
            
            plot_output_dir = output_path / collection / slug
            plot_output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(plot_output_dir / 'index.html', 'w') as f:
                f.write(html)
        
        if verbose:
            print(f"✅ Built {len(plots)} individual plot pages")
    
    def _load_full_plot_data(self, plot_dir: Path, base_plot: Dict[str, Any]) -> Dict[str, Any]:
        """Load full plot data including code content."""
        plot_data = base_plot.copy()
        
        # Load code file content
        if plot_data.get('code_file'):
            code_file = plot_dir / plot_data['code_file']
            if code_file.exists():
                with open(code_file, 'r') as f:
                    plot_data['code_content'] = f.read()
        
        # Load any additional files
        for file in plot_dir.iterdir():
            if file.is_file() and file.suffix in ['.py', '.ipynb', '.md']:
                with open(file, 'r') as f:
                    plot_data[f'{file.stem}_content'] = f.read()
        
        return plot_data