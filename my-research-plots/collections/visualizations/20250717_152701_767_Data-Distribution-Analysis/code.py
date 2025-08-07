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
