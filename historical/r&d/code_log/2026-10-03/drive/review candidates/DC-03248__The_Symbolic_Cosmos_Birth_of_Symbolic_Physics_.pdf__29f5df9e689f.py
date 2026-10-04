# Initialize data
X_data = []
y_data = []
classifier = None
interweb_data = []
# Main loop
max_successful_curves = 15 # Increased to find more rank 3 curves
max_total_attempts = 50
n = 20 # Extended Fibonacci sequence
137require_3selmer = False # Toggle to True for 3-Selmer focus
successful_curves = 0
attempts = 0
fib_numbers = generate_fibonacci(n)
print(f"Fibonacci numbers up to index {n}: {fib_numbers}")
with open("interweb_nodes.txt", "w") as f:
f.write("a,b,rank,normalized_leading_coeff,omega,regulator,tamagawa,weak_bsd_holds,log
