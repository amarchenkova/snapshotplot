# SnapshotPlot Static Site Generator

## Overview

SnapshotPlot now functions as a **static site generator for data science plots**, similar to Jekyll or Hugo, but specifically designed for research and data visualization workflows. It integrates with GitHub for version control and GitHub Pages for hosting.

## Key Features

### 🏗️ Static Site Generation
- **Collections-based organization** - Group plots by project/experiment
- **Front matter** - YAML metadata in plot files
- **Responsive themes** - Professional, mobile-friendly layouts
- **Automatic galleries** - Index pages and collection views

### 📊 GitHub Integration
- **GitHub Pages deployment** - Automatic static site hosting
- **Git version control** - Track all plots and code changes
- **GitHub Actions** - Automated builds and deployments
- **Issue/PR integration** - Discuss plots like code

### 🎯 Research-Focused
- **Reproducible plots** - Code, data, and metadata together
- **Searchable archives** - Find plots by tag, author, date
- **Team collaboration** - Share plots via GitHub permissions
- **Audit trails** - Git history for compliance

## Architecture

### Directory Structure
```
my-research-plots/
├── _config.yml                 # Site configuration
├── _layouts/                   # Template files
│   ├── default.html           # Base layout
│   ├── gallery.html           # Collection gallery
│   └── plot.html              # Individual plot page
├── _includes/                  # Reusable components
├── collections/                # Plot collections
│   ├── experiments/
│   │   ├── _index.md          # Collection metadata
│   │   └── 20250717_analysis/
│   │       ├── plot.png       # Generated plot
│   │       ├── code.py        # Source code
│   │       └── index.md       # Plot metadata
│   └── prototypes/
├── docs/                       # Generated site (GitHub Pages)
└── .github/workflows/         # GitHub Actions
```

### Enhanced API

**Basic usage (unchanged):**
```python
@snapshot()
def my_plot():
    plt.plot([1, 2, 3])
    plt.show()
```

**Static site generation:**
```python
@snapshot(
    site="my-research-plots",           # Site directory
    collection="experiments",           # Collection name
    title="Feature Analysis",           # Plot title
    tags=["regression", "features"],    # Tags for filtering
    description="Analysis of user behavior features",
    author="Research Team",
    auto_commit=True,                   # Git commit
    auto_build=True,                    # Rebuild site
    auto_deploy=True                    # Deploy to GitHub Pages
)
def feature_analysis():
    # Your plotting code
    pass
```

## CLI Commands

### Site Management
```bash
# Initialize new plot site
snapshotplot init my-research --template=scientific

# Create new collection
snapshotplot collection create experiments --title="ML Experiments"

# Generate static site
snapshotplot build

# Local development server
snapshotplot serve --port 8000

# Deploy to GitHub Pages
snapshotplot deploy --push
```

### Plot Management
```bash
# List all plots
snapshotplot list --collection experiments

# Search by tag/author is planned; for now, filter via the website or tooling
```

## Workflow Examples

### 1. Individual Researcher
```python
# Create plots with automatic site integration
@snapshot(
    collection="daily-analysis",
    tags=["exploration"],
    auto_build=True
)
def daily_analysis():
    # Your analysis code
    pass
```

### 2. Research Team
```python
# Team collaboration with git integration
@snapshot(
    site="team-research",
    collection="ml-experiments",
    author="Alice Smith",
    auto_commit=True,
    auto_build=True
)
def experiment_results():
    # Experiment code
    pass
```

### 3. Production Pipeline
```python
# Full automation for CI/CD
@snapshot(
    site="production-reports",
    collection="daily-reports",
    auto_commit=True,
    auto_build=True,
    auto_deploy=True
)
def generate_report():
    # Report generation
    pass
```

## GitHub Integration

### Automatic Setup
The CLI creates a complete GitHub-ready structure:

```yaml
# .github/workflows/build-plots.yml
name: Build and Deploy Plot Site
on:
  push:
    branches: [ main ]
    paths: ['collections/**']
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
      run: pip install snapshotplot
    - name: Build site
      run: snapshotplot build
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
```

### GitHub Pages Configuration
1. **Repository Settings** → **Pages** → **Source**: GitHub Actions
2. **Automatic deployment** on every push to main
3. **Custom domain** support
4. **HTTPS** by default

## Themes

### Scientific Theme (Default)
- Clean, professional design
- Syntax-highlighted code
- Responsive grid layouts
- Dark mode support
- Print-friendly styles

### Minimal Theme
Note: Not yet implemented; the default theme is 'scientific'.
- Simple, distraction-free design
- Fast loading
- Mobile-optimized
- High contrast

### Custom Themes
```python
# Create custom theme
snapshotplot init my-site --template=custom

# Override templates
# Edit _layouts/default.html
# Edit assets/style.css
```

