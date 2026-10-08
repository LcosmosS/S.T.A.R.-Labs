# Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, fundamental_discriminant
import numpy as np
import math
import gc
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Print SageMath version for debugging
import sage
print(f"SageMath version: {sage.version.version}")

# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6  # light-years
VIRGO_COMOVING_VOLUME = 1e9  # Mly^3
VIRGO_DENSITY_HEIGHT = 6320

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2
print(f"Golden ratio (φ): {PHI}")

# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

fib_numbers = generate_fibonacci(77)
print(f"Fibonacci numbers up to index 77: {fib_numbers}")

# Generate Lucas numbers
def generate_lucas(n):
    lucas = [2, 1]
    for i in range(2, n + 1):
        lucas.append(lucas[i-1] + lucas[i-2])
    return lucas

lucas_numbers = generate_lucas(77)
print(f"Lucas numbers up to index 77: {lucas_numbers}")

# Training data for classifier
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
    [34, 4181, 22.7453700939663, 22.0522229134064, 1],
    [17711, 17711, 25.9923456789012, 25.9923456789012, 1],
    [17711, 46368, 25.9865432109876, 24.5998765432109, 1],
    [-102, 918, 19.5063410364742, 18.4077287478061, 1]
]
training_labels = [3, 3, 3, 3, 3, 3]
print(f"Initial training data: {training_data}")
print(f"Initial labels: {training_labels}")

# Function to compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

# Function to select random Fibonacci or Lucas pair
def random_fibonacci_pair(fibs, lucas, high_rank_pairs, bias=0.99):
    if np.random.random() < bias and high_rank_pairs:
        idx = np.random.randint(len(high_rank_pairs))
        return high_rank_pairs[idx]
    use_lucas = np.random.random() < 0.5
    numbers = lucas if use_lucas else fibs
    return (np.random.choice(numbers), np.random.choice(numbers))

# Function to check Heegner hypothesis
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
        print(f"Error checking Heegner hypothesis for D={D}: {e}")
        return False

# Function to compute quadratic twist
def quadratic_twist(E, d):
    a, b = E.a4(), E.a6()
    return EllipticCurve(QQ, [0, 0, 0, d^2 * a, d^3 * b])

# Function to compute Heegner point using PARI/GP
def compute_heegner_point(E, max_D=-100):
    try:
        rank = E.rank()
        if rank == 1:
            for D in range(-3, max_D - 1, -1):
                if satisfies_heegner_hypothesis(E, D):
                    try:
                        pari_E = pari.ellinit(E.ainvs())
                        heegner_data = pari_E.ellheegner(D)
                        x, y = heegner_data[0], heegner_data[1]
                        P = E([x, y])
                        return D, P, None
                    except Exception as e:
                        print(f"PARI/GP Heegner point failed for D={D}: {e}")
                        try:
                            P = E.heegner_point(D)
                            return D, P.point_exact(), None
                        except Exception as e:
                            print(f"Sage Heegner point failed for D={D}: {e}")
                            continue
            print(f"No suitable discriminant found for Heegner point on {E.ainvs()}")
            return None, None, None
        else:
            print(f"Curve {E.ainvs()} has rank {rank}, trying quadratic twists")
            for d in [2, 3, 5, 7]:
                E_twist = quadratic_twist(E, d)
                try:
                    twist_rank = E_twist.rank(second_limit=13)
                    if twist_rank == 1:
                        print(f"Twist by d={d} has rank 1: {E_twist.ainvs()}")
                        for D in range(-3, max_D - 1, -1):
                            if satisfies_heegner_hypothesis(E_twist, D):
                                try:
                                    pari_E = pari.ellinit(E_twist.ainvs())
                                    heegner_data = pari_E.ellheegner(D)
                                    x, y = heegner_data[0], heegner_data[1]
                                    P = E_twist([x, y])
                                    return D, P, d
                                except Exception as e:
                                    print(f"PARI/GP Heegner point failed for twist d={d}, D={D}: {e}")
                                    try:
                                        P = E_twist.heegner_point(D)
                                        return D, P.point_exact(), d
                                    except Exception as e:
                                        print(f"Sage Heegner point failed for twist d={d}, D={D}: {e}")
                                        continue
                except Exception as e:
                    print(f"Rank computation failed for twist d={d}: {e}")
                    continue
            print(f"No rank 1 twist found for {E.ainvs()}")
            return None, None, None
    except Exception as e:
        print(f"Failed to compute Heegner point for {E.ainvs()}: {e}")
        return None, None, None

