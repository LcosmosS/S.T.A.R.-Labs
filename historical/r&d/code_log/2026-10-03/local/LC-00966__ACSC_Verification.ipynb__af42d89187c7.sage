# acsc_final_summary.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=== ACSC Final Summary Analysis ===\n")

# Load both files
cremona = pd.read_csv("acsc_validation_cremona.csv")
lmfdb = pd.read_csv("acsc_validation_lmfdb.csv")

print(f"Cremona: {len(cremona):,} curves")
print(f"LMFDB:   {len(lmfdb):,} curves\n")

# Combine for overall statistics
df = pd.concat([cremona, lmfdb], ignore_index=True)

# Clean numeric columns
for col in ["sage_rank", "pari_2_selmer_rank", "pari_analytic_rank", "log_abs_delta"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 1. Rank Distribution
print("Rank Distribution:")
print(df["sage_rank"].value_counts().sort_index())

# 2. Complexity-14 Pass Rate (your exact logic)
pass_rate = df["passes_complexity_14"].mean() * 100
print(f"\nComplexity-14 Pass Rate: {pass_rate:.2f}% "
      f"({df['passes_complexity_14'].sum():,} curves passed)")

# 3. Arithmetic Scarcity (log|Δ| vs Rank)
scarcity = df.groupby("sage_rank")["log_abs_delta"].mean().round(3)
print("\nArithmetic Scarcity (average log|Δ| by rank):")
print(scarcity)

# 4. Rank Consistency (Sage = PARI 2-Selmer = Analytic)
consistent = (
    (df["sage_rank"] == df["pari_2_selmer_rank"]) & 
    (df["sage_rank"] == df["pari_analytic_rank"])
).mean() * 100
print(f"\nSage/PARI Rank Consistency: {consistent:.1f}%")

# 5. Save enriched combined file
df.to_csv("acsc_final_combined.csv", index=False)
print("\nSaved full combined dataset → acsc_final_combined.csv")

# Quick plot: Rank vs log|Δ|
plt.figure(figsize=(10, 6))
for r in sorted(df["sage_rank"].dropna().unique()):
    subset = df[df["sage_rank"] == r]
    plt.scatter(subset["sage_rank"], subset["log_abs_delta"], alpha=0.6, label=f"Rank {r}")
plt.xlabel("Algebraic Rank")
plt.ylabel("log₁₀|Δ|")
plt.title("ACSC Arithmetic Scarcity: Rank vs log|Δ|")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("acsc_scarcity_plot.png")
plt.show()

print("\n ACSC analysis complete!")
print("   → acsc_final_combined.csv (all data)")
print("   → acsc_scarcity_plot.png (visual)")
print("Ready for thesis tables/figures.")