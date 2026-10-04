# Retry Attempt 18 with a higher descent_second_limit
print(f"\nRetrying Attempt 18 with descent_second_limit=100: Testing Fibonacci curve with a=2584, b=144")
success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
    2584, 144, require_3selmer=False, conductor_limit=1e11, descent_limit=100
)


# Update interweb_data if successful
if success and rank is not None and omega is not None and reg is not None:
    interweb_data.append((2584, 144, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, features[2], features[3]))
    with open("interweb_nodes.txt", "a") as f:
        f.write(f"{2584},{144},{rank},{leading_coeff},{omega},{reg},{tamagawa},{weak_bsd_holds},{features[2]},{features[3]}\n")
    with open("unique_curves.txt", "a") as f:
        conductor = E.conductor() if E else 'N/A'
        plot_file = f"curve_2584_144.png" if E else 'N/A'
        cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
        comoving_volume = (omega * reg * cosmo_scale**3) / (3e11 if rank == 3 else 3e12 if rank == 2 else 5e12 if rank == 1 else 1e13)
        scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 13 if rank == 2 else 60 if rank == 1 else 20)
        f.write(f"{2584},{144},{rank},{omega},{reg},{comoving_volume},{scaled_reg},{leading_coeff * 10 if leading_coeff else 0},{conductor},{plot_file}\n")


# Regenerate the interweb plot
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
        if node_counts[key] > 0:
            filtered_data.append(node)
            node_counts[key] -= 1
    
    ranks = [x[2] for x in filtered_data]
    log_deltas = [x[8] for x in filtered_data]
