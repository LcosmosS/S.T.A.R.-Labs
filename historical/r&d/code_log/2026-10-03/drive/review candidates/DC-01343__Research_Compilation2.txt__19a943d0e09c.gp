n = length(v);


s = vecsort(v);


if (n % 2 == 1,


    return(s[(n+1)/2]),


    return((s[n/2] + s[n/2 + 1]) / 2)
