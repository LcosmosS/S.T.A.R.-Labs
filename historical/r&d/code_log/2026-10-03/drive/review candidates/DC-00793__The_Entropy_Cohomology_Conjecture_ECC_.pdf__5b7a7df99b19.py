# Load entropy-aligned dataset
data = pd.read_csv("final_merged_entropy_projection_dataset.csv")# ECC symbolic features
features = [
'log_Mass_gas', 'log_Mass_stellar', 'Av_gas_Re', 'OH_O3N2_cen',
'Smooth', 'Featured', 'pS', 'fM', 'z', 'Re_kpc',
'L_cosmo(s)', 'BSD_likelihood'
]
target = 'log_SFR_Ha'
# Split data
X, y = data[features], data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
