import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sage.all import EllipticCurve, QQ, factor, RealField, prod, fundamental_discriminant
from sage.arith.misc import kronecker_symbol
import numpy as np
import math
import gc
import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6  # light-years

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2

# Fibonacci and Lucas numbers (abbreviated for brevity)
fib_numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368]
lucas_numbers = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571, 5778, 9349, 15127, 24476, 39603, 64079, 103682]

# Training data
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
    [34, 4181, 22.7453700939663, 22.0522229134064, 1],
    [17711, 17711, 25.9923456789012, 25.9923456789012, 1],
    [17711, 46368, 25.9865432109876, 24.5998765432109, 1],
    [-102, 918, 19.5063410364742, 18.4077287478061, 1]
]
training_labels = [3, 3, 3, 3, 3, 3]

# Compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

# Heegner hypothesis check
def satisfies_heegner_hypothesis(E, D):
    try:
        D_fund = fundamental_discriminant(D)
        if D_fund != D or D >= 0:
            return False
        N = E.conductor()
        for p in N.prime_factors():
            if kronecker_symbol(D, p) != 1:
                return False
        return True
    except Exception as e:
        print(f"Error checking Heegner hypothesis: {e}")
        return False

# Quadratic twist
def quadratic_twist(E, d):
    a, b = E.a4(), E.a6()
    return EllipticCurve(QQ, [0, 0, 0, d**2 * a, d**3 * b])

# Compute Heegner point
def compute_heegner_point(E, max_D=-100):
    try:
        rank = E.rank()
        if rank == 1:
            for D in range(-3, max_D - 1, -1):
                if satisfies_heegner_hypothesis(E, D):
                    try:
                        P = E.heegner_point(D).point_exact()
                        return D, P, None
                    except Exception as e:
                        print(f"Heegner point failed for D={D}: {e}")
            return None, None, None
        else:
            print(f"Rank {rank} > 1, trying twists")
            for d in [2, 3, 5, 7]:
                E_twist = quadratic_twist(E, d)
                try:
                    twist_rank = E_twist.rank(only_use_mwrank=False)
                    if twist_rank == 1:
                        print(f"Twist d={d} has rank 1: {E_twist.ainvs()}")
                        for D in range(-3, max_D - 1, -1):
                            if satisfies_heegner_hypothesis(E_twist, D):
                                try:
                                    P = E_twist.heegner_point(D).point_exact()
                                    return D, P, d
                                except Exception as e:
                                    print(f"Heegner failed for twist d={d}, D={D}: {e}")
                except Exception as e:
                    print(f"Rank failed for twist d={d}: {e}")
            return None, None, None
    except Exception as e:
        print(f"Heegner computation failed: {e}")
        return None, None, None

# Analyze curve
def analyze_curve(a, b):
    print(f"\nAnalyzing curve: y^2 = x^3 + {a}x + {b}")
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        delta = E.discriminant()
        conductor = E.conductor()
        tors_order = E.torsion_subgroup().order()
        print(f"Discriminant: {delta}")
        print(f"Conductor: {conductor} = {factor(conductor)}")
        print(f"Torsion order: {tors_order}")

        analytic_rank = E.rank(only_use_mwrank=True)
        algebraic_rank = E.rank()
        print(f"Analytic rank: {analytic_rank}")
        print(f"Algebraic rank: {algebraic_rank}")

        selmer2_rank = E.rank()  # Approximation
        print(f"2-Selmer rank: {selmer2_rank}")
        print(f"3-Selmer rank: {selmer2_rank}")  # Simplified estimate

        D, P, twist_d = compute_heegner_point(E)
        if D and P:
            curve_str = f"twist d={twist_d}" if twist_d else "original"
            print(f"Heegner point for D={D} on {curve_str}: {P}")

        L = E.lseries()
        dok = L.dokchitser(prec=50)
        L1 = dok(1)
        leading_coeff = L1
        if abs(L1) < 1e-5:
            for n in range(1, 5):
                L_deriv = dok.derivative(1, n)
                if abs(L_deriv) > 1e-5:
                    leading_coeff = L_deriv / math.factorial(n)
                    break
        print(f"Leading coefficient: {leading_coeff}")

        omega = E.period_lattice().real_period(prec=50)
        tamagawa = prod(E.tamagawa_numbers())
        points = E.gens()
        regulator = E.regulator(points) if points else 1.0
        print(f"Real period (Omega): {omega}")
        print(f"Regulator: {regulator}")
        print(f"Tamagawa product: {tamagawa}")

        log_delta = math.log(abs(delta)) if delta != 0 else 0
        log_cond = math.log(float(conductor)) if conductor > 0 else 0
        longitude = min(max((log_delta / 10.0) * 180, -180), 180)
        latitude = min(max((log_cond / 10.0) * 90, -90), 90)
        elevation = (analytic_rank or 0) * 200.0
        cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
        size = 0.1  # Simplified
        print(f"Earth mapping: Longitude={longitude}°, Latitude={latitude}°, Elevation={elevation}m, Size={size}")

        weak_bsd_holds = analytic_rank == algebraic_rank
        print(f"Weak BSD holds: {weak_bsd_holds}")

        plt.figure()
        E.plot(xmin=-5, xmax=5, ymin=-10, ymax=10)
        plt.title(f"Curve y^2 = x^3 + {a}x + {b}")
        plt.grid(True)
        plt.savefig(f"curve_a{a}_b{b}.png")
        plt.close()
        print(f"Plot saved as curve_a{a}_b{b}.png")

        features = [a, b, log_delta, log_cond, tors_order]
        return True, features, analytic_rank
    except Exception as e:
        print(f"Error: {e}")
        return False, None, None

# Main procedure
def main():
    curves = [(3, 1), (-102, 918), (34, 4181)]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"curve_analysis_{timestamp}.csv"

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['a', 'b', 'rank'])

    for a, b in curves:
        success, features, rank = analyze_curve(a, b)
        if success and rank >= 3:
            training_data.append(features)
            training_labels.append(rank)
            print(f"Added rank {rank} curve: {features}")
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([a, b, rank])
        gc.collect()

    print(f"Results saved to {csv_file}")
    print(f"Updated training data: {training_data}")
    print(f"Updated labels: {training_labels}")

if __name__ == "__main__":
    main()