import sage.all
from sage.all import EllipticCurve, log, plot
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LogisticRegression
import uuid


# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = KAPPA ** 0.5
VIRGO_DISTANCE = 54e6  # light-years
VIRGO_COMOVING_VOLUME = 1e9  # Mly^3
VIRGO_DENSITY_HEIGHT = 6320


# Generate Fibonacci numbers
def generate_fibonacci(n):
    fibs = [0, 1]
    for i in range(2, n + 1):
        fibs.append(fibs[i-1] + fibs[i-2])
    return fibs


# Random Fibonacci pair with bias toward high-rank pairs
def random_fibonacci_pair(fibs, high_rank_pairs, bias=0.99):
    if np.random.random() < bias and high_rank_pairs:
        return np.random.choice(high_rank_pairs)
    return (np.random.choice(fibs), np.random.choice(fibs))


# Analyze elliptic curve
def analyze_curve(a, b, max_conductor=1e9):
    try:
        E = EllipticCurve([0, a, 0, b, 0])
        conductor = E.conductor()
        if conductor > max_conductor:
            return None
        rank = E.rank()
        selmer_rank = E.selmer_rank()
        analytic_rank = E.lseries().dokchitser().rank()
        omega = E.period_lattice().real_period()
        reg = E.regulator()
        tamagawa = E.tamagawa_product()
        leading_coeff = E.lseries().L_ratio() if rank == 0 else E.lseries().dokchitser().derivative(1, rank)
        return {
            'a': a, 'b': b, 'rank': rank, 'selmer_rank': selmer_rank,
            'analytic_rank': analytic_rank, 'omega': omega, 'reg': reg,
            'tamagawa': tamagawa, 'leading_coeff': leading_coeff,
            'discriminant': E.discriminant(), 'conductor': conductor
        }
    except Exception:
        return None


# Scaling transformations
def scale_invariants(data):
    cosmo_scale = VIRGO_DISTANCE / (data['omega'] * SQRT_KAPPA)
    denominator = {0: 1e13, 1: 1e14, 2: 5e13, 3: 3e11}.get(data['rank'], 1e13)
    scaled_period = data['omega'] * cosmo_scale
    comoving_volume = data['omega'] * data['reg'] * cosmo_scale**3 / denominator
    scaled_reg = data['reg'] * SQRT_KAPPA * (20 - 5 * data['rank'])
    return scaled_period, comoving_volume, scaled_reg


# Main test procedure
def main():
    fibs = generate_fibonacci(50)
    high_rank_pairs = [(2, 144), (377, 987), (-102, 918)]
    curves_data = []
    max_attempts = 50


    # Curve generation and analysis
    for _ in range(max_attempts):
        a, b = random_fibonacci_pair(fibs, high_rank_pairs)
        data = analyze_curve(a, b)
        if data:
            scaled_period, comoving_volume, scaled_reg = scale_invariants(data)
            data.update({
                'scaled_period': scaled_period,
                'comoving_volume': comoving_volume,
                'scaled_reg': scaled_reg
            })
            curves_data.append(data)


    # Train classifier
    X = [[d['a'], d['b'], log(abs(d['discriminant'])), log(d['conductor'])] for d in curves_data]
    y = [1 if d['rank'] >= 3 else 0 for d in curves_data]
    if len(set(y)) >= 2 and len(X) >= 5:
        clf = LogisticRegression().fit(X, y)
        print("Classifier trained successfully")


    # Visualization
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for d in curves_data:
        color = 'r' if d['rank'] == 3 else 'b' if d['rank'] == 2 else 'g' if d['rank'] == 1 else 'k'
        ax.scatter(
            log(abs(d['discriminant'])), log(d['conductor']), d['rank'],
            s=d['leading_coeff'] * 10, c=color, alpha=0.6
        )
    # Add Virgo Cluster marker
    ax.scatter([0], [0], [3], s=100, c='y', marker='*', label='Virgo Cluster')
    ax.set_xlabel('Log(Discriminant)')
    ax.set_ylabel('Log(Conductor)')
    ax.set_zlabel('Rank')
    plt.legend()
    plt.savefig('interweb_plot.png')


    # Save results
    with open('interweb_nodes.txt', 'w') as f:
        for d in curves_data:
            f.write(str(d) + '\n')


if __name__ == '__main__':
    main()
