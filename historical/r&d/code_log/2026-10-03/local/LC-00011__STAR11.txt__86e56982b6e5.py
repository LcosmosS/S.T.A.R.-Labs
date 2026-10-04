# Function to standardize RA/Dec =======================================================================================================================================================================
def standardize_columns(df, cols):
    df = df[cols].copy()
    if 'RA_ICRS' in df.columns and 'DE_ICRS' in df.columns:
        df = df.rename(columns={"RA_ICRS": "objra_y", "DE_ICRS": "objdec"})
    elif 'ra' in df.columns and 'dec' in df.columns:
        df = df.rename(columns={"ra": "objra_y", "dec": "objdec"})
    return df


# Incremental merge ======================================================================================================================================================================
print("Merging Datasets...")
merged_df = None
for i, file in tqdm(enumerate(csv_files), total=len(csv_files), desc="Merging CSV Files"):
    print(f"Loading {file} ({i+1}/{len(csv_files)})...")
    try:
        chunksize = 50000
        df_chunks = pd.read_csv(file, usecols=column_mappings[file], chunksize=chunksize)
        df = pd.concat([standardize_columns(chunk, column_mappings[file]) for chunk in df_chunks], ignore_index=True)
        print(f"Rows in {file}: {len(df)}, Columns: {len(df.columns)}")
        if 'objid' in df.columns:
            print(f"objid present in {file}")
        else:
            print(f"No objid in {file}")
    except ValueError as e:
        print(f"Error loading {file}: {e}. Check column names.")
        continue
    
    if merged_df is None:
        merged_df = df
    else:
        merge_keys = ['objra_y', 'objdec']
        if 'objid' in merged_df.columns and 'objid' in df.columns:
            merge_keys.append('objid')
        merged_df = merged_df.merge(df, on=merge_keys, how='left', suffixes=('', f'_dup_{i}'))
        dup_cols = [col for col in merged_df.columns if f'_dup_{i}' in col]
        merged_df = merged_df.drop(columns=dup_cols)
    
    merged_df = merged_df.drop_duplicates(subset=['objra_y', 'objdec'], keep='first')
    print(f"Rows after merging {file}: {len(merged_df)}")
# - Save intermediate result per file --------------------------------------------------------------------------------------------------------------------------------
    temp_file = f"temp_merge_step_{i+1}.csv"
    merged_df.to_csv(temp_file, index=False)
    print(f"Saved to {temp_file}")


# Final assignment and save after all merges ==========================================================================================================================
df = merged_df
df.to_csv("*STAR_preprocess.csv", index=False)
print(f"Completed merging. Final rows: {len(df)}, columns: {len(df.columns)}. Saved to *STAR_preprocess.csv")
print("Preprocessing completed. Engineering features...")


# Clean metallicity and sfr columns by replacing -9999 with NaN =======================================================================================================
df[['metallicity', 'sfr']] = df[['metallicity', 'sfr']].replace(-9999, np.nan)
print(f"Replaced -9999 with NaN in 'metallicity' and 'sfr' columns.")
print(f"NaN in metallicity: {df['metallicity'].isna().sum()}, NaN in sfr: {df['sfr'].isna().sum()}")


# Merge Diagnostics ===================================================================================================================================================
key_columns = ['objra_y', 'objdec', 'zsp', 'flux_Ha', 'logmass', 'petrorad_r']
missing_cols = [col for col in key_columns if col not in df.columns]
if missing_cols:
    print(f"Warning: Missing key columns after merge: {missing_cols}")
else:
    print("All key columns present after merge.")
print(f"Sample data:\n{df[key_columns].head() if not missing_cols else df.head()}")


# Downcast numeric columns to save memory =============================================================================================================================
def downcast_df(df):
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    return df
df = downcast_df(df)
print(f"Memory usage after downcast: {df.memory_usage().sum() / 1024**2:.2f} MB")


# Ensure RA/Dec are numeric and impute NaN/infinities with medians ====================================================================================================
df['objra_y'] = pd.to_numeric(df['objra_y'], errors='coerce')
df['objdec'] = pd.to_numeric(df['objdec'], errors='coerce')
print(f"Initial df: objra_y dtype: {df['objra_y'].dtype}, objdec dtype: {df['objdec'].dtype}")
print(f"NaN in objra_y: {df['objra_y'].isna().sum()}, NaN in objdec: {df['objdec'].isna().sum()}")
df['objra_y'] = df['objra_y'].replace([np.inf, -np.inf], np.nan).fillna(df['objra_y'].median(skipna=True))
df['objdec'] = df['objdec'].replace([np.inf, -np.inf], np.nan).fillna(df['objdec'].median(skipna=True))
print(f"Rows after RA/Dec imputation: {len(df)}")


