def random_fibonacci_pair(fibs, lucas, high_rank_pairs, bias=0.99):
if np.random.random() < bias and high_rank_pairs:
idx = np.random.randint(len(high_rank_pairs))
return high_rank_pairs[idx]
use_lucas = np.random.random() < 0.5
numbers = lucas if use_lucas else fibs
return (np.random.choice(numbers), np.random.choice(numbers))
