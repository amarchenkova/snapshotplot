# SnapShotPlot 📸📊

Capture Python code, Matplotlib plots, and HTML documentation in one step with automatic timestamping and organization.

Ever run into this?

"Cool plot... where's the code that made it?"
"You made a mistake here, this other plot a few runs back was the correct one."
"Uhh... I think I overwrote it... maybe version 12_final_final_really_final.py?"


Yeah. Same.

snapshotplot was born out of one too many late-night research plot reviews where the code was somewhere, but no one could say where. I got tired of asking "how did you generate this?" and getting blank stares.

This package automatically takes a snapshot of your code and the plot every time you run it—HTML, code, and image saved, timestamped, and organized like a sane person lives here.

You get reproducibility without thinking about it. Your future self (and your collaborators) will thank you.

Just wrap your code with the snapshot context manager and keep shipping.

Because science shouldn't involve detective work.

![SnapshotPlot HTML Output](assets/screenshot.png)

## Features

- **🔄 Decorator & Context Manager Support**: Use as `@snapshot()` or `with snapshot():`
- **⏰ Unified Timestamping**: Single UTC timestamp per snapshot run
- **📁 Auto-Organization**: Creates timestamped folders with all outputs
- **🎨 HTML Documentation**: Beautiful, syntax-highlighted HTML with embedded plots
- **🔧 Zero Configuration**: Works out of the box with sensible defaults
- **🚀 Non-Intrusive**: Runs silently in the background

## Quick Start

### Installation

```bash
pip install snapshotplot
```

### Basic Usage

#### As a Decorator

```python
from snapshotplot import snapshot
import matplotlib.pyplot as plt
import numpy as np

@snapshot()
def create_sine_wave():
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.title("Sine Wave")
    plt.grid(True)
    plt.show()
```

#### As a Context Manager

```python
from snapshotplot import snapshot
import matplotlib.pyplot as plt
import numpy as np

with snapshot():
    x = np.linspace(0, 10, 100)
    y = x**2
    plt.plot(x, y)
    plt.title("Quadratic Function")
    plt.xlabel("x")
    plt.ylabel("y = x²")
    plt.show()
```

## Output Structure

Each snapshot creates a folder structure like this:

```
snapshot_<filename>/
├── 20241201_143022_123_code.py       # Raw source code
├── 20241201_143022_123_plot.png      # Saved plot image
└── 20241201_143022_123_snapshot.html # HTML documentation
```

The HTML file contains:
- **Metadata**: Filename, function name, timestamp
- **Syntax-highlighted code**: Your Python code with proper formatting
- **Embedded plot**: The matplotlib figure directly in the HTML
- **Clean styling**: Professional, readable layout

## HTML Example

Here's what the generated HTML documentation looks like:

![SnapshotPlot HTML Output](assets/screenshot.png)

The output includes:
- **Dark mode interface** for easy reading
- **Side-by-side layout** with code and plot
- **Syntax-highlighted Python code**
- **Embedded plot images**
- **Responsive design** for mobile and desktop

## Configuration Options

```python
@snapshot(
    output_dir="my_snapshots",      # Custom output directory
    code_format="html",            # Code format in HTML
    title="My Analysis",           # Custom title for HTML
    author="Data Scientist",       # Author metadata
    notes="Important findings"     # Additional notes
)
def my_analysis():
    # Your code here
    pass
```

## Advanced Usage

### Custom Output Directory

```python
@snapshot(output_dir="research_outputs")
def research_plot():
    # Your research code
    pass
```

### With Metadata

```python
@snapshot(
    title="Sales Analysis Q4",
    author="Analytics Team",
    notes="Key insights from quarterly data"
)
def sales_analysis():
    # Your analysis code
    pass
```

### Context Manager with Configuration

```python
with snapshot(output_dir="experiments", title="A/B Test Results"):
    # Your experimental code
    pass
```

## Jupyter Notebook Integration

SnapshotPlot provides seamless integration with Jupyter notebooks through IPython magic commands, enabling you to capture and document your analysis workflow with zero overhead.

### Quick Start

```python
# 1. Load the extension (once per notebook)
%load_ext snapshotplot

# 2. Use cell magic to capture analysis
%%snapshot -t "Customer Analysis" -a "Data Science Team"
import matplotlib.pyplot as plt
import pandas as pd

# Your analysis code
df = pd.read_csv('data.csv')
plt.figure(figsize=(10, 6))
plt.hist(df['revenue'], bins=30)
plt.title('Revenue Distribution')
plt.show()
```

### Magic Commands

#### Cell Magic (`%%snapshot`)

Capture an entire cell's code and output - the most common usage pattern:

```python
%%snapshot -t "Market Segmentation" -a "Analytics Team" --tags ml clustering
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# Perform clustering analysis
data = np.random.rand(100, 2)
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(data)

# Visualize results
plt.figure(figsize=(8, 6))
plt.scatter(data[:, 0], data[:, 1], c=clusters, cmap='viridis')
plt.title('Customer Segments')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.colorbar(label='Cluster')
plt.show()
```

#### Line Magic (`%snapshot`)

Capture the previous cell's output - useful for retroactive documentation:

```python
# First cell: Create your analysis
plt.figure(figsize=(10, 6))
plt.plot(time_series_data)
plt.title('Sales Trend Over Time')
plt.show()

# Second cell: Capture it with metadata
%snapshot -t "Q4 Sales Trend" -a "Sales Team" --tags quarterly sales --description "Shows strong growth in Q4"
```

#### Magic Command Arguments

All magic commands support comprehensive metadata and configuration options:

