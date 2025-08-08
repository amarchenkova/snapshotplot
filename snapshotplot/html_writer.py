"""
HTML generation for snapshotplot.

This module handles creating beautiful HTML documentation with syntax highlighting,
embedded plots, and metadata.
"""

import os
from typing import Dict, Any, Optional
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from jinja2 import Environment, BaseLoader


# HTML template with dark mode and side-by-side layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        :root {
            --bg: #181a1b;
            --panel: #23272e;
            --text: #e8e6e3;
            --accent: #4f8cff;
            --border: #333a41;
            --code-bg: #23272e;
            --code-header: #23272e;
            --code-border: #333a41;
            --plot-shadow: 0 4px 24px rgba(0,0,0,0.7);
        }
        html, body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Fira Mono', 'Menlo', 'Consolas', 'Liberation Mono', monospace, sans-serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: var(--panel);
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            overflow: hidden;
            padding: 0 0 32px 0;
        }
        .header {
            background: linear-gradient(135deg, #23272e 0%, #4f8cff 100%);
            color: #fff;
            padding: 32px 24px 16px 24px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.2em;
            font-weight: 400;
            margin-bottom: 8px;
        }
        .metadata {
            display: flex;
            justify-content: center;
            gap: 24px;
            margin-top: 12px;
            flex-wrap: wrap;
        }
        .metadata-item {
            background: rgba(255,255,255,0.07);
            padding: 6px 18px;
            border-radius: 16px;
            font-size: 0.95em;
            color: #b3b9c5;
        }
        .content {
            display: flex;
            flex-direction: row;
            gap: 32px;
            padding: 40px 32px 0 32px;
        }
        .section {
            flex: 1 1 0;
            min-width: 0;
        }
        .section h2 {
            color: var(--accent);
            font-size: 1.3em;
            margin-bottom: 18px;
            font-weight: 500;
            border-bottom: 2px solid var(--border);
            padding-bottom: 6px;
        }
        .code-block {
            background: var(--code-bg);
            border: 1px solid var(--code-border);
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 24px;
        }
        .code-header {
            background: var(--code-header);
            padding: 10px 20px;
            font-weight: 600;
            color: #8ecfff;
            border-bottom: 1px solid var(--code-border);
        }
        .code-content {
            padding: 18px 12px 18px 18px;
            overflow-x: auto;
        }
        .plot-section {
            text-align: center;
            margin: 0 0 24px 0;
        }
        .plot-image {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: var(--plot-shadow);
            background: #222;
            border: 1px solid var(--border);
        }
        .notes {
            background: #23272e;
            border-left: 4px solid var(--accent);
            padding: 18px 20px;
            margin: 18px 0;
            border-radius: 0 8px 8px 0;
            color: #b3b9c5;
        }
        .notes h3 {
            color: #8ecfff;
            margin-bottom: 8px;
        }
        .footer {
            background: var(--panel);
            padding: 18px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid var(--border);
        }
        /* Pygments syntax highlighting (dark) */
        .highlight {
            background: var(--code-bg);
        }
        .highlight pre {
            background: transparent;
            padding: 0;
            margin: 0;
            border: none;
        }
        /* Responsive design */
        @media (max-width: 900px) {
            .content {
                flex-direction: column;
                gap: 0;
                padding: 24px 8px 0 8px;
            }
            .section {
                margin-bottom: 32px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <div class="metadata">
                <div class="metadata-item">
                    <strong>File:</strong> {{ filename }}
                </div>
                <div class="metadata-item">
                    <strong>Function:</strong> {{ function_name }}
                </div>
                <div class="metadata-item">
                    <strong>Date:</strong> {{ date }}
                </div>
                {% if author %}
                <div class="metadata-item">
                    <strong>Author:</strong> {{ author }}
                </div>
                {% endif %}
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>Source Code</h2>
                <div class="code-block">
                    <div class="code-header">
                        {{ filename }} ({{ function_name }})
                    </div>
                    <div class="code-content">
                        {{ highlighted_code | safe }}
                    </div>
                </div>
                {% if notes %}
                <div class="notes">
                    <h3>Notes</h3>
                    <p>{{ notes }}</p>
                </div>
                {% endif %}
            </div>
            
            <div class="section">
                <h2>Generated Plot</h2>
                <div class="plot-section">
                    {% if plot_filename %}
                    <img src="{{ plot_filename }}" alt="Generated plot" class="plot-image">
                    {% else %}
                    <div style="color:#888; font-style:italic;">No plot was generated for this snapshot.</div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by SnapshotPlot on {{ date }}</p>
        </div>
    </div>
</body>
</html>
"""


def highlight_code(code: str) -> str:
    """
    Apply syntax highlighting to Python code.
    
    Args:
        code: Python source code
        
    Returns:
        str: HTML with syntax highlighting
    """
    try:
        # Use a dark style for code highlighting
        formatter = HtmlFormatter(
            style='monokai',
            noclasses=True,
            nobackground=True
        )
        highlighted = highlight(code, PythonLexer(), formatter)
        return highlighted
    except Exception:
        return f'<pre><code>{code}</code></pre>'


def generate_html(
    code: str,
    plot_filename: str,
    metadata: Dict[str, Any],
    title: Optional[str] = None,
    author: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """
    Generate HTML documentation for a snapshot.
    
    Args:
        code: Source code to include
        plot_filename: Filename of the plot image
        metadata: Dictionary with function info, filename, date, etc.
        title: Custom title for the HTML
        author: Author name
        notes: Additional notes
        
    Returns:
        str: Generated HTML content
    """
    # Prepare template variables
    template_vars = {
        'title': title or f"Snapshot: {metadata.get('function_name', 'Unknown Function')}",
        'filename': metadata.get('filename', 'unknown_file.py'),
        'function_name': metadata.get('function_name', 'unknown_function'),
        'date': metadata.get('date', 'Unknown Date'),
        'author': author,
        'notes': notes,
        'plot_filename': plot_filename,
        'highlighted_code': highlight_code(code)
    }
    
    # Render template with autoescape for safety
    env = Environment(loader=BaseLoader(), autoescape=True)
    template = env.from_string(HTML_TEMPLATE)
    return template.render(**template_vars)


def save_html(html_content: str, filepath: str) -> None:
    """
    Save HTML content to a file.
    
    Args:
        html_content: HTML content to save
        filepath: Path where to save the HTML file
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except Exception as e:
        raise IOError(f"Failed to save HTML file to {filepath}: {e}")


def create_html_snapshot(
    code: str,
    plot_path: str,
    html_path: str,
    metadata: Dict[str, Any],
    title: Optional[str] = None,
    author: Optional[str] = None,
    notes: Optional[str] = None
) -> None:
    """
    Create a complete HTML snapshot with all components.
    
    Args:
        code: Source code
        plot_path: Path to the plot image
        html_path: Path where to save the HTML file
        metadata: Metadata dictionary
        title: Custom title
        author: Author name
        notes: Additional notes
    """
    # Get just the filename for the plot image (for relative path in HTML)
    plot_filename = os.path.basename(plot_path)
    
    # Generate HTML content
    html_content = generate_html(
        code=code,
        plot_filename=plot_filename,
        metadata=metadata,
        title=title,
        author=author,
        notes=notes
    )
    
    # Save HTML file
    save_html(html_content, html_path) 