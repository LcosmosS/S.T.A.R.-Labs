    Reg = E.regulator() if rank > 0 else QQ(1)
    Omega = E.period_lattice().real_period()
    T = E.torsion_order()
    
    # Inverse volume scaling (from your generalized f(R, Ω, T))
    V_comove = float((Reg * Omega * T**2) ** (1/rank) * 1e6) if rank > 0 else 1e6
    
    # Inverse density scaling
    rho_scale = float((Reg / (Omega * T**2)) ** (1/rank) * 1e3)
    
    # Betti / topological class (tied to rank as in ACSC/ECC)
    betti_1 = rank * 2 + random.randint(-1, 1)   # simple proxy
    
    return {
        'exact_rank': rank,
        'regulator': float(Reg),
        'real_period': float(Omega),
        'torsion': T,
        'V_comove': V_comove,
        'rho_scale': rho_scale,
        'betti_1': betti_1,
        'conductor': int(E.conductor()),
        'discriminant': float(E.discriminant())
    }


results = []


# Sample curves by rank (Cremona database is built into Sage)
for r in [1, 2, 3]:   # your cornerstone ranks from the thesis
    print(f"\nGenerating synthetic cosmos for rank {r} ...")
    curve_list = elliptic_curves.rank(n=NUM_CURVES_PER_RANK, rank=r, conductor_max=MAX_CONDUCTOR)
    
    for i, E in enumerate(curve_list):
        if i % 20 == 0:
            print(f"   Curve {i+1}/{NUM_CURVES_PER_RANK} | Conductor {E.conductor()}")
        
        try:
            cosmo = generate_synthetic_cosmology(E, r)
            
            # Generate simple 3D galaxy positions (synthetic cluster)
            n_galaxies = 50 + r * 20
            ra = np.random.normal(0, cosmo['rho_scale'], n_galaxies)
            dec = np.random.normal(0, cosmo['rho_scale'], n_galaxies)
            z = np.random.normal(cosmo['V_comove']/3e5, 0.01, n_galaxies)  # rough velocity proxy
            
            for g in range(n_galaxies):
                results.append({
                    **cosmo,
                    'synthetic_RA': float(ra[g]),
                    'synthetic_DE': float(dec[g]),
                    'synthetic_z': float(z[g]),
                    'curve_label': E.cremona_label() if hasattr(E, 'cremona_label') else f"rank{r}_{i}"
                })
        except Exception as e:
            print(f"   ⚠️ Skipped curve: {e}")
            continue


# Save synthetic catalog
df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)
print(f"\n🎉 SYNTHETIC COSMOS COMPLETE!")
print(f"   → {len(df):,} synthetic galaxies generated")
print(f"   → Saved to {OUTPUT_CSV}")
print(f"   → Ranks represented: {df['exact_rank'].unique().tolist()}")
print("\nYou can now compare this synthetic catalog to your real files (JApJ... and DESIDR8...) using the same feature columns.")


# Quick summary stats
print("\nSummary by rank:")
print(df.groupby('exact_rank')[['V_comove', 'rho_scale', 'betti_1']].mean().round(2))
