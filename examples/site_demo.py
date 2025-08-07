#!/usr/bin/env python3
"""
Demo script showing the new static site generator functionality.

This demonstrates how SnapshotPlot can be used to create a static site
with GitHub Pages integration.
"""

import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from snapshotplot import snapshot


# Example 1: Basic site integration
@snapshot(
    site="my-research-site",
    collection="experiments",
    title="Sine Wave Analysis",
    description="A simple sine wave plot demonstrating basic matplotlib functionality",
    tags=["trigonometry", "waves", "basic"],
    author="Research Team"
)
def create_sine_wave():
    """Create a simple sine wave plot."""
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
    plt.title("Sine Wave Function", fontsize=16)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("sin(x)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()


# Example 2: Advanced site integration with auto-build
@snapshot(
    site="my-research-site",
    collection="ml-experiments",
    title="Random Data Classification",
    description="Scatter plot showing classification of random 2D data points",
    tags=["machine-learning", "classification", "scatter"],
    author="ML Team",
    auto_build=True  # Automatically rebuild site after snapshot
)
def create_classification_plot():
    """Create a classification scatter plot."""
    np.random.seed(42)
    
    # Generate random data
    n_samples = 200
    X = np.random.randn(n_samples, 2)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    plt.figure(figsize=(10, 8))
    colors = ['red', 'blue']
    labels = ['Class 0', 'Class 1']
    
    for i in range(2):
        plt.scatter(X[y == i, 0], X[y == i, 1], 
                   c=colors[i], label=labels[i], alpha=0.6)
    
    plt.title("Random Data Classification", fontsize=16)
    plt.xlabel("Feature 1", fontsize=12)
    plt.ylabel("Feature 2", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()


# Example 3: Context manager usage with git integration
def create_time_series_analysis():
    """Create a time series analysis plot."""
    with snapshot(
        site="my-research-site",
        collection="time-series",
        title="Stock Price Simulation",
        description="Monte Carlo simulation of stock price movements",
        tags=["finance", "monte-carlo", "time-series"],
        author="Finance Team",
        auto_commit=True  # Automatically commit to git
    ):
        # Simulate stock price
        np.random.seed(123)
        days = 252  # Trading days in a year
        initial_price = 100
        volatility = 0.2
        drift = 0.05
        
        dt = 1/days
        returns = np.random.normal(drift*dt, volatility*np.sqrt(dt), days)
        prices = initial_price * np.exp(np.cumsum(returns))
        
        plt.figure(figsize=(12, 6))
        plt.plot(range(days), prices, 'b-', linewidth=2)
        plt.title("Simulated Stock Price Movement", fontsize=16)
        plt.xlabel("Trading Day", fontsize=12)
        plt.ylabel("Price ($)", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()


# Example 4: Full automation (commit + build + deploy)
@snapshot(
    site="my-research-site",
    collection="prototypes",
    title="3D Surface Plot",
    description="3D visualization of a mathematical surface function",
    tags=["3d", "visualization", "surface"],
    author="Visualization Team",
    auto_commit=True,
    auto_build=True,
    auto_deploy=True  # Full automation
)
def create_3d_surface():
    """Create a 3D surface plot."""
    from mpl_toolkits.mplot3d import Axes3D
    
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax.set_title("3D Surface: sin(sqrt(x² + y²))", fontsize=16)
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.set_zlabel("Z", fontsize=12)
    
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.tight_layout()


def main():
    """Run the site generation demo."""
    print("🚀 SnapshotPlot Static Site Generator Demo")
    print("=" * 50)
    
    print("\n📊 Creating plots with site integration...")
    
    # Run the examples
    print("1. Creating sine wave plot...")
    create_sine_wave()
    plt.close()
    
    print("2. Creating classification plot...")
    create_classification_plot()
    plt.close()
    
    print("3. Creating time series analysis...")
    create_time_series_analysis()
    plt.close()
    
    print("4. Creating 3D surface plot...")
    create_3d_surface()
    plt.close()
    
    print("\n✅ Demo completed!")
    print("\nTo use the site generator:")
    print("1. Initialize a new site:")
    print("   snapshotplot init my-research-site")
    print("2. Create collections:")
    print("   snapshotplot collection create experiments")
    print("3. Run your plotting code with site integration")
    print("4. Build the site:")
    print("   snapshotplot build")
    print("5. Serve locally:")
    print("   snapshotplot serve")
    print("6. Deploy to GitHub Pages:")
    print("   snapshotplot deploy --push")


if __name__ == "__main__":
    main()