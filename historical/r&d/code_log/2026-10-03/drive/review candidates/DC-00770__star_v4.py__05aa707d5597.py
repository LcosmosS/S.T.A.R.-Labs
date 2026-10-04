    mers = [2**p - 1 for p in [2,3,5,7,11,13,17,19,23,29][:n]]


    MOD = 2**53
    for i in range(2, n):
        fib.append((fib[i-1] + fib[i-2]) % MOD)
        luc.append((luc[i-1] + luc[i-2]) % MOD)
        pell.append((2*pell[i-1] + pell[i-2]) % MOD)
        cat.append(((2*(2*i-1)//(i+1)) * cat[i-1]) % MOD)


    return {
        'Fibonacci': fib, 'Lucas': luc, 'Pell': pell, 'Catalan': cat,
        'PrimePowers': ppow, 'Triangular': tri, 'Square': sq, 'Mersenne': mers
    }


# ----------------------------------------------------------------------
# 3. Sequence similarity (DTW + correlation)
# ----------------------------------------------------------------------
def sequence_similarity(row, sequences):
    a = row['a']; b = row['b']
    results = {}
    for name, seq in sequences.items():
        dist, _ = fastdtw([a, b], seq[:2])
        corr = np.corrcoef([a, b], seq[:2])[0,1] if len(seq) >= 2 else 0
        results[f'{name}_dtw'] = dist
        results[f'{name}_corr'] = corr
    return results


# ----------------------------------------------------------------------
# 4. LMFDB lookup
# ----------------------------------------------------------------------
def lmfdb_lookup(a, b):
    try:
        a = int(a); b = int(b)
        E = EllipticCurve(QQ, [a, b])
        cond = E.conductor()
        url = f"https://www.lmfdb.org/EllipticCurve/Q/{cond}"
        r = requests.head(url, timeout=5)
        return r.status_code == 200
    except:
        return False


# ----------------------------------------------------------------------
# 5. Sha estimation
# ----------------------------------------------------------------------
def estimate_sha(E):
    try:
        sha = E.sha()
        an = sha.an()
        return an if an != 'unknown' else np.nan
    except:
        return np.nan


# ----------------------------------------------------------------------
# 6. Hierarchy of Evidence – algebraic first, 2-descent, 3-isogeny, analytic
# ----------------------------------------------------------------------
def hierarchy_of_evidence(a, b):
    try:
        a = int(a); b = int(b)
        E = EllipticCurve(QQ, [a, b])
        print(E)
     
        # Calculate the discriminant of the curve E
        delta = E.discriminant()
        print(delta)


        # Compute the torsion subgroup of E
        torsion_subgroup = E.torsion_subgroup()
        print(torsion_subgroup)


        # Compute the algebraic rank of E
        try:
            alg = E.rank()
            print(alg)
        except:
            alg = E.rank_bounds()[0]  # lower bound


        # Use analytic rank as fallback
        anal = L.order_of_vanishing()
        raw['rank'] = raw['alg_rank'].fillna(anal).fillna(0)
        print(anal)


        # Find the generator(s) of the free part of the Mordell-Weil group
        generators = E.gens()
        print(generators)


        # Compute the L-series associated with E
        L = E.lseries()
        print(L)


        # Compute the value of L(E,s) at s=1
        L_value_at_1 = L(1)
        print(L_value_at_1)


        # Compute the value of the first derivative L'(E,s) at s=1
        L_derivative_at_1 = L.dokchitser().derivative(1, 1)
        print(L_derivative_at_1)


        # Re-compute L'(E,1) with higher precision
        L_derivative_high_precision = E.lseries().dokchitser(prec=400).derivative(1, 1)
        print(L_derivative_high_precision)


        # Compute the real period with higher precision
        omega_high_precision = E.period_lattice().real_period(prec=400)
        print(omega_high_precision)


        # Compute the regulator with higher precision
        P = E.gens()[0]
        regulator_high_precision = P.height(precision=400)
        print(regulator_high_precision)


        # Compute the product of the Tamagawa numbers
        tamagawa_product = prod(E.tamagawa_numbers())
        print(tamagawa_product)


        S = E.selmer_rank()
        print(S)


        E.two_descent(second_limit=20, verbose=False)
        sel2 = E.selmer_rank()
        try:
            isog3 = E.isogeny_class()
            sel3 = sum(1 for _ in isog3.curves() if _.rank() == alg)
            print(isog3)
            print(sel3)
        except:
            sel3 = np.nan
        L = E.lseries()
        anal = L.order_of_vanishing()
        tamagawa_flag = (alg != anal)
        return alg, sel2, sel3, anal, (alg == sel2 == anal), tamagawa_flag
        print(tamagawa_flag)
    except Exception:
        return np.nan, np.nan, np.nan, np.nan, False, True


# ----------------------------------------------------------------------
# 7. Alternative Mappings – safe log
# ----------------------------------------------------------------------
def alternative_mappings(row):
    try:
        a = int(row['a']); b = int(row['b'])
        E = EllipticCurve(QQ, [a, b])
        disc = abs(E.discriminant())
        j = E.j_invariant()
        cond = E.conductor()
        j_abs = abs(j) + 1e-12
        ptd = (np.log(abs(disc)+1e-12), 0.0, 0.0)
        mcj = (np.log(cond+1e-12), np.log(j_abs), 0.0)
        coeffs = [row.get(f'COEFF{i}',0) for i in range(10)]
        return {
            **{f'ptd_{k}': v for k,v in zip(['phi','theta','z'], ptd)},
            **{f'mcj_{k}': v for k,v in zip(['phi','theta','z'], mcj)},
            'ft_mean': np.mean(coeffs), 'ft_var': np.var(coeffs),
            'iwt_isog': 1, 'iwt_deg': 1, 'iwt_tors': row.get('torsion',1)
        }
    except Exception:
        return {f'{m}_{k}':0 for m in ['ptd','mcj'] for k in ['phi','theta','z']}


# ----------------------------------------------------------------------
# 8. Invariant Scaling Laws
# ----------------------------------------------------------------------
def invariant_scaling(df):
    V0 = 8.52e6
    df['psi'] = df['rank'] * (df['rank'] + 1) / 2
    df['V_comove'] = V0 * (df['Regulator']**(1/(df['rank']+1e-12)) *
                           np.exp(df['psi'])) / (df['T'] *
                           np.log(df['Omega'] / (2*np.pi) + 1e-12))
    df['rho_scale'] = (df['Omega'] * df['T']**2 * np.exp(df['psi']) /
                       df['Regulator'])**(df['rank']+1e-12) * np.exp(-1/(df['Omega']+1e-12))
    return df


# ----------------------------------------------------------------------
# 9. Inverse design of b
# ----------------------------------------------------------------------
def inverse_b_design(df):
    df['b_target'] = df['b']
    return df


# ----------------------------------------------------------------------
# 10. Physics - Tully-Fisher, Planck, Hubble-time, Wasserstein, StatMech, Anthropic
# ----------------------------------------------------------------------
def physics_extensions(df):
    v_rot = df.get('vel_disp_Ha_cen', 100)
    df['M_TF'] = 4 * np.log10(v_rot + 1)
    df['t_H'] = 977.8 / 70
    lp = 1.616255e-35
    Re_kpc = df.get('Re_kpc', 1.0)
    Re_m = Re_kpc * 3.08568e19
    df['lp_ratio'] = Re_m / lp
    if len(df) > 1:
        d1 = df['z'].values[:len(df)//2]
        d2 = df['z'].values[len(df)//2:]
        df['W2_example'] = wasserstein_distance(d1, d2)
    else:
        df['W2_example'] = 0.0
    k = 1.38e-23; T = 2.7
    df['S_mech'] = np.log(df['V_comove'] / (k*T) + 1)
    df['Delta_H'] = np.random.normal(0, 1e-5, len(df))
    df['anthropic_ok'] = (abs(df['Delta_H']) < 1e-5)
    return df


# ----------------------------------------------------------------------
# 11. Binning
# ----------------------------------------------------------------------
def bin_generator_type(row):
    is_recursive = 1 if pd.notna(row.get('OType')) and 'GALAXY' in str(row['OType']).upper() else 0
    a = int(abs(row.get('a',1)))
    b = int(abs(row.get('b',1)))
    is_rational = 1 if b != 0 and gcd(a,b) > 1 else 0
    coeffs = [row.get(f'COEFF{i}',0) for i in range(10) if pd.notna(row.get(f'COEFF{i}',np.nan))]
    if len(coeffs) < 3:
        fractal = vortex = 0; symmetrical = 1
    else:
        f = np.abs(fft(coeffs))
        power = np.log(np.var(f)+1e-12)
        phase = np.std(np.angle(fft(coeffs)))
        var = np.var(coeffs)
        fractal = 1 if power > np.mean(power) else 0
        vortex   = 1 if phase > np.pi/4 else 0
        symmetrical = 1 if var < np.mean(var) else 0
    shape = ['fractal','vortex','symmetrical'][max(range(3), key=[fractal,vortex,symmetrical].__getitem__)]
    return f"{['simple','recursive'][is_recursive]}_{['irrational','rational'][is_rational]}_{shape}"


# ----------------------------------------------------------------------
# 12. Feature engineering – NOW CREATES logmass
# ----------------------------------------------------------------------
def engineer_features(df):
    # --- SAFE: use .get() with fallbacks ---
    df['logmass'] = np.log10(df.get('Fg',1) + df.get('Fr',1) + df.get('Fz',1) + 1e-6)
    df['z'] = df.get('z', 0.05)
    df['petrorad_r'] = df.get('Re_kpc', 1.0)
    df['sfr'] = df.get('sfr_tot_p50', 1.0)
    df['metallicity'] = df.get('ZH_LW_Re_fit', 0.02)
    df['Smooth'] = df.get('Smooth', np.random.uniform(0,1,len(df)))
    df['Featured'] = 1 - df['Smooth']


    # --- SAFE: avoid division by zero ---
    df['L_cosmo'] = np.log10(df['logmass']) * (1+df['z'])**0.7 * (df['Smooth'] - df['Featured'])
    df['RCC'] = np.log1p(df['sfr']) / (np.log1p(df['petrorad_r']) + 1e-12)
    df['TPF'] = np.sqrt(np.log1p(df['metallicity']) / (df['Smooth'] + 1))
    df['VDI'] = df['logmass'] * df['sfr'] / (df['petrorad_r'] + 1e-6)
    return df


# ----------------------------------------------------------------------
# 13. Unity Export
# ----------------------------------------------------------------------
def export_to_unity(df, out_dir):
    unity_csv = os.path.join(out_dir, "star_v4_unity.csv")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_unity = df[numeric_cols].copy()
    df_unity.to_csv(unity_csv, index=False)
    
    manifest = {
        "csv_file": "star_v4_unity.csv",
        "columns": {col: str(df_unity[col].dtype) for col in df_unity.columns},
        "description": "S.T.A.R. v4 – Elliptic curves from DESI spectra",
        "version": "v4"
    }
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Unity-ready CSV: {unity_csv}")
    print(f"Manifest: {os.path.join(out_dir, 'manifest.json')}")
    
# ----------------------------------------------------------------------
# 14. ML per bin
# ----------------------------------------------------------------------
def run_per_bin(df, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    feature_cols = ['z','logmass','petrorad_r','sfr','metallicity','Smooth','Featured',
                    'L_cosmo','RCC','TPF','VDI','lp_ratio','M_TF','t_H','W2_example'] + \
                   [f'{m}_{k}' for m in ['ptd','mcj'] for k in ['phi','theta','z']] + \
                   [f'{s}_dtw' for s in generate_sequences(10).keys()] + \
