import requests
import pandas as pd
import time
import math
from sage.all import EllipticCurve, QQ, prod

# ==============================================================================
# SECTION 1: CORE PARAMETERS
# ==============================================================================

DATA_DRIVEN_KAPPA = 31.5926
KAPPA = 1000.0
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 5.4e7

def get_expanded_cluster_data():
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
# SECTION 2: CURVE DERIVATION + SAGE (with debugging)
# ==============================================================================

def derive_curve_parameters(cluster_name, r, rho):
    if cluster_name == 'Virgo':
        return -1706, 6320
    else:
        return round(-DATA_DRIVEN_KAPPA * r), rho


def create_minimal_model(a, b):
    print(f"    Creating Sage model for a={a}, b={b}...")
    try:
        E = EllipticCurve([0, a, 0, b, 0], minimal_twist=True)
        E_min = E.minimal_model()
        ainvs = E_min.ainvs()
        print(f"    ✓ Minimal model created: {ainvs}")
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
        print(f"    ✗ Sage Error: {str(e)}")
        return {'status': f'Sage Error: {str(e)}'}


def query_lmfdb_api(a, b, cluster_name):
    print(f"  > Processing '{cluster_name}' (a={a}, b={b})...")
    sage_info = create_minimal_model(a, b)
    if sage_info['status'] != 'Success':
        return {**sage_info, 'lmfdb_label': None, 'found': False}

    ainvs = sage_info['minimal_ainvs']
    a4 = ainvs[3]
    a6 = ainvs[4]

    api_url = "https://www.lmfdb.org/api/ec_curvedata/"
    params = {
        'a4': int(a4),
        'a6': int(a6),
        '_format': 'json',
        'limit': 3
    }

    try:
        response = requests.get(api_url, params=params, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        data = response.json()
        if data.get('data') and len(data['data']) > 0:
            curve = data['data'][0]
            return {'found': True, 'lmfdb_label': curve.get('label'), **sage_info}
        else:
            return {**sage_info, 'found': False, 'lmfdb_label': None, 'status': 'Not Found in LMFDB'}
    except Exception as e:
        return {**sage_info, 'found': False, 'lmfdb_label': None, 'status': f'API Error: {str(e)}'}


# ==============================================================================
# SECTION 3: FULL ACSC + ENTROPY COHOMOLOGY PROJECTION
# ==============================================================================

def acsc_entropy_projection_hook(sage_info, cluster_r, cluster_rho):
    if sage_info.get('status') != 'Success':
        return {
            'projected_omega': None, 'h_eff_factor': None, 'comoving_volume': None,
            'scaled_regulator': None, 'entropy_proxy': None, 'cohomology_class': None,
            'cosmo_scale': None, 'note': sage_info.get('status')
        }

    rank = sage_info['rank']
    omega = sage_info['real_period']
    reg = sage_info['regulator']
    disc = abs(sage_info['discriminant'])

    cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
    scaled_period = omega * SQRT_KAPPA * cosmo_scale

    rank_divisors = {3: (1.5e13, 20), 2: (1.5e14, 7), 1: (8e13, 5)}
    volume_divisor, regulator_factor = rank_divisors.get(rank, (1e14, 20))

    comoving_volume = (omega * reg * (cosmo_scale ** 3)) / volume_divisor
    scaled_reg = reg * SQRT_KAPPA * regulator_factor

    h_eff_factor = (scaled_period / VIRGO_DISTANCE) * (1 + 0.01 * math.log10(cluster_r + 1))

    entropy_proxy = math.log(disc + 1e-8)
    cohomology_class = entropy_proxy * (rank + 1) / (cluster_r ** 0.5 + 1)

    return {
        'projected_omega': float(scaled_period),
        'h_eff_factor': float(h_eff_factor),
        'comoving_volume': float(comoving_volume),
        'scaled_regulator': float(scaled_reg),
        'entropy_proxy': float(entropy_proxy),
        'cohomology_class': float(cohomology_class),
        'cosmo_scale': float(cosmo_scale),
        'note': 'Full ACSC Φ + ECC projection'
    }


# ==============================================================================
# SECTION 4: MAIN EXECUTION + SAFE FORMATTING
# ==============================================================================

if __name__ == "__main__":
    print("="*90)
    print("   UCF LMFDB Expansion Tool — Full ACSC + Entropy Cohomology Projection")
    print("="*90)
    
    cluster_data = get_expanded_cluster_data()
    results_list = []
    
    for name, data in cluster_data.items():
        a, b = derive_curve_parameters(name, data['r'], data['rho'])
        time.sleep(int(1.5))
        
        lmfdb_result = query_lmfdb_api(a, b, name)
        projection = acsc_entropy_projection_hook(lmfdb_result, data['r'], data['rho'])
        
        # Safe formatting helper
        def safe_fmt(val, fmt):
            if val is None:
                return 'N/A'
            try:
                return f"{val:{fmt}}"
            except:
                return str(val)
        
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
            'LMFDB Found': 'Yes' if lmfdb_result.get('found', False) else 'No',
            'Projected Omega (ly)': safe_fmt(projection.get('projected_omega'), '.1f'),
            'H_eff Factor': safe_fmt(projection.get('h_eff_factor'), '.4f'),
            'Comoving Vol (Mly³)': safe_fmt(projection.get('comoving_volume'), '.0f'),
            'Entropy Proxy': safe_fmt(projection.get('entropy_proxy'), '.2f'),
            'Cohomology Class': safe_fmt(projection.get('cohomology_class'), '.4f'),
            'Status': lmfdb_result.get('status', 'Success')
        })

    results_df = pd.DataFrame(results_list)
    print("\n" + "="*90)
    print("                 FINAL RESULTS WITH FULL PROJECTION")
    print("="*90)
    print(results_df.to_string(index=False))
    
    results_df.to_csv('ucf_lmfdb_full_acsc_projection.csv', index=False)
    print("\n Results saved to 'ucf_lmfdb_full_acsc_projection.csv'")
    print("Execution complete. Check debug output above for any Sage/LMFDB issues.")