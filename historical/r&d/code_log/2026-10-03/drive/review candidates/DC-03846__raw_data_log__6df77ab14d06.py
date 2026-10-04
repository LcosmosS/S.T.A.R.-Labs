import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import glob


print("🔧 Fixing outputs from your last run...")


# 1. Load the hall_of_fame that PySR already saved
hof_path = sorted(glob.glob("outputs/*/hall_of_fame.csv"))[-1]
hof = pd.read_csv(hof_path)
hof.to_csv("hall_of_fame_final.csv", index=False)
print("✅ hall_of_fame_final.csv saved")


print("\nBest PySR equations (leakage-free):")
print(hof[['Complexity', 'Loss', 'Equation']].to_string(index=False))


# 2. Feature importance
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio']
xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
xgb.fit(synth[feature_cols], synth['exact_rank'])
imp = pd.DataFrame({'feature': feature_cols, 'importance': xgb.feature_importances_})
imp = imp.sort_values('importance', ascending=False)
imp.to_csv("feature_importance.csv", index=False)
print("\n✅ feature_importance.csv saved")
print(imp)


# 3. Predictions
pred_df = pd.DataFrame({
    'true_rank': synth['exact_rank'],
    'flux_gr': synth['flux_gr'],
    'pm_mag_proxy': synth['pm_mag_proxy'],
    'mag_ratio': synth['mag_ratio']
})
pred_df.to_csv("predictions_final.csv", index=False)
print("\n✅ predictions_final.csv saved")


print("\n🎉 All three files are ready.")
