if 'umag' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'Jmag' in df.columns:
    features.extend(["color_JK", "e_color_JK"])
if 'color_ug' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'color_JK' in df.columns:
    features.extend(["color_JK", "e_color_JK"])

# Global imputation before feature selection
========================================================================
=====================================================================
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf],
np.nan).fillna(df[numeric_cols].median(skipna=True))

# Select features and target
========================================================================
========================================================================
=============
X = df[features]
y = df[target]
print(f"Rows after feature selection: {len(X)}")
print(f"NaN in y ({target}): {y.isna().sum()}")
missing_features = [f for f in features if f not in df.columns]
if missing_features:
    print(f"Warning: The following features are missing from the dataset: {missing_features}")
else:
    print("All features present in the dataset.")

# Correlation heatmap of numeric features
========================================================================
========================================================================
plt.figure(figsize=(12, 10))
sns.heatmap(X.corr(), annot=False, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Correlation Heatmap of Features")
plt.savefig("feature_correlation_heatmap.png")
plt.close()
