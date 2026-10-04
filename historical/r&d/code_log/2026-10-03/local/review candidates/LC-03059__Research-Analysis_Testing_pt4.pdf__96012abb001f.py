# Main testing loop
target_3selmer_curves = 7
max_attempts = 86  # Match the attempts in the output
attempt = 71
current_fib_index = 62
phi_powers = [0, 1, 2]

while attempt <= max_attempts:
    if current_fib_index >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")
    current_fib_index += 1

    a_idx = (attempt - 71) % 20
    b_idx = (attempt - 71) % len(fib_numbers)