   for i in range(2, n + 1):
       fib.append(fib[i-1] + fib[i-2])
   return fib

def generate_candidate_curves(max_fib_index=20):
   """Generates a list of (a, b) pairs from Fibonacci numbers."""
   fib_numbers = generate_fibonacci(max_fib_index)
