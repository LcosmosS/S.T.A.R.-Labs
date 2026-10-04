    a_new = a * u**4
    b_new = b * u**6
    return a_new, b_new

def analyze_curve(a, b, is_original=False, max_attempts=5, require_3selmer=False,
conductor_limit=1e11):