# Impute NaN/infinities for all numeric columns =======================================================================================================================
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    df[col] = df[col].replace([np.inf, -np.inf], np.nan).fillna(df[col].median(skipna=True))


# Recompute log_SFR_Ha and metallicity ================================================================================================================================
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']
for col in flux_cols:
    print(f"NaN count in {col} after imputation: {df[col].isna().sum()}")
df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']
Ha_Hb_intrinsic = 2.86
k_Ha = 2.468
k_Hb = 3.634
df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha))
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])


# Define cosmology ====================================================================================================================================================
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
sfr_conversion = 7.9e-42 * u.Msun / u.yr / u.erg * u.s  # Kennicutt 1998, Salpeter IMF


# Cluster galaxies using RA/Dec and redshift (optimized with parallelization) =========================================================================================
print("initiating galaxy clustering...")
start_time = time.time()


# Convert coordinates to Cartesian for clustering =====================================================================================================================
coords = SkyCoord(ra=df['objra_y']*u.deg, dec=df['objdec']*u.deg, distance=df['zsp']*cosmo.hubble_distance, frame='icrs')
xyz = coords.cartesian.xyz.value.T  # Shape: (n_rows, 3)


# Build the cKDTree ===================================================================================================================================================
tree = cKDTree(xyz)
dist_threshold = 1 / cosmo.hubble_distance.value  # ~1 Mpc


# Function to compute neighbors for a chunk of indices ================================================================================================================
def compute_neighbors_chunk(chunk_indices, xyz_data, dist_thr):
    local_tree = cKDTree(xyz_data)  # Rebuild tree for consistency (small overhead)
    return [len(local_tree.query_ball_point(xyz_data[i], r=dist_thr)) - 1 for i in chunk_indices]


# Parallelize the neighbor search =====================================================================================================================================
n_cores = mp.cpu_count()  # Use all available cores on SciServer
chunk_size = len(df) // n_cores
if chunk_size == 0:
    chunk_size = len(df)  # Handle case where n_rows < n_cores


index_chunks = [range(i, min(i + chunk_size, len(df))) for i in range(0, len(df), chunk_size)]
pool = mp.Pool(processes=n_cores)
compute_neighbors_partial = partial(compute_neighbors_chunk, xyz_data=xyz, dist_thr=dist_threshold)


# Compute neighbors in parallel =======================================================================================================================================
results = pool.map(compute_neighbors_partial, index_chunks)
pool.close()
pool.join()


# Flatten the results =================================================================================================================================================
cluster_density = []
for chunk_result in results:
    cluster_density.extend(chunk_result)


df['cluster_density'] = cluster_density


# Diagnostics =======================================================================================================================================================================
end_time = time.time()
print(f"Clustering completed in {end_time - start_time:.2f} seconds.")
print(f"Memory usage after clustering: {df.memory_usage().sum() / 1024**2:.2f} MB")
print(f"cluster_density: mean={df['cluster_density'].mean():.2f}, std={df['cluster_density'].std():.2f}, "
      f"min={df['cluster_density'].min():.2f}, max={df['cluster_density'].max():.2f}")


# Galactic extinction correction (enhanced with caching and robust error handling) ====================================================================================
print("Applying galactic extinction correction...")
start_time = time.time()


# Define cache file for ebv values ====================================================================================================================================
ebv_cache_file = "ebv_cache.pkl"


# Check if cached ebv values exist ====================================================================================================================================
if os.path.exists(ebv_cache_file):
    print(f"Loading cached EBV values from {ebv_cache_file}...")
    with open(ebv_cache_file, 'rb') as f:
        ebv = pickle.load(f)
else:
# = Initialize SFDQuery ===============================================================================================================================================
    try:
        sfd = SFDQuery()
    except FileNotFoundError:
        print("SFD dustmap not found. Fetching now...")
        try:
            import dustmaps.sfd
            dustmaps.sfd.fetch()
            sfd = SFDQuery()
        except Exception as e:
            print(f"Failed to fetch SFD dustmap due to {e}. Will use fallback.")
            sfd = None
    except Exception as e:
        print(f"Failed to initialize SFDQuery due to {e}. Will use fallback.")
        sfd = None
