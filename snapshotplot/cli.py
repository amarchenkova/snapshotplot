#!/usr/bin/env python3
"""
CLI interface for SnapshotPlot static site generator functionality.
"""

import click
import os
import shutil
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import subprocess
import sys

from .site_generator import SiteGenerator
from .templates import get_template


@click.group()
@click.version_option()
def cli():
    """SnapshotPlot - Static Site Generator for Data Science Plots"""
    pass


@cli.command()
@click.argument('name')
@click.option('--template', default='scientific', help='Site template to use')
@click.option('--github-repo', help='GitHub repository (user/repo)')
@click.option('--author', help='Default author name')
@click.option('--title', help='Site title')
def init(name: str, template: str, github_repo: Optional[str], author: Optional[str], title: Optional[str]):
    """Initialize a new plot site."""
    site_path = Path(name)
    
    if site_path.exists():
        click.echo(f"Directory {name} already exists!")
        return
    
    click.echo(f"Creating new plot site: {name}")
    
    # Create directory structure
    site_path.mkdir()
    (site_path / '_layouts').mkdir()
    (site_path / '_includes').mkdir()
    (site_path / '_data').mkdir()
    (site_path / 'assets').mkdir()
    (site_path / 'collections').mkdir()
    (site_path / 'docs').mkdir()
    (site_path / '.github' / 'workflows').mkdir(parents=True)
    
    # Create config file
    config = {
        'title': title or f'{name.replace("-", " ").title()} Plots',
        'description': f'Data science plots and analysis for {name}',
        'author': author or 'Research Team',
        'github_repo': github_repo,
        'template': template,
        'build_dir': 'docs',
        'collections': {},
        'defaults': {
            'layout': 'plot',
            'author': author or 'Research Team'
        }
    }
    
    with open(site_path / '_config.yml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    # Create templates
    _create_templates(site_path, template)
    
    # Create GitHub workflow
    _create_github_workflow(site_path)
    
    # Create initial assets
    _create_assets(site_path)
    
    click.echo(f"✅ Plot site '{name}' created successfully!")
    click.echo(f"📁 Directory: {site_path.absolute()}")
    click.echo(f"🚀 Next steps:")
    click.echo(f"   cd {name}")
    click.echo(f"   snapshotplot collection create experiments")
    click.echo(f"   snapshotplot serve")


@cli.group()
def collection():
    """Manage plot collections."""
    pass


@collection.command('create')
@click.argument('name')
@click.option('--title', help='Collection title')
@click.option('--description', help='Collection description')
@click.option('--tags', help='Default tags (comma-separated)')
def create_collection(name: str, title: Optional[str], description: Optional[str], tags: Optional[str]):
    """Create a new plot collection."""
    config_path = Path('_config.yml')
    if not config_path.exists():
        click.echo("❌ No _config.yml found. Run 'snapshotplot init' first.")
        return
    
    collection_path = Path('collections') / name
    collection_path.mkdir(parents=True, exist_ok=True)
    
    # Create collection metadata
    metadata = {
        'title': title or name.replace('-', ' ').title(),
        'description': description or f'Plot collection for {name}',
        'tags': tags.split(',') if tags else [],
        'created': datetime.now().isoformat(),
        'layout': 'gallery'
    }
    
    with open(collection_path / '_index.md', 'w') as f:
        f.write('---\n')
        yaml.dump(metadata, f, default_flow_style=False)
        f.write('---\n\n')
        f.write(f'# {metadata["title"]}\n\n')
        f.write(f'{metadata["description"]}\n')
    
    # Update site config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    config['collections'][name] = {
        'title': metadata['title'],
        'description': metadata['description'],
        'output': True
    }
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    click.echo(f"✅ Collection '{name}' created successfully!")
    click.echo(f"📁 Directory: {collection_path.absolute()}")


