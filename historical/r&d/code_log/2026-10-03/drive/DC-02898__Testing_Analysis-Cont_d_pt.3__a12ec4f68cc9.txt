print("Precision set to 38");


/* Define the elliptic curve */
curves = [[1, 2]];  /* Curve: y^2 = x^3 + x + 2 */
print("Curves defined: ", curves);
i = 1;
print("Processing curve ", i);
a = curves[i][1];
b = curves[i][2];
print("Curve: y^2 = x^3 + ", a, "x + ", b);
E = ellinit([0, 0, 0, a, b], 1);  /* Initialize with real flag */
print("Elliptic curve initialized");


/* Compute basic invariants */
disc = -16 * (4*a^3 + 27*b^2);
print("Discriminant: ", disc);
conductor = ellglobalred(E)[1];
print("Conductor: ", conductor);
tors = elltors(E);
tors_order = tors[1];
print("Torsion subgroup order: ", tors_order);


/* Compute rank and L-series */
rank_data = ellrank(E);
alg_rank = rank_data[1];
print("Algebraic rank: ", alg_rank);
L = elllseries(E, 1);
print("L-series at s=1: ", L);
analytic_rank = 0;
L_val = L;
if (abs(L) < 1e-10, L_deriv = elllseries(E, 1, 1); L_val = L_deriv; analytic_rank = 1);
if (analytic_rank == 1 && abs(L_deriv) < 1e-10, L_deriv2 = elllseries(E, 1, 2); L_val = L_deriv2; analytic_rank = 2);
print("Analytic rank: ", analytic_rank);
print("Leading coefficient L^(r)(E, 1): ", L_val);


/* Check weak BSD */
if (alg_rank == analytic_rank, print("Weak BSD holds: Algebraic rank = Analytic rank"), print("Weak BSD fails: Algebraic rank != Analytic rank"));


/* Define constants for modification */
p = 5;
print("p set to: ", p);
phi = (1 + sqrt(5)) / 2;
print("phi set to: ", phi);
pi_val = Pi;
print("pi_val set to: ", pi_val);


/* Compute p-adic L-function */
L_padic = ellpadicL(E, p, 10);
L_padic_val = polcoeff(L_padic, 0);
print("p-adic L-function at s=1 (p=", p, "): ", L_padic_val);
L_padic_val_valuation = valuation(L_padic_val, p);
if (L_padic_val_valuation > 0, print("p-adic L-function suggests higher rank"), print("p-adic L-function suggests rank 0"));


/* Compute periods numerically */
periods = ellperiods(E, 1);  /* Real periods */
omega = periods[1];         /* Real period */
print("Real period (Omega): ", omega);
omega_scaled = pi_val * omega;
print("Scaled real period (Omega * pi): ", omega_scaled);


/* Compute regulator */
reg = 1;  /* Default for rank 0 */
if (alg_rank != 0, gens = ellgenerators(E); if (#gens > 0, reg = ellheight(E, gens[1])));
reg_scaled = reg * phi;
print("Scaled regulator (Reg * phi): ", reg_scaled);


/* Compute Tamagawa product over all bad primes */
tamagawa = 1;
bad_primes = factor(conductor)[,1];
for (i = 1, #bad_primes, tamagawa = tamagawa * elltamagawa(E, bad_primes[i]));
print("Product of Tamagawa numbers: ", tamagawa);


/* Compute right-hand side of modified strong BSD */
rhs = (omega_scaled * reg_scaled * p * tamagawa) / (tors_order^2);
print("Right-hand side of modified strong BSD: ", rhs);


/* Define modified leading coefficient and check */
modified_leading_coeff = 8;  /* As given in the original script */
print("Modified leading coefficient (F_6 = 8): ", modified_leading_coeff);
if (abs(modified_leading_coeff - rhs) < 1e-5, print("Modified strong BSD holds with pi and phi substitutions"), print("Modified strong BSD fails with pi and phi substitutions"));


/* Compute adjusted Sha */
adjusted_sha = modified_leading_coeff / (omega_scaled * reg_scaled * tamagawa) * (tors_order^2);
print("Adjusted |Sha(E)| to match: ", adjusted_sha);
