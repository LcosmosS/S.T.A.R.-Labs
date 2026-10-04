import os
import pandas as pd
import time
import math
from sage.all import QQ, EllipticCurve, prod
from sage.schemes.elliptic_curves.ec_database import elliptic_curves
from concurrent.futures import ProcessPoolExecutor, as_completed


# ==============================================================================
# SECTION 1: LOCAL DATABASE SETUP
# ==============================================================================


os.environ["CREMONA_DATABASE_PATH"] = os.path.expanduser("~/ecdata")
os.environ["LMFDB_DATABASE_PATH"] = os.path.expanduser("~/lmfdb")


print(" Using local ecdata at:", os.environ.get("CREMONA_DATABASE_PATH"))
print("Using local lmfdb data at:", os.environ.get("LMFDB_DATABASE_PATH"))


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
# SECTION 2: WORKER FUNCTION FOR PARALLEL PROCESSING
# ==============================================================================


def process_cluster(args):
    """Worker function for parallel execution (must be top-level)."""
    name, data = args
    a, b = derive_curve_parameters(name, data['r'], data['rho'])
    
    print(f"  > Processing '{name}' (a={a}, b={b})...")
    sage_info = create_minimal_model(a, b)
    projection = acsc_entropy_projection_hook(sage_info, data['r'], data['rho'])
    
    return {
        'Cluster': name,
        'r (Mly)': data['r'],
        'rho': data['rho'],
        'Derived a': a,
        'Derived b': b,
        'Minimal ainv': str(sage_info.get('minimal_ainvs', 'N/A')),
        'Conductor': sage_info.get('conductor'),
        'Rank': sage_info.get('rank'),
        'Local Label': sage_info.get('local_label', '---'),
        **projection,
        'Status': sage_info.get('status', 'Error')
    }




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
        print(f"     Minimal model: {ainvs}")


        # === HIGH two_descent + ROBUST RANK ===
        try:
            print(f"    Computing rank with high two_descent limit...")
            E_min.two_descent(second_limit=10000)          
            rank = E_min.rank(only_use_mwrank=False)
        except Exception:
            try:
                rank = E_min.rank_bound()
            except:
                rank = 0


        # Local DB label lookup
        label = "Unknown"
        try:
            db = elliptic_curves
            cond = E_min.conductor()
            for curve in db.iter(curve_class=cond):
                if tuple(curve.ainvs()) == tuple(ainvs):
                    label = getattr(curve, 'label', lambda: str(curve))()
                    break
        except:
            pass


        return {
            'E': E_min,
            'minimal_ainvs': ainvs,
            'conductor': int(E_min.conductor()),
            'rank': rank,
            'discriminant': int(E_min.discriminant()),
            'real_period': float(E_min.period_lattice().real_period(prec=50)),
            'regulator': float(E_min.regulator()) if rank > 0 else 1.0,
            'tamagawa': float(prod(E_min.tamagawa_numbers())),
            'torsion_order': E_min.torsion_subgroup().order(),
            'local_label': label,
            'status': 'Success'
        }
    except Exception as e:
        print(f"    Sage Error: {str(e)}")
        return {'status': f'Sage Error: {str(e)}'}
