"""Constrained genetic-programming primitives for symbolic regression."""

import random

import numpy as np

from .law_discovery_manifold import LawDiscoveryManifold


class GPNode:
    """Node in a GP expression tree."""

    def __init__(self, op, children=None, value=None):
        self.op = op
        self.children = children or []
        self.value = value

    def evaluate(self, x):
        if self.op == "const":
            return self.value
        if self.op == "var":
            return x[self.value]

        vals = [child.evaluate(x) for child in self.children]

        with np.errstate(over="raise", invalid="raise", divide="raise"):
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

        raise ValueError(f"Unknown operator: {self.op}")

    def depth(self):
        if not self.children:
            return 1
        return 1 + max(child.depth() for child in self.children)


class ConstrainedGP:
    """Constrained GP engine with a private, reproducible random stream."""

    def __init__(
        self,
        max_depth=6,
        population=50,
        mutation_rate=0.1,
        *,
        seed: int = 0,
    ):
        if population < 2:
            raise ValueError("population must be at least 2")
        self.manifold = LawDiscoveryManifold(max_depth=max_depth)
        self.max_depth = int(max_depth)
        self.population = int(population)
        self.mutation_rate = float(mutation_rate)
        self.seed = int(seed)
        self.rng = random.Random(self.seed)

    def random_tree(self, depth=0):
        if depth >= self.max_depth or self.rng.random() < 0.2:
            if self.rng.random() < 0.5:
                return GPNode("const", value=self.rng.uniform(-1, 1))
            return GPNode("var", value=self.rng.randint(0, 2))

        op = self.rng.choice(self.manifold.primitives)
        if op in ["log", "exp", "arctan"]:
            return GPNode(op, children=[self.random_tree(depth + 1)])
        return GPNode(
            op,
            children=[self.random_tree(depth + 1), self.random_tree(depth + 1)],
        )

    def mutate(self, tree):
        if self.rng.random() < self.mutation_rate:
            return self.random_tree()
        if tree.children:
            tree.children = [self.mutate(c) for c in tree.children]
        return tree

    def crossover(self, t1, t2):
        if self.rng.random() < 0.5:
            return t2
        if t1.children and t2.children:
            idx = self.rng.randint(0, len(t1.children) - 1)
            t1.children[idx] = self.crossover(
                t1.children[idx], self.rng.choice(t2.children)
            )
        return t1

    def evolve(self, data, isogeny_pairs, scrambled, generations=20):
        population = [self.random_tree() for _ in range(self.population)]

        for _ in range(int(generations)):
            scored = []
            for tree in population:
                f = lambda x, node=tree: node.evaluate(x)
                if self.manifold.admissible(f, data, isogeny_pairs, scrambled):
                    try:
                        values = np.asarray([f(x) for x in data], dtype=float)
                        score = float(np.var(values))
                        if not np.isfinite(score):
                            score = -np.inf
                    except (FloatingPointError, OverflowError, ValueError):
                        score = -np.inf
                else:
                    score = -np.inf
                scored.append((score, tree))

            scored.sort(key=lambda t: t[0], reverse=True)
            population = [t for _, t in scored[: max(2, self.population // 2)]]

            while len(population) < self.population:
                t1, t2 = self.rng.sample(population, 2)
                child = self.crossover(t1, t2)
                population.append(self.mutate(child))

        return population[0]
