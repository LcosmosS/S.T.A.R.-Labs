training_labels = [3, 3, 3, 3, 3, 3]
print(f"Initial training data: {training_data}")
print(f"Initial labels: {training_labels}")

# Store results for plotting
results = []

# Function to compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

# Function to analyze an elliptic curve
def analyze_curve(a, b, is_original=False, max_attempts=3, conductor_limit=1e14):
    print(f"\nFibonacci curve: y² = x³ + {a}x + {b}")

    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")
        return False, None, None, None, None, None, None, False, None, None

    delta = E.discriminant()