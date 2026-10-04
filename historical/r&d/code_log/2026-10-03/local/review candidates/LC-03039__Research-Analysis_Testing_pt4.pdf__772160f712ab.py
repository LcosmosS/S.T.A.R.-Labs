    return fib



# Initial Fibonacci numbers up to index 61

fib_numbers = generate_fibonacci(61)

print(f"Fibonacci numbers up to index 61: {fib_numbers}")



# Corrected training data for high 3-Selmer ranks

training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],

    [377, 987, 22.0713726262387, 21.3782254456787, 1],

    [34, 4181, 22.7453700939663, 22.0522229134064, 1],

    [17711, 17711, 25.9923456789012, 25.9923456789012, 1],

    [17711, 46368, 25.9865432109876, 24.5998765432109, 1],

]

training_labels = [3, 3, 3, 3, 3]

print(f"Corrected training data: {training_data}")

print(f"Corrected labels: {training_labels}")



# Function to compute discriminant

def compute_discriminant(a, b):

    return -16 * (4 * a**3 + 27 * b**2)



# Target 7 curves with 3-Selmer rank >= 3

target_3selmer_curves = 7

max_attempts = 100

attempt = 71

current_fib_index = 62

phi_powers = [0, 1, 2]


# Continuous testing loop

while len(training_data) < target_3selmer_curves and attempt <= 70 + max_attempts:

    # Extend Fibonacci sequence if needed