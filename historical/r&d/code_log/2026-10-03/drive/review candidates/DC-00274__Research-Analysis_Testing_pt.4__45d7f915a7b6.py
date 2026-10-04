# Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, heegner_points, Integer
import math
import gc  # For garbage collection to manage memory


# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6
VIRGO_COMOVING_VOLUME = 1e9


# Golden ratio
PHI = (1 + math.sqrt(5)) / 2
print(f"Golden ratio (φ): {PHI}")


# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib


# Fibonacci numbers up to index 77 (from previous run)
fib_numbers = generate_fibonacci(77)
print(f"Fibonacci numbers up to index 77: {fib_numbers}")


# Training data (from previous run, including twisted curve)
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
