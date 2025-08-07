#!/usr/bin/env python3
"""
Generate test plots for our research site.
"""

import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Add the parent directory to the path to import snapshotplot
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from snapshotplot import snapshot


@snapshot(
    site=".",  # Current directory (my-research-plots)
    collection="experiments",
    title="Linear Regression Analysis",
    description="Example of linear regression with noise",
    tags=["regression", "statistics", "machine-learning"],
    author="Data Science Team"
)
def create_linear_regression():
    """Create a linear regression plot."""
    np.random.seed(42)
    
    # Generate sample data
    x = np.linspace(0, 10, 100)
    y = 2 * x + 1 + np.random.normal(0, 2, 100)
    
    # Fit linear regression
    coeffs = np.polyfit(x, y, 1)
    line = np.polyval(coeffs, x)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.6, label='Data points')
    plt.plot(x, line, 'r-', linewidth=2, label=f'Linear fit: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Linear Regression Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()


@snapshot(
    site=".",
    collection="visualizations",
    title="Sine and Cosine Comparison",
    description="Comparing sine and cosine functions with different frequencies",
    tags=["trigonometry", "comparison", "functions"],
    author="Data Science Team"
)
def create_trig_comparison():
    """Create a trigonometric functions comparison."""
    x = np.linspace(0, 4*np.pi, 1000)
    
    plt.figure(figsize=(12, 6))
    plt.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
    plt.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
    plt.plot(x, np.sin(2*x), 'g--', linewidth=2, label='sin(2x)')
    plt.plot(x, np.cos(2*x), 'm--', linewidth=2, label='cos(2x)')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Trigonometric Functions Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()


@snapshot(
    site=".",
    collection="experiments",
    title="Random Walk Simulation",
    description="Monte Carlo simulation of a random walk process",
    tags=["simulation", "random-walk", "monte-carlo"],
    author="Data Science Team"
)
def create_random_walk():
    """Create a random walk simulation."""
    np.random.seed(123)
    
    # Generate multiple random walks
    n_steps = 1000
    n_walks = 5
    
    plt.figure(figsize=(12, 8))
    
    for i in range(n_walks):
        steps = np.random.choice([-1, 1], n_steps)
        walk = np.cumsum(steps)
        plt.plot(walk, alpha=0.7, label=f'Walk {i+1}')
    
    plt.xlabel('Step')
    plt.ylabel('Position')
    plt.title('Random Walk Simulation (5 walks)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()


@snapshot(
    site=".",
    collection="visualizations",
    title="Data Distribution Analysis",
    description="Histogram and density plot of normal distribution",
    tags=["statistics", "distribution", "histogram"],
    author="Data Science Team"
)
def create_distribution_analysis():
    """Create a distribution analysis plot."""
    np.random.seed(42)
    
    # Generate sample data
    data = np.random.normal(100, 15, 1000)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogram
    ax1.hist(data, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Density')
    ax1.set_title('Histogram of Data')
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    ax2.boxplot(data, vert=True)
    ax2.set_ylabel('Value')
    ax2.set_title('Box Plot of Data')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()


@snapshot(
    site=".",
    collection="experiments",
    title="Clustering Analysis",
    description="K-means clustering visualization on 2D data",
    tags=["clustering", "k-means", "unsupervised-learning"],
    author="Data Science Team"
)
def create_clustering_analysis():
    """Create a clustering analysis plot."""
    np.random.seed(42)
    
    # Generate sample data with clusters
    cluster1 = np.random.multivariate_normal([2, 2], [[1, 0], [0, 1]], 100)
    cluster2 = np.random.multivariate_normal([6, 6], [[1, 0], [0, 1]], 100)
    cluster3 = np.random.multivariate_normal([2, 6], [[1, 0], [0, 1]], 100)
    
    data = np.vstack([cluster1, cluster2, cluster3])
    
    plt.figure(figsize=(10, 8))
    plt.scatter(cluster1[:, 0], cluster1[:, 1], c='red', alpha=0.6, label='Cluster 1')
    plt.scatter(cluster2[:, 0], cluster2[:, 1], c='blue', alpha=0.6, label='Cluster 2')
    plt.scatter(cluster3[:, 0], cluster3[:, 1], c='green', alpha=0.6, label='Cluster 3')
    
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('K-means Clustering Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()


def main():
    """Generate all test plots."""
    print("🚀 Generating test plots for the research site...")
    
    plots = [
        ("Linear Regression", create_linear_regression),
        ("Trig Comparison", create_trig_comparison),
        ("Random Walk", create_random_walk),
        ("Distribution Analysis", create_distribution_analysis),
        ("Clustering Analysis", create_clustering_analysis)
    ]
    
    for name, func in plots:
        print(f"📊 Creating {name}...")
        func()
        plt.close('all')  # Close all figures to free memory
    
    print("✅ All plots generated successfully!")
    print("📁 Check the collections/ directory for the generated plots")


if __name__ == "__main__":
    main()