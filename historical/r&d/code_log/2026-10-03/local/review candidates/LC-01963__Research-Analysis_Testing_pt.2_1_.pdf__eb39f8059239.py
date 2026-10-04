# Define the Fibonacci function
def fibonacci(n):
    if n < 0:
        raise ValueError("Fibonacci sequence not defined for negative indices")
    if n == 0:
        return 0
    if n == 1:
        return 1
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib[n]

# Define the pairs of indices
pairs = [(5, 7), (6, 8), (7, 9)]

# Loop over each pair to construct and analyze the curve
for n1, n2 in pairs:
    a = fibonacci(n1)
    b = fibonacci(n2)
    print(f"\nCurve with a = F_{n1} = {a}, b = F_{n2} = {b}: y^2 = x^3 + {a}x + {b}")

    # Define the elliptic curve
    E = EllipticCurve(QQ, [a, b])

    # Compute the discriminant
    delta = E.discriminant()
    print(f"Discriminant: {delta}")
    if delta == 0:
        print("Not an elliptic curve (singular). Skipping.")
        continue

    # Compute the conductor
    conductor = E.conductor()
    print(f"Conductor: {conductor}")

    # Compute the torsion subgroup
    tors = E.torsion_subgroup()
    tors_order = tors.order()
    print(f"Torsion subgroup order: {tors_order}")
