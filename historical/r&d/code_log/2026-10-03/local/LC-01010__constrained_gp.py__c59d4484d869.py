"""
constrained_gp.py
-----------------
Implements a constrained Genetic Programming (GP) engine for the
S.T.A.R. Model's symbolic regression layer.

Constraints enforced:
- restricted primitive set
- max tree depth
- Lipschitz penalty
- isogeny-invariance
- null-scramble rejection
- law-discovery manifold admissibility
"""

import numpy as np
import random
from .law_discovery_manifold import LawDiscoveryManifold


class GPNode:
    """
    Node in a GP expression tree.
    """

    def __init__(self, op, children=None, value=None):
        self.op = op
        self.children = children or []
        self.value = value

    def evaluate(self, x):
        """
        Evaluate the GP tree on input x.
        """
        if self.op == "const":
            return self.value
        if self.op == "var":
            return x[self.value]

        vals = [child.evaluate(x) for child in self.children]

        if self.op == "add":
            return vals[0] + vals[1]
        if self.op == "sub":
            return vals[0] - vals[1]
        if self.op == "mul":
            return vals[0] * vals[1]
        if self.op == "div":
            return vals[0] / (vals[1] + 1e-12)
        if self.op == "log":
            return np.log(abs(vals[0]) + 1e-12)
        if self.op == "exp":
            return np.exp(vals[0])
        if self.op == "arctan":
            return np.arctan(vals[0])

        raise ValueError("Unknown operator")

    def depth(self):
        """
        Compute tree depth.
        """
        if not self.children:
            return 1
        return 1 + max(child.depth() for child in self.children)


class ConstrainedGP:
    """
    Constrained GP engine for symbolic law discovery.
    """

    def __init__(self, max_depth=6, population=50, mutation_rate=0.1):
        self.manifold = LawDiscoveryManifold(max_depth=max_depth)
        self.max_depth = max_depth
        self.population = population
        self.mutation_rate = mutation_rate

    def random_tree(self, depth=0):
        """
        Generate a random GP tree.
        """
        if depth >= self.max_depth or random.random() < 0.2:
            if random.random() < 0.5:
                return GPNode("const", value=random.uniform(-1, 1))
            return GPNode("var", value=random.randint(0, 2))

        op = random.choice(self.manifold.primitives)
        if op in ["log", "exp", "arctan"]:
            return GPNode(op, children=[self.random_tree(depth + 1)])
        return GPNode(op, children=[self.random_tree(depth + 1),
                                    self.random_tree(depth + 1)])

    def mutate(self, tree):
        """
        Mutate a GP tree.
        """
        if random.random() < self.mutation_rate:
            return self.random_tree()
        if tree.children:
            tree.children = [self.mutate(c) for c in tree.children]
        return tree

    def crossover(self, t1, t2):
        """
        Swap subtrees between two trees.
        """
        if random.random() < 0.5:
            return t2
        if t1.children and t2.children:
            idx = random.randint(0, len(t1.children) - 1)
            t1.children[idx] = self.crossover(t1.children[idx],
                                              random.choice(t2.children))
        return t1

    def evolve(self, data, isogeny_pairs, scrambled, generations=20):
        """
        Evolve GP trees under manifold constraints.
        """
        population = [self.random_tree() for _ in range(self.population)]

        for _ in range(generations):
            scored = []
            for tree in population:
                f = lambda x: tree.evaluate(x)
                if self.manifold.admissible(f, data, isogeny_pairs, scrambled):
                    score = np.var([f(x) for x in data])
                else:
                    score = -np.inf
                scored.append((score, tree))

            scored.sort(key=lambda t: t[0], reverse=True)
            population = [t for _, t in scored[: self.population // 2]]

            while len(population) < self.population:
                t1, t2 = random.sample(population, 2)
                child = self.crossover(t1, t2)
                child = self.mutate(child)
                population.append(child)

        return population[0]
