# Suppress deprecation warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari
import numpy as np
import matplotlib.pyplot as plt


# Define precision for real numbers
RR = RealField(100)


# Function to check Heegner hypothesis
def satisfies_heegner_hypothesis(E, D):
    """
    Check if discriminant D satisfies the Heegner hypothesis for curve E.
    D must be a negative fundamental discriminant, and all primes dividing the conductor
    must split in the imaginary quadratic field K = Q(sqrt(D)).
    """
    if D >= 0:
        return False
    # Ensure D is a fundamental discriminant
    if D % 4 == 0:
        D0 = D // 4
        if not D0.is_squarefree():
            return False
    elif D % 4 == 1:
        return False
    else:
        if not D.is_squarefree():
            return False
    N = E.conductor()
    for p in N.prime_factors():
        # Check if p splits in Q(sqrt(D)) using Kronecker symbol
        if kronecker_symbol(D, p) != 1:
            return False
    return True


# Function to compute Heegner point
def compute_heegner_point(E, max_D=-100):
    """
    Attempt to compute a Heegner point for curve E using discriminants D >= max_D.
    Returns (D, point) if successful, else (None, None).
    """
    try:
        rank = E.rank()
        if rank != 1:
            print(f"Curve {E.ainvs()} has rank {rank}, Heegner points typically for rank 1")
            return None, None
        # Try negative fundamental discriminants
        for D in range(-3, max_D - 1, -1):
            if satisfies_heegner_hypothesis(E, D):
                try:
                    P = E.heegner_point(D)
                    return D, P
                except Exception as e:
                    continue
        print(f"No suitable discriminant found for Heegner point on {E.ainvs()}")
        return None, None
    except Exception as e:
        print(f"Failed to compute Heegner point for {E.ainvs()}: {e}")
        return None, None


# Function to compute 3-Selmer rank using Sage and PARI/GP
def compute_3_selmer_rank(E):
    """
    Compute the 3-Selmer rank of curve E using SageMath and validate with PARI/GP.
    Returns (Sage rank, PARI/GP rank).
    """
    try:
        # SageMath 3-Selmer rank
        sage_rank = E.selmer_rank(p=3)
    except Exception as e:
        print(f"SageMath selmer_rank failed for {E.ainvs()}: {e}")
        sage_rank = None


    try:
        # PARI/GP rank estimation
        pari_E = pari.ellinit(E.ainvs())
        pari_data = pari_E.ellrank()
        pari_rank = pari_data[0]  # Algebraic rank estimate
    except Exception as e:
        print(f"PARI/GP ellrank failed for {E.ainvs()}: {e}")
        pari_rank = None


    return sage_rank, pari_rank


# Function to analyze a curve
def analyze_curve(a, b):
    """
    Analyze elliptic curve y^2 = x^3 + ax + b.
    Compute ranks, 3-Selmer rank, and attempt Heegner point.
    """
    print(f"\nAnalyzing curve: y^2 = x^3 + {a}x + {b}")
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        conductor = E.conductor()
        print(f"Conductor: {factor(conductor)}")
        
        # Analytic and algebraic ranks
        analytic_rank = E.rank(only_use_mwrank=True)
        algebraic_rank = E.rank()
        print(f"Analytic rank: {analytic_rank}")
        print(f"Algebraic rank: {algebraic_rank}")
        
        # 3-Selmer rank
        selmer_rank, pari_rank = compute_3_selmer_rank(E)
        print(f"3-Selmer rank (Sage): {selmer_rank}")
        print(f"3-Selmer rank (PARI/GP estimate): {pari_rank}")
        
        # Heegner point
        D, P = compute_heegner_point(E)
        if D is not None and P is not None:
            print(f"Heegner point for D={D}: {P.point()}")
            print(f"Height of Heegner point: {RR(P.height())}")
        
        # Plot the curve
        plt.figure()
        plot = E.plot(xmin=-5, xmax=5, ymin=-10, ymax=10)
        plt.title(f"Elliptic Curve y^2 = x^3 + {a}x + {b}")
        plt.grid(True)
        plt.savefig(f"curve_a{a}_b{b}.png")
        plt.close()
        print(f"Plot saved as curve_a{a}_b{b}.png")
        
    except Exception as e:
        print(f"Error analyzing curve: {e}")


# Main execution
curves = [
    (3, 1),          # Rank 1 curve for Heegner point success
    (-102, 918)      # Rank 3 curve where Heegner point failed
]


for a, b in curves:
    analyze_curve(a, b)
