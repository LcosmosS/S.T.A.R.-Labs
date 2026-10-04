    v_sorted = vecsort(v);
    n = length(v);
    if (n % 2 == 1,
        v_sorted[(n+1)\2],
        (v_sorted[n\2] + v_sorted[n\2 + 1]) / 2
