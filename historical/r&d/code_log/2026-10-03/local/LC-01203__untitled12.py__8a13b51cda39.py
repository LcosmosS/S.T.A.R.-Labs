import requests
import pandas as pd
import time
import json
from sage.all import EllipticCurve, QQ, prod
import math
import numpy as np

# ==============================================================================
# SECTION 1: CORE UCF PARAMETERS AND EXPANDED CLUSTER DATA
# ==============================================================================

DATA_DRIVEN_KAPPA = 31.5926
KAPPA = 1000.0                      # From notebook core scaling
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 5.4e7              # 54 million light-years (anchor)

def get_expanded_cluster_data():
    """Provides physical parameters for major cosmological structures."""
    return {
        'Virgo':      {'r': 54,  'rho': 6320},
        'Coma':       {'r': 321, 'rho': 9980},
        'Perseus':    {'r': 236, 'rho': 11500},
        'Centaurus':  {'r': 170, 'rho': 7500},
        'Fornax':     {'r': 62,  'rho': 3200},
        'Hercules':   {'r': 500, 'rho': 8500},
        'Shapley':    {'r': 650, 'rho': 18000},
        'Horologium': {'r': 700, 'rho': 12000},
    }


# ==============================================================================
# SECTION 2: CURVE DERIVATION, SAGE INTEGRATION, AND LMFDB API QUERY
# ==============================================================================

def derive_curve_parameters(cluster_name, r, rho):
    """Applies UCF scaling law. Virgo is the foundational case."""
    if cluster_name == 'Virgo':
        a = -1706
        b = 6320
    else:
        a = round(-DATA_DRIVEN_KAPPA * r)
        b = rho
    return a, b


def create_minimal_model(a, b):
    """Create Sage EllipticCurve and compute minimal model + invariants."""
    try:
        E = EllipticCurve([0, a, 0, b, 0])
        E_min = E.minimal_model()
        ainvs = E_min.ainvs()
        return {
            'E': E_min,
            'minimal_ainvs': ainvs,
            'conductor': int(E_min.conductor()),
            'rank': E_min.rank(),
            'discriminant': int(E_min.discriminant()),
            'real_period': float(E_min.period_lattice().real_period(prec=50)),
            'regulator': float(E_min.regulator()) if E_min.rank() > 0 else 1.0,
            'tamagawa': float(prod(E_min.tamagawa_numbers())),
            'torsion_order': E_min.torsion_subgroup().order(),
            'status': 'Success'
        }
    except Exception as e:
        return {'status': f'Sage Error: {str(e)}'}


def query_lmfdb_api(a, b, cluster_name):
    """Query LMFDB API using minimal model coefficients."""
    print(f"  > Processing '{cluster_name}' (a={a}, b={b})...")

    sage_info = create_minimal_model(a, b)
    if sage_info['status'] != 'Success':
        return {**sage_info, 'lmfdb_label': None, 'found': False}

    ainvs = sage_info['minimal_ainvs']
    api_url = "https://www.lmfdb.org/api/ec_curvedata/"
    params = {
        'a4': ainvs[3],
        'a6': ainvs[5],
        '_format': 'json',
        'limit': 3
    }

    try:
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get('data') and len(data['data']) > 0:
            curve = data['data'][0]
            return {
                'found': True,
                'lmfdb_label': curve.get('label'),
                **sage_info
            }
        else:
            return {**sage_info, 'found': False, 'lmfdb_label': None, 'status': 'Not Found'}
    except Exception as e:
        return {**sage_info, 'found': False, 'lmfdb_label': None, 'status': f'API Error: {str(e)}'}


# ==============================================================================
# SECTION 3: FULL ACSC + ENTROPY COHOMOLOGY PROJECTION LOGIC (from STAR.ipynb)
# ==============================================================================