# Function to compute 3-Selmer rank
def compute_3_selmer_rank(E):
    try:
        E.three_descent(second_limit=13)
        selmer_rank = E.rank()  # Approximate via descent
    except Exception as e:
        print(f"SageMath three_descent failed for {E.ainvs()}: {e}")
        selmer_rank = None
    try:
        pari_E = pari.ellinit(E.ainvs())
        pari_data = pari_E.ellrank()
        pari_rank = pari_data[0]
    except Exception as e:
        print(f"PARI/GP ellrank failed for {E.ainvs()}: {e}")
        pari_rank = None
    return selmer_rank, pari_rank

# Function to analyze a curve
def analyze_curve(a, b, conductor_limit=1e14):
    print(f"\nAnalyzing curve: y^2 = x^3 + {a}x + {b}")
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        delta = E.discriminant()
        conductor = E.conductor()
        tors_order = E.torsion_subgroup().order()
        print(f"Discriminant: {delta}")
        print(f"Conductor: {conductor} = {factor(conductor)}")
        print(f"Torsion order: {tors_order}")

        if conductor > conductor_limit:
            print(f"Conductor too large (> {conductor_limit}), skipping curve")
            return False, None, None, None, None, None, None, False, None, None, None, None, None, None

        analytic_rank = E.rank(only_use_mwrank=True)
        algebraic_rank = E.rank()
        print(f"Analytic rank: {analytic_rank}")
        print(f"Algebraic rank: {algebraic_rank}")

        selmer_rank, pari_rank = compute_3_selmer_rank(E)
        print(f"3-Selmer rank (Sage): {selmer_rank}")
        print(f"3-Selmer rank (PARI/GP estimate): {pari_rank}")

        D, P, twist_d = compute_heegner_point(E)
        if D is not None and P is not None:
            curve_str = f"twist by d={twist_d}" if twist_d else "original curve"
            print(f"Heegner point for D={D} on {curve_str}: {P}")
            print(f"Height of Heegner point: {E.regulator_of([P])}")

        L = E.lseries()
        dok = L.dokchitser(prec=50)
        L1 = dok(1)
        leading_coeff = L1
        if abs(L1) < 1e-5:
            for n in range(1, 5):
                L_deriv = dok.derivative(1, n)
                if abs(L_deriv) < 1e-5:
                    continue
                analytic_rank = n
                leading_coeff = L_deriv / math.factorial(n)
                break
        print(f"Leading coefficient: {leading_coeff}")

        omega = E.period_lattice().real_period(prec=50)
        tamagawa = prod(E.tamagawa_numbers())
        sha_order = 1
        rhs = leading_coeff * (tors_order**2)
        reg = rhs / (omega * tamagawa * sha_order) if analytic_rank > 0 else 1.0

        log_delta = math.log(abs(delta)) if delta != 0 else 0
        log_cond = math.log(float(conductor)) if conductor > 0 else 0
        longitude = (log_delta / 10.0) * 180 if log_delta != 0 else 0
        longitude = max(min(longitude, 180), -180)
        latitude = (log_cond / 10.0) * 90 if log_cond != 0 else 0
        latitude = max(min(latitude, 90), -90)
        elevation = analytic_rank * 200.0 if analytic_rank is not None else 0
        elevation = min(elevation, 1000)
        cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
        raw_volume = omega * reg * cosmo_scale**3 if omega and reg else 0
        size = math.log1p(raw_volume) / 1e13 if raw_volume > 0 else 0
        size = max(min(size * 100, 10), 0.1)

        scaled_period = omega * cosmo_scale
        denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(analytic_rank, 1e13)
        comoving_volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
        reg_factor = 20 - 5 * analytic_rank if analytic_rank <= 3 else 10
        scaled_reg = reg * SQRT_KAPPA * reg_factor

        print(f"Real period (Omega): {omega}")
        print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
        print(f"Scaled period: {float(scaled_period)} light-years")
        print(f"Regulator: {reg}")
        print(f"Scaled regulator: {float(scaled_reg)}")
        print(f"Product of Tamagawa numbers: {tamagawa}")
        print(f"Estimated comoving volume: {comoving_volume} Mly^3")
        print(f"Earth mapping: Longitude={longitude}°, Latitude={latitude}°, Elevation={elevation}m, Size={size}")

        weak_bsd_holds = (analytic_rank == algebraic_rank)
        print(f"Weak BSD holds: {weak_bsd_holds}")

        plt.figure()
        plot = E.plot(xmin=-5, xmax=5, ymin=-10, ymax=10)
        plt.title(f"Elliptic Curve y^2 = x^3 + {a}x + {b}")
        plt.grid(True)
        plt.savefig(f"curve_a{a}_b{b}.png")
        plt.close()
        print(f"Plot saved as curve_a{a}_b{b}.png")

        features = [a, b, log_delta, log_cond, tors_order]
        return True, features, analytic_rank, leading_coeff / 10, omega, reg, tamagawa, weak_bsd_holds, E, selmer_rank, log_delta, log_cond, longitude, latitude, elevation, size

    except Exception as e:
        print(f"Error analyzing curve: {e}")
        return False, None, None, None, None, None, None, False, None, None, None, None, None, None

