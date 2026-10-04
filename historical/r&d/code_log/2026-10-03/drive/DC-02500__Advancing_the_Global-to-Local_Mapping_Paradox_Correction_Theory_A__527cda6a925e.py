def generate_lucas(n):
lucas = [2, 1]
for i in range(2, n + 1):
lucas.append(lucas[i-1] + lucas[i-2])
return lucas
lucas_numbers = generate_lucas(77)
print(f"Lucas numbers up to index 77: {lucas_numbers}")