# = Compute ebv values ---------------------------------------------------------------------------------------------
    if sfd is not None:
        try:
# ========= Validate coordinates -----------------------------------------------------------------------------------
            if not coords.is_finite().all():
                raise ValueError("Invalid coordinates detected in SkyCoord object.")
            ebv = sfd(coords)
            ebv = np.array(ebv, dtype=np.float32)
# ======== Validate ebv values --------------------------------------------------------------------------------------
            ebv = np.where(np.isfinite(ebv) & (ebv >= 0), ebv, 0.0)  # Replace NaN/inf and negative values with 0
# ======== Cache the ebv values --------------------------------------------------------------------------------------
            with open(ebv_cache_file, 'wb') as f:
                pickle.dump(ebv, f)
            print(f"Cached EBV values to {ebv_cache_file}.")
        except Exception as e:
            print(f"Failed to compute EBV due to {e}. Will use fallback.")
            ebv = None
    else:
        ebv = None
# Fallback if ebv computation failed -----------------------------------------------------------------------------------
if ebv is None:
    print("Warning: Using median-based fallback for galactic extinction correction.")
# = Estimate a reasonable A_Ha_mw based on typical EBV values (e.g., 0.05 as a median for low-latitude regions) =======================================================
    typical_ebv = 0.05
    A_Ha_mw = k_Ha * typical_ebv * 3.1  # Rv = 3.1
    A_Ha_mw = np.full(len(df), A_Ha_mw, dtype=np.float32)
else:
    A_Ha_mw = k_Ha * ebv * 3.1  # Rv = 3.1
# Diagnostics for A_Ha_mw ------------------------------------------------------------------------------------------------
print(f"A_Ha_mw: mean={np.mean(A_Ha_mw):.4f}, std={np.std(A_Ha_mw):.4f}, "
      f"min={np.min(A_Ha_mw):.4f}, max={np.max(A_Ha_mw):.4f}")
if ebv is not None:
    print(f"EBV: mean={np.mean(ebv):.4f}, std={np.std(ebv):.4f}, "
          f"min={np.min(ebv):.4f}, max={np.max(ebv):.4f}")


# Update flux_Ha_corr with extinction correction ======================================================================================================================
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * (df['A_Ha'] + A_Ha_mw))


# Diagnostics for flux_Ha_corr ========================================================================================================================================
print(f"flux_Ha_corr: mean={df['flux_Ha_corr'].mean():.4f}, std={df['flux_Ha_corr'].std():.4f}, "
      f"NaN={df['flux_Ha_corr'].isna().sum()}, Inf={np.isinf(df['flux_Ha_corr']).sum()}")


end_time = time.time()
print(f"Galactic extinction correction completed in {end_time - start_time:.2f} seconds.")


# Compute luminosity distance and SFR =================================================================================================================================
df['DL'] = cosmo.luminosity_distance(df['zsp']).to(u.cm).value
df['L_Ha'] = (df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2 * u.erg / u.s).to(u.L_sun).value
df['log_SFR_Ha_raw'] = np.log10((df['L_Ha'] * sfr_conversion).value)
print(f"NaN in L_Ha: {df['L_Ha'].isna().sum()}")
print(f"NaN in log_SFR_Ha_raw: {df['log_SFR_Ha_raw'].isna().sum()}")


# Add raw fluxes/morpholohicals as features ===========================================================================================================================
df['log_flux_Ha'] = np.log10(df['flux_Ha'] + 1e-10)
df['log_flux_Hb'] = np.log10(df['flux_Hb'] + 1e-10)
df['log_flux_OIII_5007'] = np.log10(df['flux_OIII_5007'] + 1e-10)
df['log_flux_NII_6584'] = np.log10(df['flux_NII_6584'] + 1e-10)
df['log_e_flux_Ha'] = np.log10(df['e_flux_Ha'] + 1e-10)


# Compute metallicity =================================================================================================================================================
df['log_O3N2_raw'] = np.log10((df['flux_OIII_5007'] / df['flux_Hb']) / (df['flux_NII_6584'] / df['flux_Ha']) + 1e-10)
df['OH_O3N2_raw'] = 8.533 - 0.214 * df['log_O3N2_raw']


