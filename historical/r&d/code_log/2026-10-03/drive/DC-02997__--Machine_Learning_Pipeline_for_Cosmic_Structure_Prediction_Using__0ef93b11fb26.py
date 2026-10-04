import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Define symbolic entropy field ℳ(x)
def symbolic_entropy(discriminant, conductor, rank, regulator):
    p1 = np.log(np.abs(discriminant)) / np.log(np.max(np.abs(discriminant)))
    p2 = np.log(conductor) / np.log(np.max(conductor))
    p3 = rank / np.max(rank)
    p4 = np.log(1 + regulator) / np.log(np.max(1 + regulator))
    return -(p1 * np.log(p1) + p2 * np.log(p2) + p3 * np.log(p3) + p4 * np.log(p4))


# Generate synthetic data for elliptic curve invariants
discriminant = np.linspace(-1000, -10, 50)
conductor = np.linspace(10, 1000, 50)
rank = np.linspace(0, 3, 50)
regulator = np.linspace(1, 10, 50)


# Create a 3D grid
X, Y = np.meshgrid(discriminant, conductor)
Z = symbolic_entropy(X, Y, rank[1], regulator[1])  # Fix rank and regulator for simplicity


# Plot the 3D surface
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax.set_title('Symbolic Entropy Field ℳ(x)')
ax.set_xlabel('Discriminant (Δ)')
ax.set_ylabel('Conductor (N)')
ax.set_zlabel('Symbolic Entropy ℳ(x)')
plt.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
plt.show()