```python
# Basic metadata
%%snapshot -t "Analysis Title" -a "Author Name" -n "Additional notes"

# Categorization and organization  
%%snapshot --tags experiment ml analysis --description "Detailed description" --collection research

# Custom output location
%%snapshot -o "custom_snapshots" --dpi 300

# Site integration (for static site generation)
%%snapshot --site "../my-blog" --collection "data-science" --auto-build

# Full example with all options
%%snapshot -t "Final Model Results" \
           -a "ML Team" \
           -n "Production model evaluation" \
           --tags model evaluation production \
           --description "Performance metrics for the final customer churn model" \
           --collection "ml-models" \
           --site "../research-blog" \
           --auto-commit \
           --auto-build
```

### Context Manager

Use the notebook-aware context manager for programmatic control:

```python
from snapshotplot import notebook_snapshot

# Basic usage
with notebook_snapshot(title="Experiment Results"):
    run_experiment()
    plot_results()
    plt.show()

# With full configuration
with notebook_snapshot(
    title="A/B Test Analysis",
    author="Product Team", 
    tags=["ab-test", "conversion"],
    collection="experiments",
    site="../product-blog"
):
    analyze_ab_test()
    plot_conversion_rates()
    plt.show()
```

### Real-World Workflow

Here's how to integrate SnapshotPlot into a typical data science workflow:

```python
# === NOTEBOOK SETUP ===
%load_ext snapshotplot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === EXPLORATORY DATA ANALYSIS ===
# Regular cells for exploration (no snapshot needed)
df = pd.read_csv('customer_data.csv')
df.info()
df.describe()

# === KEY INSIGHTS (Capture with snapshot) ===
%%snapshot -t "Customer Demographics Overview" -a "Data Science Team" --tags demographics eda
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
df['age'].hist(bins=20)
plt.title('Age Distribution')

plt.subplot(1, 3, 2) 
df['income'].hist(bins=20)
plt.title('Income Distribution')

plt.subplot(1, 3, 3)
sns.countplot(data=df, x='segment')
plt.title('Customer Segments')

plt.tight_layout()
plt.show()

# === MODELING (More exploration) ===
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# === MODEL RESULTS (Capture with snapshot) ===
%%snapshot -t "Model Performance Evaluation" --tags modeling evaluation --collection research
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Evaluate model
y_pred = model.predict(X_test)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

print("Classification Report:")
print(classification_report(y_test, y_pred))

# === FINAL INSIGHTS (Capture for presentation) ===
%%snapshot -t "Business Impact Analysis" -a "Data Science Team" \
           --description "Revenue impact of customer segmentation model" \
           --tags business-impact revenue --collection presentations \
           --site "../executive-dashboard" --auto-build

# Calculate business impact
plot_revenue_impact_by_segment()
plt.show()
```

### Generated Output

Each snapshot creates three files with consistent naming:

```
Project/
├── my_analysis.ipynb
└── snapshot_my_analysis/
    ├── 20240718_143022_001_code.py      # Cell source code
    ├── 20240718_143022_001_plot.png     # Matplotlib figure
    ├── 20240718_143022_001_snapshot.html # HTML documentation
    ├── 20240718_143155_002_code.py      # Next snapshot
    ├── 20240718_143155_002_plot.png
    └── 20240718_143155_002_snapshot.html
```

### HTML Documentation Features

The generated HTML documentation includes:

- **Notebook Metadata**: Name, kernel info, execution timestamp
- **Syntax-Highlighted Code**: Beautiful Python code formatting
- **Embedded Plots**: High-resolution matplotlib figures
- **User Metadata**: Title, author, tags, and notes
- **Responsive Design**: Mobile and desktop friendly
- **Dark Mode Theme**: Easy on the eyes for long reading sessions
- **Professional Styling**: Ready for sharing with stakeholders

### Site Integration

For teams maintaining research blogs or documentation sites, SnapshotPlot can automatically integrate with static site generators:

```python
%%snapshot -t "Quarterly Results" \
           --site "../research-blog" \
           --collection "quarterly-reports" \
           --auto-commit \
           --auto-build \
           --auto-deploy

# This will:
# 1. Create the snapshot files
# 2. Copy them to your site's collection directory  
# 3. Generate site metadata
# 4. Commit changes to git
# 5. Build the static site
# 6. Deploy to your hosting platform
```

### Checking Notebook Environment

You can programmatically detect if code is running in a notebook:

```python
from snapshotplot import is_notebook

if is_notebook():
    print("Running in Jupyter - magic commands available!")
    %load_ext snapshotplot
else:
    print("Running in regular Python - using context managers")
    from snapshotplot import snapshot
```

### Best Practices

1. **Load Once**: Run `%load_ext snapshotplot` once at the beginning of your notebook
2. **Meaningful Titles**: Use descriptive titles that will make sense months later
3. **Tag Everything**: Use consistent tags to organize your analysis across notebooks
4. **Capture Key Steps**: Not every cell needs a snapshot - focus on important insights
5. **Team Consistency**: Establish naming conventions for titles, authors, and tags
6. **Regular Review**: Generated HTML files are perfect for team reviews and presentations

## Requirements

- Python 3.8+
- matplotlib >= 3.5.0
- jinja2 >= 3.0.0
- pygments >= 2.10.0

## Development

### Installation for Development

```bash
git clone https://github.com/snapshotplot/snapshotplot.git
cd snapshotplot
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black snapshotplot/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Roadmap

- [ ] Support for Plotly and Altair
- [ ] Markdown export option
- [ ] Multiple plot gallery
- [ ] CLI tool for batch processing
- [x] Jupyter notebook integration 
