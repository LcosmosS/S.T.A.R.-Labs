import numpy as np
import matplotlib.pyplot as plt
import gudhi as gd


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


# Create a 2D grid
X, Y = np.meshgrid(discriminant, conductor)
Z = symbolic_entropy(X, Y, rank[1], regulator[1])  # Fix rank and regulator for simplicity


# Compute persistence diagram
rips_complex = gd.RipsComplex(points=np.c_[X.flatten(), Y.flatten()])
simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)
diag = simplex_tree.persistence()


# Plot persistence diagram
gd.plot_persistence_diagram(diag)
plt.title("Persistence Diagram of Symbolic Entropy Field ℳ(x)")
plt.show()
