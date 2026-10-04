fib = [0, 1]
if n < 2:
return fib[:n+1]
for i in range(2, n+1):
fib.append(fib[i-1] + fib[i-2])
return fib
def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None,
force_failure=False):
"""Select a random Fibonacci pair, biased toward rank ≥ 3 or successful curves."""
if fib_list is None:
fib_list = generate_fibonacci(n)
valid_fibs = [f for f in fib_list if f != 0 and f <= 2000] # Increased limit
large_fibs = [f for f in fib_list if f > 2000 and f <= 10000]
if len(valid_fibs) < 2:
return random.choice(fib_list), random.choice(fib_list)
if force_failure and large_fibs:
return random.sample(large_fibs, 2) if len(large_fibs) >= 2 else
random.sample(valid_fibs, 2)
# Bias toward pairs that yielded rank 3 (e.g., a=2, b=144)
high_rank_fibs = [f for f in valid_fibs if f in [1, 2, 5, 144, 233]]
if classifier is None or X_data is None or len(X_data) < 10:
if len(high_rank_fibs) >= 2 and random.random() < 0.5:
return random.sample(high_rank_fibs, 2)
small_fibs = [f for f in valid_fibs if f <= 200]
if len(small_fibs) >= 2:
return random.sample(small_fibs, 2)
return random.sample(valid_fibs, 2)
best_score = -float('inf')
best_pair = None
attempts = min(50, len(valid_fibs) * (len(valid_fibs) - 1) // 2)
for _ in range(attempts):
a, b = random.sample(valid_fibs, 2)
delta = -16 * (4 * a**3 + 27 * b**2)
log_delta = math.log(abs(delta)) if delta != 0 else 0
log_cond = math.log(max(abs(a), abs(b), 1)) * 2
tors_order = 1 # Default assumption
X = np.array([[a, b, log_delta, log_cond, tors_order]])
score = classifier.predict_proba(X)[0, 1]
if score > best_score:
best_score = score
best_pair = (a, b)
return best_pair if best_pair else random.sample(valid_fibs, 2)
def analyze_curve(a, b, is_original=False, max_attempts=5, require_3selmer=False):
"""Analyze an elliptic curve, mapping invariants to cosmological parameters."""
curve_name = 'Original curve' if is_original else 'Fibonacci curve'
print(f"\n{curve_name}: y² = x³ + {a}x + {b}")
try:
E = EllipticCurve(QQ, [0, 0, 0, a, b])
except ValueError as e:
print(f"Error creating curve: {e}")
return False, None, None, None, None, None, None, False
delta = E.discriminant()
conductor = E.conductor()