# Add photometric colors ==============================================================================================================================================
if 'umag' in df.columns and 'gmag' in df.columns:
    df['color_ug'] = df['umag'] - df['gmag']
    df['color_gr'] = df['gmag'] - df['rmag']
    df['color_ri'] = df['rmag'] - df['imag']
    df['color_iz'] = df['imag'] - df['zmag']
    df['e_color_ug'] = np.sqrt(df['e_umag']**2 + df['e_gmag']**2)
    df['e_color_gr'] = np.sqrt(df['e_gmag']**2 + df['e_rmag']**2)
if 'Jmag' in df.columns and 'Kmag' in df.columns:
    df['color_JK'] = df['Jmag'] - df['Kmag']
    df['e_color_JK'] = np.sqrt(df['e_Jmag']**2 + df['e_Kmag']**2)


# Step 1: Cosmo-Rank Construction (flux or morphological features) ====================================================================================================
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']
if 'ellipticity' in df.columns and ('zsp' in df.columns or 'z' in df.columns):
    gz_df = df[['ellipticity']].copy()
    gz_df['redshift'] = df['zsp'] if 'zsp' in df.columns else df['z']
    gz_df['morph_proxy'] = gz_df['ellipticity']
    gz_df['Num_w'] = 1.0
    scaler_rank = MinMaxScaler()
    gz_df[['morph_norm', 'Num_w_norm', 'redshift_norm']] = scaler_rank.fit_transform(
        gz_df[['morph_proxy', 'Num_w', 'redshift']]
    )
    df['cosmo_rank'] = 0.5 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_norm'] + 0.2 * gz_df['redshift_norm']
    print("Computed cosmo_rank using ellipticity and redshift proxies.")
else:
    print("Warning: ellipticity or redshift missing. Setting cosmo_rank to 0.5.")
    df['cosmo_rank'] = 0.5


# Ensure cosmo_rank is numeric and imputed ============================================================================================================================
df['cosmo_rank'] = pd.to_numeric(df['cosmo_rank'], errors='coerce').replace([np.inf, -np.inf], np.nan).fillna(0.5)


# Step 2: L_cosmo(s) Construction =====================================================================================================================================
if 'logmass' in df.columns:
    df['logMass'] = df['logmass']
if 'petrorad_r' in df.columns:
    df['kronRad'] = df['petrorad_r']


alpha = -1.5
if 'logMass' in df.columns and 'kronRad' in df.columns:
    df['log_Mass_gas'] = df['logMass']
    M_star = df['log_Mass_gas'].median()
    df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
    
# = Preprocess kronRad ------------------------------------------------------------------------------------------
    df['kronRad'] = df['kronRad'].replace([np.inf, -np.inf], np.nan).fillna(df['kronRad'].median(skipna=True))
    if df['kronRad'].isna().all():
        print("Warning: kronRad is all NaN after preprocessing. Setting L_cosmo_s_* to 0.")
        for s in [0.5, 1.0, 1.5, 2.0]:
            df[f'L_cosmo_s_{s:.1f}'] = 0
    else:


# ======= Try quantile binning first ------------------------------------------------------------------------------
        try:
            bins = pd.qcut(df['kronRad'], q=20, labels=False, duplicates='drop') + 1
            df['z_bin'] = bins
            n_bins = df['z_bin'].nunique()
            print(f"Number of unique bins (qcut): {n_bins}")
            print("Bin distribution for kronRad (qcut):")
            print(df['z_bin'].value_counts().sort_index())
        except Exception as e:
            print(f"Warning: pd.qcut failed due to {e}. Falling back to pd.cut.")


# ======== Fallback to equal-width binning ---------------------------------------------------------------------------
            try:
                bins = pd.cut(df['kronRad'], bins=20, labels=False, duplicates='drop') + 1
                df['z_bin'] = bins
                n_bins = df['z_bin'].nunique()
                print(f"Number of unique bins (cut): {n_bins}")
                print("Bin distribution for kronRad (cut):")
                print(df['z_bin'].value_counts().sort_index())
            except Exception as e:
                print(f"Warning: pd.cut also failed due to {e}. Using median-based fallback.")
                df['z_bin'] = (df['kronRad'] > df['kronRad'].median()).astype(int) + 1  # Binary split
                n_bins = df['z_bin'].nunique()
                print(f"Number of unique bins (fallback): {n_bins}")
                print("Bin distribution for kronRad (fallback):")
                print(df['z_bin'].value_counts().sort_index())


# ======== Ensure a minimum number of bins ---------------------------------------------------------------------------------
        if n_bins < 5:
