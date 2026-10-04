selected_lmfdb = random.sample(lmfdb_high_rank_labels, min(LMFDB_EXTRA_CURVES, len(lmfdb_high_rank_labels)))


with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
    future_to_label = {executor.submit(worker, label, 4, "LMFDB"): label for label in selected_lmfdb}
    for future in tqdm(concurrent.futures.as_completed(future_to_label), total=len(selected_lmfdb), desc="LMFDB high-rank"):
        cosmo = future.result()
        if 'error' in cosmo:
            continue
        for g in range(GALAXIES_PER_CURVE):
            results.append({**cosmo,
                            'synthetic_RA': float(np.random.normal(0, cosmo['rho_scale']/10)),
                            'synthetic_DE': float(np.random.normal(0, cosmo['rho_scale']/10)),
                            'synthetic_z': float(np.random.normal(cosmo['V_comove']/3e5, 0.008)),
                            'galaxy_id': f"{cosmo['cremona_label']}_g{g}"})


# Final save
pd.DataFrame(results).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
print(f"\n🎉 FULL SYNTHETIC COSMOS COMPLETE!")
print(f"   → Total galaxies: {pd.read_csv(OUTPUT_CSV).shape[0]:,}")
print(f"   → File: {OUTPUT_CSV}")
print(f"   → Sources: Full Cremona (ranks 1–3) + LMFDB high-rank")


print("\nSummary by rank:")
print(pd.read_csv(OUTPUT_CSV).groupby('exact_rank')[['V_comove', 'rho_scale', 'betti_1']].mean().round(2))


print("\nNext: reply with **compare synthetic** or **step 3**")
