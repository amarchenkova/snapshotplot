"""
Template files for different site themes.
"""

def get_template(theme: str = 'scientific') -> dict:
    """Get template files for a specific theme."""
    
    if theme == 'scientific':
        return get_scientific_templates()
    elif theme == 'minimal':
        return get_minimal_templates()
    else:
        return get_scientific_templates()


def get_scientific_templates() -> dict:
    """Scientific theme templates."""
    
    return {
        '_layouts/default.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }} - {{ site.title }}</title>
    <link rel="stylesheet" href="assets/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css">
</head>
<body>
    {% include 'header.html' %}
    
    <main class="container">
        {% if is_index %}
            <section class="hero">
                <h1>{{ site.title }}</h1>
                <p>{{ site.description }}</p>
            </section>
            
            <section class="recent-plots">
                <h2>Recent Plots</h2>
                <div class="plot-grid">
                    {% for plot in plots %}
                        {% include 'plot-card.html' %}
                    {% endfor %}
                </div>
            </section>
            
            <section class="collections">
                <h2>Collections</h2>
                <div class="collection-grid">
                    {% for collection_name, collection_plots in collections.items() %}
                        <div class="collection-card">
                            <h3><a href="{{ collection_name }}/">{{ collection_name|title }}</a></h3>
                            <p>{{ collection_plots|length }} plots</p>
                        </div>
                    {% endfor %}
                </div>
            </section>
        {% else %}
            {{ content }}
        {% endif %}
    </main>
    
    {% include 'footer.html' %}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>''',

        '_layouts/gallery.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }} - {{ site.title }}</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    {% include 'header.html' %}
    
    <main class="container">
        <div class="collection-header">
            <h1>{{ collection.title }}</h1>
            <p>{{ collection.description }}</p>
        </div>
        
        <div class="plot-grid">
            {% for plot in plots %}
                {% include 'plot-card.html' %}
            {% endfor %}
        </div>
    </main>
    
    {% include 'footer.html' %}
</body>
</html>''',

        '_layouts/plot.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ plot.title }} - {{ site.title }}</title>
    <link rel="stylesheet" href="../../assets/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css">
</head>
<body>
    {% include 'header.html' %}
    
    <main class="container">
        <article class="plot-detail">
            <header class="plot-header">
                <h1>{{ plot.title }}</h1>
                <div class="plot-meta">
                    <span class="date">{{ plot.date|dateformat }}</span>
                    {% if plot.author %}
                        <span class="author">by {{ plot.author }}</span>
                    {% endif %}
                    <span class="collection">in <a href="../">{{ plot.collection }}</a></span>
                </div>
                {% if plot.tags %}
                    <div class="plot-tags">
                        {% for tag in plot.tags %}
                            <span class="tag">{{ tag }}</span>
                        {% endfor %}
                    </div>
                {% endif %}
            </header>
            
            {% if plot.description %}
                <div class="plot-description">
                    <p>{{ plot.description }}</p>
                </div>
            {% endif %}
            
            {% if plot.plot_image %}
                <div class="plot-image-container">
                    <img src="{{ plot.plot_image }}" alt="{{ plot.title }}" class="plot-image-full">
                </div>
            {% endif %}
            
            {% if plot.code_content %}
                <div class="code-section">
                    <h3>Source Code</h3>
                    <pre><code class="language-python">{{ plot.code_content }}</code></pre>
                </div>
            {% endif %}
            
            {% if plot.content %}
                <div class="plot-content">
                    {{ plot.content|safe }}
                </div>
            {% endif %}
            
            <div class="plot-actions">
                <a href="../" class="btn-secondary">← Back to {{ plot.collection }}</a>
                {% if plot.code_file %}
                    <a href="{{ plot.code_file }}" class="btn-primary" download>Download Code</a>
                {% endif %}
            </div>
        </article>
    </main>
    
    {% include 'footer.html' %}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>''',

        '_includes/header.html': '''<header>
    <div class="container">
        <div class="header-content">
            <a href="{{ base_path or '/' }}" class="logo">{{ site.title }}</a>
            <nav>
                <ul>
                    <li><a href="{{ base_path or '/' }}">Home</a></li>
                    {% for collection_name, collection_config in site.collections.items() %}
                        <li><a href="{{ base_path or '' }}/{{ collection_name }}/">{{ collection_config.title }}</a></li>
                    {% endfor %}
                </ul>
            </nav>
        </div>
    </div>
</header>''',

        '_includes/footer.html': '''<footer>
    <div class="container">
        <p>&copy; {{ site.author }} - Generated with SnapshotPlot</p>
        {% if site.github_repo %}
            <p><a href="https://github.com/{{ site.github_repo }}">View on GitHub</a></p>
        {% endif %}
    </div>
</footer>''',

        '_includes/plot-card.html': '''<div class="plot-card">
    <a href="{{ plot.collection }}/{{ plot.slug }}/">
        {% if plot.plot_image %}
            <img src="{{ plot.collection }}/{{ plot.slug }}/{{ plot.plot_image }}" alt="{{ plot.title }}" class="plot-image">
        {% endif %}
        <h3 class="plot-title">{{ plot.title }}</h3>
    </a>
    <div class="plot-meta">
        <span class="date">{{ plot.date|dateformat('%b %d, %Y') }}</span>
        {% if plot.author %}
            <span class="author">by {{ plot.author }}</span>
        {% endif %}
    </div>
    {% if plot.tags %}
        <div class="plot-tags">
            {% for tag in plot.tags %}
                <span class="tag">{{ tag }}</span>
            {% endfor %}
        </div>
    {% endif %}
</div>''',

        'assets/style.css': '''/* Enhanced Scientific Theme - Dark Mode */
:root {
    --primary-color: #60a5fa;
    --secondary-color: #94a3b8;
    --accent-color: #22d3ee;
    --background-color: #0f172a;
    --surface-color: #1e293b;
    --text-color: #f1f5f9;
    --text-light: #cbd5e1;
    --border-color: #334155;
    --success-color: #34d399;
    --warning-color: #fbbf24;
    --error-color: #f87171;
    --code-bg: #020617;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
header {
    background: var(--surface-color);
    border-bottom: 1px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
    text-decoration: none;
    display: flex;
    align-items: center;
}

.logo::before {
    content: "📊";
    margin-right: 0.5rem;
}

nav ul {
    display: flex;
    list-style: none;
    gap: 0.5rem;
}

nav a {
    color: var(--text-light);
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    transition: all 0.2s ease;
    font-weight: 500;
}

nav a:hover {
    background-color: var(--primary-color);
    color: white;
}

/* Hero Section */
.hero {
    text-align: center;
    padding: 4rem 0;
    background: linear-gradient(135deg, var(--surface-color), var(--background-color));
    color: var(--text-color);
    margin: 0 -20px 3rem -20px;
    border-bottom: 1px solid var(--border-color);
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: 700;
}

.hero p {
    font-size: 1.25rem;
    opacity: 0.8;
    color: var(--text-light);
}

/* Sections */
section {
    margin-bottom: 3rem;
}

section h2 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    color: var(--text-color);
    font-weight: 600;
}

/* Plot Grid */
.plot-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.plot-card {
    background: var(--surface-color);
    border-radius: 0.75rem;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    border: 1px solid var(--border-color);
}

.plot-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.plot-card a {
    text-decoration: none;
    color: inherit;
}

.plot-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    background: var(--background-color);
}

