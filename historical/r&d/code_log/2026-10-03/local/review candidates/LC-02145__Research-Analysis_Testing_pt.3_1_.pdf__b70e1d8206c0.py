        fib.append(fib[i-1] + fib[i-2])


    return fib





def random_fibonacci_pair(n, classifier=None, fib_list=None, X_data=None, force_failure=False):


    """Select a random Fibonacci pair, biased by classifier or heuristic."""


    if fib_list is None:


        fib_list = generate_fibonacci(n)


    valid_fibs = [f for f in fib_list if f != 0 and f <= 1000]


    large_fibs = [f for f in fib_list if f > 1000 and f <= 5000]


    if len(valid_fibs) < 2:


        return random.choice(fib_list), random.choice(fib_list)





    if force_failure and large_fibs:


        return random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)





    if classifier is None or X_data is None or len(X_data) < 10:


        small_fibs = [f for f in valid_fibs if f <= 200]


        if len(small_fibs) >= 2:


            return random.sample(small_fibs, 2)