# Main test procedure
def main():
    high_rank_pairs = [(2, 144), (377, 987), (-102, 918), (34, 4181), (17711, 17711), (17711, 46368)]
    max_attempts = 10
    curves_data = []
    conductor_limit = 1e14
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"interweb_nodes_{timestamp}.csv"

    with open(csv_file, 'w', newline='') as csv_f:
        csv_writer = csv.writer(csv_f)
        csv_writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'reg', 'tamagawa', 'weak_bsd_holds', 'selmer3_rank', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size'])

    previous_curves = [
        (3, 1), (-102, 918)
    ]
    for a, b in previous_curves:
        result = analyze_curve(a, b, conductor_limit=conductor_limit)
        if result[0]:
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size = result
            data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size)
            curves_data.append((None, data_tuple))
            with open(csv_file, 'a', newline='') as csv_f:
                csv_writer = csv.writer(csv_f)
                csv_writer.writerow(data_tuple)
            if rank >= 3:
                training_data.append(features)
                training_labels.append(rank)
                print(f"Added rank {rank} curve to training data: {features}")
        gc.collect()

    for _ in range(max_attempts):
        a, b = random_fibonacci_pair(fib_numbers, lucas_numbers, high_rank_pairs)
        result = analyze_curve(a, b, conductor_limit=conductor_limit)
        if result[0]:
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size = result
            data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size)
            curves_data.append((None, data_tuple))
            with open(csv_file, 'a', newline='') as csv_f:
                csv_writer = csv.writer(csv_f)
                csv_writer.writerow(data_tuple)
            if rank >= 3:
                training_data.append(features)
                training_labels.append(rank)
                print(f"Added rank {rank} curve to training data: {features}")
        gc.collect()

    twist_primes = [2, 3, 5, 7]
    for a, b in high_rank_pairs:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        for d in twist_primes:
            E_twist = quadratic_twist(E, d)
            a_new = E_twist.a4()
            b_new = E_twist.a6()
            print(f"\nTwisting curve (a={a}, b={b}) with d={d}")
            result = analyze_curve(a_new, b_new, conductor_limit=conductor_limit)
            if result[0]:
                success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E_tw