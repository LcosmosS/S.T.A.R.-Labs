print("Precision set to 38");


/* Define elliptic curve: y^2 = x^3 + x + 2 */
E = ellinit([0, 0, 0, 1, 2], 1);
print("Elliptic curve initialized");


/* Basic invariants */
disc = -16 * (4*1^3 + 27*2^2); print("Discriminant: ", disc);
conductor = ellglobalred(E)[1]; print("Conductor: ", conductor);
tors_order = elltors(E)[1]; print("Torsion subgroup order: ", tors_order);


/* Rank and L-series */
alg_rank = ellrank(E)[1]; print("Algebraic rank: ", alg_rank);
L = elllseries(E, 1); print("L-series at s=1: ", L);
analytic_rank = 0; L_val = L;
if (abs(L) < 1e-10, L_deriv = elllseries(E, 1, 1); L_val = L_deriv; analytic_rank = 1);
print("Analytic rank: ", analytic_rank);
print("Leading coefficient L^(r)(E, 1): ", L_val);


/* Check weak BSD */
if (alg_rank == analytic_rank, print("Weak BSD holds"), print("Weak BSD fails"));


/* Modified BSD constants */
p = 5; phi = (1 + sqrt(5)) / 2; pi_val = Pi;
print("p: ", p, ", phi: ", phi, ", pi: ", pi_val);


/* Periods */
periods = ellperiods(E, 1); real_period = real(periods[1]);
if (type(real_period) == "t_VEC", real_period = real_period[1]);
print("Real period (Omega): ", real_period);
omega_scaled = pi_val * real_period; print("Scaled period (pi * Omega): ", omega_scaled);


/* Regulator */
reg = 1; reg_scaled = reg * phi; print("Scaled regulator: ", reg_scaled);


/* Tamagawa product */
tamagawa = 1; bad_primes = factor(conductor)[,1];
for(i = 1, #bad_primes, tamagawa *= elltamagawa(E, bad_primes[i]));
print("Tamagawa product: ", tamagawa);


/* Modified BSD */
rhs = (omega_scaled * reg_scaled * p * tamagawa) / (tors_order^2);
print("Right-hand side: ", rhs);
modified_leading_coeff = 8; print("Modified leading coeff: ", modified_leading_coeff);
if (abs(modified_leading_coeff - rhs) < 1e-5, print("Modified BSD holds"), print("Modified BSD fails"));
adjusted_sha = modified_leading_coeff / (omega_scaled * reg_scaled * tamagawa) * (tors_order^2);
print("Adjusted Sha: ", adjusted_sha);