## Benefits Over Traditional Approaches

### vs. Manual Documentation
- **Automatic** - No manual HTML writing
- **Consistent** - Standardized layouts
- **Searchable** - Built-in search and filtering
- **Version controlled** - Git tracks everything

### vs. Jupyter Notebooks
- **Focused** - Plot-centric, not code-centric
- **Shareable** - Easy to send links
- **Archival** - Long-term storage and retrieval
- **Collaborative** - Team access via GitHub

### vs. Cloud Solutions
- **Open source** - No vendor lock-in
- **Self-hosted** - Full control
- **Integrated** - Works with existing Git workflows
- **Cost-effective** - GitHub Pages is free

## Advanced Features

### Metadata Management
```yaml
# Generated automatically in index.md
---
title: "Feature Analysis"
date: 2025-07-17T10:30:00Z
author: "Research Team"
tags: ["regression", "features"]
description: "Analysis of user behavior features"
plot_image: "plot.png"
code_file: "code.py"
function_name: "feature_analysis"
---
```

### Search and Filtering
- **By collection** - All experiments, prototypes, etc.
- **By tag** - machine-learning, visualization, etc.
- **By author** - Team member contributions
- **By date** - Recent or historical analysis

### Export Options (planned)
- **PDF** - For presentations and reports
- **Markdown** - For documentation
- **JSON** - For programmatic access
- **Static HTML** - For offline viewing

## Getting Started

### Quick Start
```bash
# 1. Initialize site
snapshotplot init my-research

# 2. Create collection
cd my-research
snapshotplot collection create experiments

# 3. Create plots with integration
python -c "
from snapshotplot import snapshot
import matplotlib.pyplot as plt
import numpy as np

@snapshot(
    collection='experiments',
    title='Quick Test',
    tags=['test']
)
def test_plot():
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.show()

test_plot()
"

# 4. Build and serve
snapshotplot build
snapshotplot serve
```

### GitHub Setup
```bash
# 1. Create GitHub repository
gh repo create my-research-plots --public

# 2. Initialize site with GitHub integration
snapshotplot init my-research-plots --github-repo=username/my-research-plots

# 3. Push to GitHub
cd my-research-plots
git add .
git commit -m "Initial site setup"
git push -u origin main

# 4. Enable GitHub Pages
# Go to Settings → Pages → Source: GitHub Actions
```

## Migration Guide

### From Existing SnapshotPlot
Existing code works unchanged:
```python
# This still works exactly the same
@snapshot()
def my_plot():
    plt.plot([1, 2, 3])
    plt.show()
```

Add site integration when ready:
```python
# Enhanced version
@snapshot(
    collection="experiments",  # Add this
    title="My Analysis",       # Add this
    tags=["analysis"]          # Add this
)
def my_plot():
    plt.plot([1, 2, 3])
    plt.show()
```

### From Manual HTML
1. **Initialize site** - `snapshotplot init`
2. **Create collections** - Organize existing plots
3. **Add metadata** - Convert to front matter format
4. **Build site** - `snapshotplot build`

## Best Practices

### Project Organization
```
research-project/
├── data/                    # Raw data
├── notebooks/              # Jupyter notebooks
├── scripts/                # Analysis scripts
├── plots/                  # SnapshotPlot site
│   ├── collections/
│   │   ├── exploration/
│   │   ├── experiments/
│   │   └── results/
│   └── docs/              # Generated site
└── README.md
```

### Naming Conventions
- **Collections**: `experiments`, `prototypes`, `results`
- **Tags**: `machine-learning`, `visualization`, `statistical-analysis`
- **Titles**: Descriptive, specific titles

### Team Workflows
1. **Feature branches** for experiments
2. **Pull requests** for review
3. **Issues** for tracking analysis tasks
4. **Tags** for releases/milestones

## Performance

Note: The following items are planned improvements; current builds are full rebuilds without caching or incremental processing.

### Build Speed
- **Incremental builds** - Only changed plots
- **Parallel processing** - Multiple plots simultaneously
- **Caching** - Template and asset caching

### Site Performance
- **Static files** - No server-side processing
- **CDN-friendly** - Works with GitHub Pages CDN
- **Optimized images** - Automatic compression
- **Lazy loading** - Progressive image loading

## Conclusion

SnapshotPlot's static site generator transforms plot documentation from a manual, error-prone process into an automated, version-controlled workflow. By leveraging GitHub's ecosystem, it provides enterprise-grade features while remaining simple enough for individual researchers.

The Jekyll/Hugo-inspired architecture makes it familiar to developers while the research-focused features address the specific needs of data science teams. The result is a comprehensive solution for reproducible, shareable, and discoverable data visualization.

**Next steps:**
1. Try the quick start example
2. Set up GitHub Pages integration
3. Explore themes and customization
4. Integrate with your existing workflow