def acsc_entropy_projection_hook(sage_info, cluster_r, cluster_rho):
    """
    Full projection Φ from ACSC + Entropy Cohomology logic adapted from STAR.ipynb.
    Maps elliptic invariants → cosmological quantities with scale-dependent effects.
    """
    if sage_info.get('status') != 'Success':
        return {'projected_omega': None, 'h_eff_factor': None, 'comoving_volume': None,
                'entropy_cohomology_class': None, 'note': 'Sage computation failed'}

    E = sage_info['E']
    rank = sage_info['rank']
    omega = sage_info['real_period']
    reg = sage_info['regulator']
    tamagawa = sage_info['tamagawa']
    tors = sage_info['torsion_order']

    # Dynamic COSMO_SCALE (Virgo anchor + √κ)
    cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
    scaled_period = omega * SQRT_KAPPA * cosmo_scale

    # Rank-specific divisors (directly from notebook)
    if rank == 3:
        volume_divisor = 1.5e13
        regulator_factor = 20
    elif rank == 2:
        volume_divisor = 1.5e14
        regulator_factor = 7
    elif rank == 1:
        volume_divisor = 8e13
        regulator_factor = 5
    else:
        volume_divisor = 1e14
        regulator_factor = 20

    # Comoving volume & scaled regulator
    comoving_volume = (omega * reg * (cosmo_scale ** 3)) / volume_divisor
    scaled_reg = reg * SQRT_KAPPA * regulator_factor

    # ACSC Projection: effective Hubble-like factor (scale-dependent)
    # ⟨Ω_E⟩_z proxy weighted by cluster distance
    h_eff_factor = (scaled_period / VIRGO_DISTANCE) * (1 + 0.01 * math.log10(cluster_r + 1))

    # Entropy Cohomology Component (simplified differential form / class proxy)
    # Entropy field ℳ(x) ~ log(|Δ|) + cohomology weighting
    entropy_proxy = math.log(abs(sage_info['discriminant']) + 1e-8)
    cohomology_class = entropy_proxy * (rank + 1) / (cluster_r ** 0.5)   # rough topological weighting

    return {
        'projected_omega': float(scaled_period),
        'h_eff_factor': float(h_eff_factor),
        'comoving_volume': float(comoving_volume),
        'scaled_regulator': float(scaled_reg),
        'entropy_proxy': float(entropy_proxy),
        'cohomology_class': float(cohomology_class),
        'cosmo_scale': float(cosmo_scale),
        'note': 'ACSC Φ + ECC entropy field projection (extend with full TDA/symbolic regression)'
    }


# ==============================================================================
# SECTION 4: MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("="*90)
    print("   UCF LMFDB Expansion Tool — Full ACSC + Entropy Cohomology Projection")
    print("="*90)
    
    cluster_data = get_expanded_cluster_data()
    results_list = []
    
    for name, data in cluster_data.items():
        a, b = derive_curve_parameters(name, data['r'], data['rho'])
        time.sleep(1.5)
        
        lmfdb_result = query_lmfdb_api(a, b, name)
        projection = acsc_entropy_projection_hook(lmfdb_result, data['r'], data['rho'])
        
        results_list.append({
            'Cluster': name,
            'r (Mly)': data['r'],
            'rho': data['rho'],
            'Derived a': a,
            'Derived b': b,
            'Minimal ainv': str(lmfdb_result.get('minimal_ainvs', 'N/A')),
            'Conductor': lmfdb_result.get('conductor'),
            'Rank': lmfdb_result.get('rank'),
            'LMFDB Label': lmfdb_result.get('lmfdb_label', '---'),
            'LMFDB Found': 'Yes' if lmfdb_result.get('found') else 'No',
            'Projected Omega (ly)': f"{projection['projected_omega']:.1f}" if projection['projected_omega'] else 'N/A',
            'H_eff Factor': f"{projection['h_eff_factor']:.4f}" if projection['h_eff_factor'] else 'N/A',
            'Comoving Vol (Mly³)': f"{projection['comoving_volume']:.0f}" if projection['comoving_volume'] else 'N/A',
            'Entropy Proxy': f"{projection['entropy_proxy']:.2f}",
            'Cohomology Class': f"{projection['cohomology_class']:.4f}",
            'Status': lmfdb_result.get('status', 'Success')
        })

    results_df = pd.DataFrame(results_list)
    print("\n" + "="*90)
    print("                 FINAL RESULTS WITH FULL PROJECTION")
    print("="*90)
    print(results_df.to_string(index=False))
    
    results_df.to_csv('ucf_lmfdb_full_acsc_projection.csv', index=False)
    print("\nFull results saved to 'ucf_lmfdb_full_acsc_projection.csv'")
    print("Ready for import into STAR.ipynb or symbolic regression / TDA pipeline.")
    print("Execution complete.")