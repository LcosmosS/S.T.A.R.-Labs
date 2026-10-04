# --- 1. Configuration ---
# Edit these variables to control the script's behavior.
INPUT_FILE = 'merged_galspec_gz2.csv'
OUTPUT_FILE = 'sagemath_run_results.csv'
CHUNKSIZE = int(100000)  # Number of rows to process at a time
ROW_LIMIT = 500000  # Set to None to process the full file, or a number for testing.

# --- 2. Imports ---
# Standard scientific libraries
import pandas as pd
import numpy as np
import sys
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
from astropy.constants import G

# SageMath specific imports
# These will be available when running in a SageMath environment.
from sage.all import EllipticCurve, QQ

# --- 3. Scientific Derivation Functions ---

def calculate_distance_mpc(z):
    """Calculates comoving distance from redshift using Planck18 cosmology."""
    if z is None or not np.isfinite(z) or z <= 0:
        return np.nan
    try:
        return cosmo.comoving_distance(z).to(u.Mpc).value
    except (ValueError, TypeError):
        return np.nan

def convert_logmass_to_sm(logmass):
    """Converts logarithmic mass to stellar mass in solar mass units."""
    if logmass is None or not np.isfinite(logmass):
        return np.nan
    return 10**logmass

def estimate_radius_ly(angular_size_arcsec, distance_mpc):
    """Estimates physical radius in light-years from angular size and distance."""
    if not np.isfinite(angular_size_arcsec) or not np.isfinite(distance_mpc) or angular_size_arcsec <= 0 or distance_mpc <= 0:
        return np.nan
    angle_rad = (angular_size_arcsec * u.arcsec).to(u.rad).value
    radius_mpc = distance_mpc * angle_rad
    return (radius_mpc * u.Mpc).to(u.lyr).value

def calculate_virial_energy(mass_sm, radius_ly):
    """Calculates the Virial Energy in Joules."""
    if not np.isfinite(mass_sm) or not np.isfinite(radius_ly) or mass_sm <= 0 or radius_ly <= 0:
        return np.nan
    mass_kg = mass_sm * 1.989e30
    radius_m = radius_ly * 9.461e15
    potential_energy = -1 * G.value * (mass_kg ** 2) / radius_m
    return potential_energy / 2.0

# --- 4. SageMath Core Hypothesis Functions ---

def map_physics_to_curve_coeffs(distance_mly, density_kg_m3):
    """Maps physical properties to elliptic curve coefficients 'a' and 'b'."""
    if not np.isfinite(distance_mly) or not np.isfinite(density_kg_m3):
        return np.nan, np.nan
    a = QQ(-distance_mly)
    b = QQ(density_kg_m3)
    return a, b

def calculate_sagemath_discriminant(a, b):
    """Calculates the discriminant using SageMath's native functionality."""
    if not isinstance(a, (int, float, complex)) or not isinstance(b, (int, float, complex)) or not np.isfinite(a) or not np.isfinite(b):
         return np.nan
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        return E.discriminant()
    except (TypeError, ValueError):
        return np.nan

# --- 5. Main Processing Pipeline ---

def main():
    """The main function to run the data processing pipeline."""
    try:
        chunk_iter = pd.read_csv(
            INPUT_FILE,
            chunksize=CHUNKSIZE,
            on_bad_lines='skip',
            low_memory=True
        )
    except FileNotFoundError:
        print(f"Error: Input file not found at '{INPUT_FILE}'.", file=sys.stderr)
        return

    total_rows_processed = 0
    header_written = False

    print(f"Starting SageMath pipeline for '{INPUT_FILE}'...")
    for i, chunk in enumerate(chunk_iter):
        print(f"Processing chunk {i+1}...")

        chunk.replace(-9999, np.nan, inplace=True)
        required_cols = ['z', 'logmass', 'petrorad_r']
        chunk.dropna(subset=required_cols, inplace=True)
        chunk = chunk[chunk['z'] > 0]

        if not chunk.empty:
            # Derive physical parameters
            chunk['distance_mpc'] = chunk['z'].apply(calculate_distance_mpc)
            chunk['mass_sm'] = chunk['logmass'].apply(convert_logmass_to_sm)
            chunk['radius_ly'] = chunk.apply(lambda row: estimate_radius_ly(row['petrorad_r'], row['distance_mpc']), axis=1)

            # Calculate Virial Energy and Density
            chunk['virial_energy_j'] = chunk.apply(lambda row: calculate_virial_energy(row['mass_sm'], row['radius_ly']), axis=1)

            valid_data = chunk['radius_ly'].notna() & (chunk['radius_ly'] > 0) & chunk['mass_sm'].notna()
            radius_m = chunk.loc[valid_data, 'radius_ly'] * 9.461e15
            mass_kg = chunk.loc[valid_data, 'mass_sm'] * 1.989e30
            volume_m3 = (4/3) * np.pi * (radius_m ** 3)
            chunk['density_kg_m3'] = np.nan
            chunk.loc[valid_data, 'density_kg_m3'] = mass_kg / volume_m3

            # Map to curve and calculate discriminant using SageMath
            distance_mly = chunk['distance_mpc'] * 3.26156
            coeffs = chunk.apply(lambda row: map_physics_to_curve_coeffs(distance_mly.get(row.name), row['density_kg_m3']), axis=1)
            chunk[['coeff_a', 'coeff_b']] = pd.DataFrame(coeffs.tolist(), index=chunk.index)
            chunk['discriminant'] = chunk.apply(lambda row: calculate_sagemath_discriminant(row['coeff_a'], row['coeff_b']), axis=1)

            # Calculate the scaling constant
            chunk['scaling_constant_K'] = chunk['virial_energy_j'] / chunk['discriminant'].astype(float)

            # Define and save output
            output_cols = [
                'objid', 'ra', 'dec', 'z', 'mass_sm', 'radius_ly',
                'distance_mpc', 'virial_energy_j', 'discriminant', 'scaling_constant_K'
            ]

            # Ensure all output columns exist before saving
            for col in output_cols:
                if col not in chunk.columns:
                    chunk[col] = np.nan

            processed_chunk = chunk[output_cols]
            processed_chunk.to_csv(
                OUTPUT_FILE,
                mode='a',
                header=not header_written,
                index=False
            )
            header_written = True

        total_rows_processed += len(chunk)
        if ROW_LIMIT and total_rows_processed >= ROW_LIMIT:
            print(f"Reached row limit of {ROW_LIMIT}. Stopping.")
            break

    print("\nPipeline finished.")
    print(f"Total rows processed from input: {total_rows_processed}")
    print(f"Results saved to '{OUTPUT_FILE}'")
    print(f"\nTo analyze the results, you can now run:\nimport pandas as pd\ndf = pd.read_csv('{OUTPUT_FILE}')\nprint(df.head())\nprint(df['scaling_constant_K'].describe())")

# --- 6. Script Execution ---
if __name__ == "__main__":
    main()
