n = length(logmass)
print("Number of original entries: ", n)


sorted_logmass = vecsort(logmass)
Q1_index = floor(0.25 * (n + 1))
Q3_index = floor(0.75 * (n + 1))
Q1 = sorted_logmass[Q1_index]
Q3 = sorted_logmass[Q3_index]
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR


filtered_logmass = select(x -> x >= lower_bound && x <= upper_bound, logmass)
n_filtered = length(filtered_logmass)
print("Number of filtered entries: ", n_filtered)


M = vector(n_filtered, i, 10^filtered_logmass[i])
sorted_M = vecsort(M)


if (n_filtered % 2 == 1,
    M0 = sorted_M[(n_filtered + 1)/2],
    M0 = (sorted_M[n_filtered / 2] + sorted_M[n_filtered / 2 + 1]) / 2
)


sum_M_over_M0 = sum(i=1, n_filtered, M[i] / M0)
sum_M0_over_M = sum(i=1, n_filtered, M0 / M[i])
K_theory = sum_M_over_M0 / sum_M0_over_M


print("Q1: ", Q1)
print("Q3: ", Q3)
print("IQR: ", IQR)
print("Lower bound: ", lower_bound)
print("Upper bound: ", upper_bound)
print("M0: ", M0)
print("K_theory: ", K_theory)
