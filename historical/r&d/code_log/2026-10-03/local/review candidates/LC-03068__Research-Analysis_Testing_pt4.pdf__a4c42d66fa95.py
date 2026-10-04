import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
interweb_data = [(a, b, rank, leading_coeff/10, omega, reg, tamagawa, weak_bsd_holds,
math.log(abs(E.discriminant())), math.log(E.conductor())) for _, (a, b, rank, leading_coeff, omega, reg,
tamagawa, weak_bsd_holds, E, _) in results if omega is not None]
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ranks = [x[2] for x in interweb_data]
log_deltas = [x[8] for x in interweb_data]
log_conds = [x[9] for x in interweb_data]
sizes = [float(max(x[3] * 100, 1e-6)) for x in interweb_data]
colors = [x[7] for x in interweb_data]
scatter = ax.scatter(log_deltas, log_conds, ranks, s=sizes, c=colors, cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label='Weak BSD Holds')
for i in range(len(interweb_data)):
    for j in range(i + 1, len(interweb_data)):
        reg_diff = abs(interweb_data[i][5] - interweb_data[j][5])
        if reg_diff < 10000:
            weight = 1 / (1 + reg_diff / 100)
            ax.plot([log_deltas[i], log_deltas[j]], [log_conds[i], log_conds[j]], [ranks[i], ranks[j]], 'b-', alpha=0.5 *
weight, linewidth=0.7 * weight)
ax.set_xlabel('Log(Discriminant)')
ax.set_ylabel('Log(Conductor)')
ax.set_zlabel('Rank')
ax.set_title('Cosmic Interweb: Nodes and Weighted Filaments')
plt.savefig("interweb_final.png")


               ●    plt.close()
