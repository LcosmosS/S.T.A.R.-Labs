    return fib





def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None):


    """Select a random Fibonacci pair, biased by classifier or heuristic."""


    if fib_list is None:


        fib_list = generate_fibonacci(n)


    valid_fibs = [f for f in fib_list if f != 0 and f <= 5000]  # Tighter cap


    if len(valid_fibs) < 2:


        return random.choice(fib_list), random.choice(fib_list)





    if classifier is None or X_data is None or len(X_data) < 10:


        # Heuristic: prefer smaller coefficients to reduce conductor


        small_fibs = [f for f in valid_fibs if f <= 1000]


        if len(small_fibs) >= 2:


            return random.sample(small_fibs, 2)


        return random.sample(valid_fibs, 2)





    # Use classifier


    best_score = -float('inf')