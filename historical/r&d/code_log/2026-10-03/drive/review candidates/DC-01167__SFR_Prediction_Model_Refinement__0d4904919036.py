import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import shap
import matplotlib.pyplot as plt
import seaborn as sns


# Load all datasets
df_main = pd.read_csv("filtered_dataset.csv")
df_class = pd.read_csv("GalaxiesClassified.csv")
df_mass = pd.read_csv("Stellar_Mass2_Table.csv")
df_hi = pd.read_csv("mangaHIall.csv")


# Merge on 'mangaid'
df = df_main.merge(df_class, on="mangaid", how="left")
df = df.merge(df_mass, on="mangaid", how="left")
df = df.merge(df_hi, on="mangaid", how="left")


# Drop rows with missing SFR or key variables
df.dropna(subset=["SFR", "log_Mass_gas", "metallicity", "dust_attenuation"], inplace=True)


# Optional: Drop rows with any NaNs (if you prefer)
df.dropna(inplace=True)


# Define features and target
features = [
    "log_Mass_gas",
    "metallicity",
    "dust_attenuation",
    "log_Mass_stellar",
    "log_Mass_bulge",
    "log_Mass_disk",
    "logHI"
]


X = df[features]
y = df["SFR"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Gradient Boosting Regressor
gbr = GradientBoostingRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
gbr.fit(X_train, y_train)
y_pred_gbr = gbr.predict(X_test)


# Random Forest Regressor
rfr = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rfr.fit(X_train, y_train)
y_pred_rfr = rfr.predict(X_test)


# Evaluation
def evaluate(model_name, y_true, y_pred):
    print(f"\n--- {model_name} ---")
    print("R² Score:", r2_score(y_true, y_pred))
    print("RMSE:", mean_squared_error(y_true, y_pred, squared=False))


evaluate("Gradient Boosting", y_test, y_pred_gbr)
evaluate("Random Forest", y_test, y_pred_rfr)


# SHAP for Gradient Boosting
explainer = shap.Explainer(gbr, X)
shap_values = explainer(X)


shap.summary_plot(shap_values, X)


# Optional: Save plots if you're in non-interactive mode
# plt.savefig("shap_summary.png")
# plt.close()
