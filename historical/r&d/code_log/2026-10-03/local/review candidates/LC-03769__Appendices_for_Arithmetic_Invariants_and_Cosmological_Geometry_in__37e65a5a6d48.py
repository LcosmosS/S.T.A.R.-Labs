        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        rank = E.selmer_rank(3)
        torsion = E.torsion_subgroup().order()
        j_inv = E.j_invariant()
        disc = E.discriminant()
        print(f"compute_3selmer_rank: logmass={logmass:.3f},
delta_scaled={delta_scaled}, conductor_scaled={conductor_scaled},
entropy={entropy:.3e}, betti_1={betti_1}, entropy_gradient={entropy_gradient:.3e},
rank={rank}")
        if rank > SELMER_BOUND:
            print(f"compute_3selmer_rank: High rank={rank} >
SELMER_BOUND={SELMER_BOUND}")
            return rank, 'high_rank', torsion, j_inv, disc
        return rank, 'success', torsion, j_inv, disc
    except Exception as e:
        print(f"compute_3selmer_rank: Error - {str(e)}")
        return np.nan, f'error_{str(e)}', np.nan, np.nan, np.nan

# --- 12. Mapping Functions ---
def compute_mappings(row, pari):
    log_function("compute_mappings")
    reg_cosmo = row['logmass'] * REG_COSMO * KAPPA if np.isfinite(row['logmass']) else
np.nan
    t_cosmo = row['petrorad_r'] * T_COSMO * KAPPA if np.isfinite(row['petrorad_r'])
else np.nan
    delta = row['logmass'] * 1e6 if np.isfinite(row['logmass']) else np.nan
    omega = row['petrorad_r'] * 1e3 if np.isfinite(row['petrorad_r']) else np.nan
    conductor = delta**2 if np.isfinite(delta) else np.nan
    j_invariant = row['metallicity'] * 1e4 if np.isfinite(row['metallicity']) else
np.nan
    tr_p1 = float(factor(int(delta))[0][0]) if np.isfinite(delta) and delta > 0 else
np.nan
