import pymc3 as pm
with pm.Model():
    mu = pm.Normal('mu', mu=10.58, sd=1)
    sigma = pm.HalfNormal('sigma', sd=1)
    log_mass_model = pm.Lognormal('log_mass', mu=mu, sd=sigma, observed=log_mass)
    trace = pm.sample(2000, tune=1000)
filtered_log_mass = log_mass[pm.summary(trace)['mean']['log_mass'] > 0.95]  # High-probability
   * np.savetxt("filtered_log_mass.txt", filtered_log_mass, fmt='%.18f', header="log_mass = [", footer="];", comments='')
