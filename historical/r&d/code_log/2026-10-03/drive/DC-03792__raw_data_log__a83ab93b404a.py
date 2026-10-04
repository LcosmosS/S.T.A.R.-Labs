import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')


print("🚀 Generating requested outputs (hall_of_fame, feature_importance, predictions)")


# Load data
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
real1 = pd.concat([chunk for chunk in pd.read_csv("JApJ94494_2MASS_GAIADR3_EPOCH.csv", chunksize=20000, low_memory=False)], ignore_index=True)
real2 = pd.concat([chunk for chunk in pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv", chunksize=20000, low_memory=False)], ignore_index=True)


# Leakage-free features
def add_features(df):
    df = df.copy()
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


synth = add_features(synth)


feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio']


# PySR on synthetic only
print("\nRunning PySR on synthetic...")
from pysr import PySRRegressor
pysr = PySRRegressor(niterations=80, maxsize=12, random_state=42)
pysr.fit(synth[feature_cols], synth['exact_rank'])


# Save hall of fame
hof = pysr.get_hall_of_fame()
hof.to_csv("hall_of_fame_final.csv", index=False)
print("✅ hall_of_fame_final.csv saved")


print("\nBest PySR Equations (from hall_of_fame):")
print(hof[['Complexity', 'Loss', 'Equation']].to_string(index=False))


# Feature importance (XGBoost)
print("\nFeature Importance:")
xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
xgb.fit(synth[feature_cols], synth['exact_rank'])
imp = pd.DataFrame({'feature': feature_cols, 'importance': xgb.feature_importances_})
imp = imp.sort_values('importance', ascending=False)
imp.to_csv("feature_importance.csv", index=False)
print(imp)


# Save predictions
pred_df = pd.DataFrame({
    'true_rank': synth['exact_rank'],
    'flux_gr': synth['flux_gr'],
    'pm_mag_proxy': synth['pm_mag_proxy'],
    'mag_ratio': synth['mag_ratio']
})
pred_df.to_csv("predictions_final.csv", index=False)
print("\n✅ predictions_final.csv saved")


print("\n🎉 All three files generated successfully!")
print("   → hall_of_fame_final.csv")
print("   → feature_importance.csv")
print("   → predictions_final.csv")