@cli.command()
@click.option('--port', default=8000, help='Port to serve on')
@click.option('--host', default='127.0.0.1', help='Host to serve on')
def serve(port: int, host: str):
    """Start local development server."""
    if not Path('_config.yml').exists():
        click.echo("❌ No _config.yml found. Run 'snapshotplot init' first.")
        return
    
    # Build site first
    generator = SiteGenerator('.')
    generator.build()
    
    # Start server
    import http.server
    import socketserver
    import threading
    import webbrowser
    
    os.chdir('docs')
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()
    
    with socketserver.TCPServer((host, port), Handler) as httpd:
        url = f"http://{host}:{port}"
        click.echo(f"🚀 Serving plot site at {url}")
        click.echo(f"📁 Serving from: {Path.cwd()}")
        click.echo(f"⏹️  Press Ctrl+C to stop")
        
        # Open browser
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            click.echo("\n👋 Server stopped")


@cli.command()
@click.option('--output', default='docs', help='Output directory')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def build(output: str, verbose: bool):
    """Build the static site."""
    if not Path('_config.yml').exists():
        click.echo("❌ No _config.yml found. Run 'snapshotplot init' first.")
        return
    
    click.echo("🔨 Building plot site...")
    
    generator = SiteGenerator('.')
    generator.build(output_dir=output, verbose=verbose)
    
    click.echo(f"✅ Site built successfully!")
    click.echo(f"📁 Output: {Path(output).absolute()}")


@cli.command()
@click.option('--message', '-m', help='Commit message')
@click.option('--push', is_flag=True, help='Push to remote after building')
def deploy(message: Optional[str], push: bool):
    """Deploy site to GitHub Pages."""
    if not Path('_config.yml').exists():
        click.echo("❌ No _config.yml found. Run 'snapshotplot init' first.")
        return
    
    # Build site
    generator = SiteGenerator('.')
    generator.build()
    
    # Git operations
    commit_msg = message or f"Update plots site - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    try:
        subprocess.run(['git', 'add', 'docs/'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        if push:
            subprocess.run(['git', 'push'], check=True)
            click.echo("🚀 Site deployed successfully!")
        else:
            click.echo("✅ Site committed. Run 'git push' to deploy.")
            
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Git operation failed: {e}")


@cli.command()
@click.option('--collection', help='Filter by collection')
@click.option('--tag', help='Filter by tag')
@click.option('--author', help='Filter by author')
def list(collection: Optional[str], tag: Optional[str], author: Optional[str]):
    """List all plots."""
    if not Path('_config.yml').exists():
        click.echo("❌ No _config.yml found. Run 'snapshotplot init' first.")
        return
    
    generator = SiteGenerator('.')
    plots = generator.get_all_plots()
    
    # Apply filters
    if collection:
        plots = [p for p in plots if p.get('collection') == collection]
    if tag:
        plots = [p for p in plots if tag in p.get('tags', [])]
    if author:
        plots = [p for p in plots if p.get('author') == author]
    
    if not plots:
        click.echo("No plots found.")
        return
    
    click.echo(f"Found {len(plots)} plots:")
    for plot in plots:
        click.echo(f"  📊 {plot['title']} ({plot['collection']}) - {plot['date']}")


def _create_templates(site_path: Path, template: str):
    """Create template files."""
    templates = get_template(template)
    
    for filename, content in templates.items():
        if filename.startswith('_layouts/'):
            filepath = site_path / filename
        elif filename.startswith('_includes/'):
            filepath = site_path / filename
        elif filename.startswith('assets/'):
            filepath = site_path / filename
        else:
            filepath = site_path / filename
            
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)


def _create_github_workflow(site_path: Path):
    """Create GitHub Actions workflow."""
    workflow = '''name: Build and Deploy Plot Site

on:
  push:
    branches: [ main ]
    paths: ['collections/**', '_config.yml', '_layouts/**', 'assets/**']

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install snapshotplot
    
    - name: Build site
      run: |
        snapshotplot build
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
'''
    
    with open(site_path / '.github' / 'workflows' / 'build-plots.yml', 'w') as f:
        f.write(workflow)


def _create_assets(site_path: Path):
    """Create basic CSS and assets."""
    # Use the dark mode theme from templates
    from .templates import get_template
    templates = get_template('scientific')
    css = templates['assets/style.css']
    
    with open(site_path / 'assets' / 'style.css', 'w') as f:
        f.write(css)


if __name__ == '__main__':
    cli()