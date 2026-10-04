            successful_curves += 1
    attempts += 1

# Skip re-analyzing the original curve since it was already successful
print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")
if X_data:
    print(f"Total curves analyzed: {len(X_data)}")
    success_rate = float(sum(y_data) / len(y_data))
    print(f"Success rate: {success_rate:.2%}")
if interweb_data:
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    node_counts = {}
    for node in interweb_data:
        key = (node[0], node[1], node[2])
        node_counts[key] = node_counts.get(key, 0) + 1
    filtered_data = []
    for node in interweb_data:
        key = (node[0], node[1], node[2])
        if node_counts[key] == 1:
            filtered_data.append(node)
            node_counts[key] -= 1

    ranks = [x[2] for x in filtered_data]
    log_deltas = [x[8] for x in filtered_data]
    log_conds = [x[9] for x in filtered_data]
    sizes = [float(max(x[3] * 100, 1e-6)) for x in filtered_data]
    colors = [x[7] for x in filtered_data]
    scatter = ax.scatter(log_deltas, log_conds, ranks, s=sizes, c=colors, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter, label='Weak BSD Holds')

    for i in range(len(filtered_data)):
        for j in range(i + 1, len(filtered_data)):
            reg_diff = abs(filtered_data[i][5] - filtered_data[j][5])