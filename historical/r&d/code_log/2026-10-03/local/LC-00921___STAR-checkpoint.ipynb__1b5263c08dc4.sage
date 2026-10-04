# Test cosmic recurrence on 10 real clusters

from sage.all import *
import pandas as pd

# ———————— COSMIC RECURRENCE (EXACT FOR COMA) ————————
def cosmic_recurrence(r, rho):
    num_x = round(r * (10987 / 321))        # 34.231...
    offset = 5874                          # = 774964 - 10987*70
    num_y = num_x * 70 + offset
    return num_x, num_y

def predict_generator(r, rho):
    num_x, num_y = cosmic_recurrence(r, rho)
    d_x = 3**4  # 81
    d_y = 3**6  # 729
    return (QQ(num_x)/d_x, QQ(num_y)/d_y, 1)

def derive_curve(r, rho, kappa=31.59259259259259):
    a = -round(kappa * r)
    b = rho
    return a, b

# ———————— CLUSTER CORPUS ————————
clusters = [
    ("Virgo",      54,  6200),
    ("Coma",      321, 9980),
    ("Fornax",     62,  3200),
    ("Perseus",   240,  8500),
    ("Centaurus", 170,  7200),
    ("Hydra",     190,  7800),
    ("Norma",     220,  8100),
    ("Abell 754", 280,  9200),
    ("Abell 2199",410, 11000),
    ("Abell 85",  370, 10500),
]

results = []

for name, r, rho in clusters:
    # Predict
    P_pred = predict_generator(r, rho)
    a, b = derive_curve(r, rho)
    
    # Compute actual curve
    try:
        E = EllipticCurve(QQ, [a, b])
        rank = E.rank()
        gens = E.gens()
        P_actual = gens[0] if rank > 0 else None
    except:
        rank = "Error"
        P_actual = None
    
    # Match
    match = (P_actual is not None and P_pred == P_actual)
    
    results.append({
        "Cluster": name,
        "r": r,
        "ρ": rho,
        "a": a,
        "b": b,
        "Predicted P": str(P_pred),
        "Actual Rank": rank,
        "Actual P": str(P_actual) if P_actual else "—",
        "Match": "YES" if match else "NO"
    })

# ———————— SUMMARY TABLE ————————
df = pd.DataFrame(results)
print(df.to_string(index=False))
