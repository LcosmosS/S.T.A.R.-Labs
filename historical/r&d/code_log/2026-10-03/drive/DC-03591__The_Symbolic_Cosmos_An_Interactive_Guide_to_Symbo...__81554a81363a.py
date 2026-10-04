# Generate Fibonacci numbers up to a specified index
def generate_fibonacci(n):
   fib = [0, 1]
   for i in range(2, n + 1):
       fib.append(fib[i-1] + fib[i-2])
   return fib

# Generate a list of candidate (a, b) pairs from Fibonacci numbers
fib_numbers = generate_fibonacci(25)
candidate_pairs = []
for i in range(2, len(fib_numbers)):
   for j in range(2, len(fib_numbers)):
       candidate_pairs.append((fib_numbers[i], fib_numbers[j]))
