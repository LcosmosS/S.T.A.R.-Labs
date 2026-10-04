stellar_masses = pd.read_csv('StellarMassesLambdar.csv')[['CATAID', 'logmstar', 'extBV', 'gminusi', 'uminusr']]
galaxies_classified = pd.read_csv('GalaxiesClassified.csv')[['CATAID', 'Z', 'GeoS4', 'GeoS10']]
environment_measures = pd.read_csv('EnvironmentMeasures.csv')[['CATAID', 'DistanceTo5nn', 'SurfaceDensity',
'CountInCyl', 'AGEDenPar']]


# --- Merge Datasets ---
print("Merging datasets on 'CATAID'...")
data = pd.merge(magphys, stellar_masses, on='CATAID', how='inner')
data = pd.merge(data, galaxies_classified, on='CATAID', how='inner')
data = pd.merge(data, environment_measures, on='CATAID', how='inner')


# --- Feature Engineering ---
print("Engineering features...")
data['log_mass_stellar'] = np.log10(data['mass_stellar_best_fit'])
data['log_sSFR'] = np.log10(data['sSFR_0_1Gyr_best_fit'] + 1e-6)
data['log_dust_mass'] = np.log10(data['mass_dust_best_fit'] + 1e-6)
data['log_Z'] = np.log10(data['metalicity_Z_Zo_percentile50'] + 1e-6)


# BSD-inspired feature
data['BSD_likelihood'] = data['log_mass_stellar'] * data['log_Z'] / (data['agem_percentile50'] + 1)


# --- Define Features and Target ---
features = [