.plot-card h3 {
    padding: 1rem 1.5rem 0.5rem;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-color);
}

.plot-meta {
    padding: 0 1.5rem;
    color: var(--text-light);
    font-size: 0.875rem;
    margin-bottom: 1rem;
}

.plot-meta .date::before {
    content: "📅 ";
}

.plot-meta .author::before {
    content: "👤 ";
    margin-left: 1rem;
}

.plot-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0 1.5rem 1.5rem;
}

.tag {
    background: var(--primary-color);
    color: var(--background-color);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.2s ease;
}

.tag:hover {
    transform: scale(1.05);
    background: var(--accent-color);
}

/* Collection Grid */
.collection-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}

.collection-card {
    background: var(--surface-color);
    padding: 2rem;
    border-radius: 0.75rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.collection-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.collection-card h3 {
    margin-bottom: 0.5rem;
    font-size: 1.5rem;
}

.collection-card a {
    color: var(--primary-color);
    text-decoration: none;
}

.collection-card a:hover {
    text-decoration: underline;
}

/* Plot Detail Page */
.plot-detail {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 0;
}

.plot-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--border-color);
}

.plot-header h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--text-color);
}

.plot-header .plot-meta {
    font-size: 1rem;
    margin-bottom: 1rem;
}

.plot-header .plot-meta .date {
    font-weight: 600;
}

.plot-header .plot-meta a {
    color: var(--primary-color);
    text-decoration: none;
}

.plot-header .plot-meta a:hover {
    text-decoration: underline;
}

.plot-description {
    margin-bottom: 2rem;
    font-size: 1.125rem;
    color: var(--text-light);
}

.plot-image-container {
    margin: 2rem 0;
    text-align: center;
    background: var(--surface-color);
    border-radius: 0.75rem;
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.plot-image-full {
    max-width: 100%;
    height: auto;
    border-radius: 0.5rem;
}

.code-section {
    margin: 2rem 0;
}

.code-section h3 {
    margin-bottom: 1rem;
    color: var(--text-color);
    font-size: 1.5rem;
}

.code-section pre {
    background: var(--code-bg);
    color: var(--text-color);
    padding: 1.5rem;
    border-radius: 0.75rem;
    overflow-x: auto;
    font-size: 0.875rem;
    line-height: 1.5;
    border: 1px solid var(--border-color);
}

.plot-actions {
    display: flex;
    gap: 1rem;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
}

.btn-primary, .btn-secondary {
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
    display: inline-block;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: var(--accent-color);
}

.btn-secondary {
    background: transparent;
    color: var(--text-light);
    border: 1px solid var(--border-color);
}

.btn-secondary:hover {
    background: var(--background-color);
    color: var(--text-color);
}

/* Footer */
footer {
    margin-top: 4rem;
    padding: 2rem 0;
    border-top: 1px solid var(--border-color);
    background: var(--surface-color);
    text-align: center;
    color: var(--text-light);
}

footer a {
    color: var(--primary-color);
    text-decoration: none;
}

footer a:hover {
    text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        gap: 1rem;
    }
    
    nav ul {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .plot-grid {
        grid-template-columns: 1fr;
    }
    
    .plot-actions {
        flex-direction: column;
    }
}'''
    }


def get_minimal_templates() -> dict:
    """Minimal theme templates."""
    return {
        # Similar structure but with minimal styling
        # This would be a simpler version of the scientific theme
    }