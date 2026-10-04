# 6. Topological Analysis
print("Computing persistence diagrams...")
arith_pd = compute_persistence(arithmetic_cloud, max_dim=2)
cosmic_pd = compute_persistence(embedded, max_dim=2)
print(" Persistence diagrams computed.")

# 7. Integration Note
print("\nReady for integration with PaperFiguresPipeline and JointMCMCPipeline.")