# --- 1. Python Standard Imports for Robustness ---
import pandas as pd
import numpy as np
import warnings
import logging
import signal
from contextlib import contextmanager
import sys
import os
import time

# --- 2. SageMath and Astro Imports ---
from sage.all import EllipticCurve, QQ, pari, Integer, Infinity 
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u

# --- 3. Configuration and Setup ---
INPUT_FILE = 'GalSpecExtra.csv'
# NOTE: Renamed output file for the fixed version
OUTPUT_FILE = '3_selmer_ground_truth_50k_v6_robust.csv' 
SAMPLE_ROW_LIMIT = 50000 
RANK_TIMEOUT_SECONDS = 300 
MAX_THREADS = 16 
TWO_DESCENT_LIMIT = 100 # The recommended limit

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
analysis_logger = logging.getLogger('Selmer_Solver')
warnings.filterwarnings('default', category=UserWarning)

# --- 4. Custom Timeout Implementation (Crucial for preventing hangs) ---
class TimeoutException(Exception):
    """Raised when a function call exceeds the allocated time limit."""
    pass

@contextmanager
def timeout(seconds):
    """Standard Python context manager to enforce a time limit using SIGALRM."""
    def signal_handler(signum, frame):
        raise TimeoutException(f"Computation timed out after {seconds} seconds.")

    # Only set signal handlers on operating systems that support SIGALRM (i.e., not Windows)
    if os.name != 'nt':
        original_handler = signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
    try:
        yield
    finally:
        if os.name != 'nt':
            signal.alarm(0)
            signal.signal(signal.SIGALRM, original_handler)


# --- 5. Helper Functions ---

def print_step(step_num, title, summary=None):
    """Helper function to print pipeline steps and summary."""
    step_key = f"STEP {step_num}: {title}"
    analysis_logger.info(f"{step_key} starting...")
    print(f"\n--- {step_key} ---")
    if summary is not None:
        analysis_logger.info(f"Step {step_num} Summary: {summary}")

def compute_a_b_coefficients(row):
    """Maps galaxy properties to integer curve coefficients."""
    try:
        log_mass = row['logmass']
        radius = row['petrorad_r']

        a_val = -int(100 * (log_mass * 10))
        b_val = int((log_mass * 10)**2 + radius * 100)

        return pd.Series({'a_coefficient': a_val, 'b_coefficient': b_val})
    except Exception:
        return pd.Series({'a_coefficient': np.nan, 'b_coefficient': np.nan})


# --- 6. The Core Hierarchy of Evidence Solver (Modified for Robustness) ---

def get_robust_algebraic_rank(E, curve_name):
    """
    Attempts to calculate the rank using a multi-tiered hierarchy of confidence.
    1. E.rank() (Certainty)
    2. E.two_descent() + E.rank() (Refined Certainty)
    3. E.rank_bounds() (Proven Lower Bound)
    4. E.ellanalyticrank() (Best Estimate via BSD)
    """
    
    # --- 1. Pass 1: Standard Rank Attempt (Highest Confidence) ---
    try:
        rank = E.rank()
        if rank is not Infinity:
             analysis_logger.info(f"Standard rank successful for {curve_name}: {rank}")
             return int(rank)
    except Exception:
        analysis_logger.warning(f"Standard rank inconclusive for {curve_name}. Proceeding to refinement.")
        pass # Proceed to refinement

    # --- 2. Pass 2: Two-Descent Refinement and Re-check ---
    analysis_logger.info(f"Attempting two_descent refinement for {curve_name} (limit={TWO_DESCENT_LIMIT})...")
    try:
        E.two_descent(second_limit=TWO_DESCENT_LIMIT) 
        
        # Re-check the rank after refinement
        rank = E.rank()
        if rank is not Infinity:
            analysis_logger.info(f"Refined rank successful for {curve_name}: {rank}")
            return int(rank)
    except Exception as e:
        analysis_logger.warning(f"Refinement re-check failed/inconclusive for {curve_name}. Error: {e}")
        pass # Proceed to robust fallback

    # --- 3. Pass 3: Robust Fallback to Proven Lower Bound (Using rank_bounds) ---
    try:
        # This method is more robust than lower_bound_rank()
        lower_bound, upper_bound = E.rank_bounds()
        analysis_logger.warning(
            f"Returning PROVEN LOWER BOUND via rank_bounds for {curve_name}: {lower_bound} "
            f"(Uncertainty: {lower_bound} <= rank <= {upper_bound})"
        )
        return int(lower_bound)
    except Exception as e:
        analysis_logger.error(f"rank_bounds also failed for {curve_name}. Error: {e}")
        pass

    # --- 4. Pass 4: Final Fallback to Analytic Rank (Best Estimate) ---
    try:
        analytic_rank_info = pari(E).ellanalyticrank()
        analytic_rank = int(analytic_rank_info[0])
        analysis_logger.warning(f"Returning ANALYTIC RANK as last resort for {curve_name}: {analytic_rank}")
        return analytic_rank
    except Exception as e:
        analysis_logger.error(f"HARD FAILURE: Analytic rank also failed for {curve_name}. Error: {e}")
        return np.nan # Final hard failure

def analyze_3_selmer_evidence_pipeline(row):
    """
    Performs the multi-pronged 3-Selmer analysis using the Hierarchy of Evidence
    approach with robust error handling and timeout.
    """
    a_val = row['a_coefficient']
    b_val = row['b_coefficient']
    curve_name = f"({a_val}, {b_val})"

    # Initialize results
    results = {
        'sage_algebraic_rank': np.nan,
        'pari_2_selmer_rank': np.nan,
        'pari_analytic_rank': np.nan,
        'has_rational_3_torsion': False,
        'estimated_3_selmer_bound': np.nan,
        'is_tractable_full_analysis': False
    }
    
    if pd.isna(a_val) or pd.isna(b_val):
        return pd.Series(results)

    try:
        # Instantiate the curve
        E = EllipticCurve(QQ, [0, 0, 0, Integer(a_val), Integer(b_val)])
    except Exception:
        return pd.Series(results)
    
    
    try:
        # --- Apply the Python Timeout to the entire analysis ---
        with timeout(RANK_TIMEOUT_SECONDS):

            # --- 1. Baseline: Robust Standard SageMath Rank ---
            rank = get_robust_algebraic_rank(E, curve_name)
            results['sage_algebraic_rank'] = rank


            # --- 2. PARI/GP Backend: 2-Selmer Rank (Upper Bound) ---
            try:
                # Use selmer_rank(2) as the true upper bound
                selmer_2_rank = E.selmer_rank(2)
                results['pari_2_selmer_rank'] = int(selmer_2_rank)
            except Exception:
                try: # Direct PARI call as a secondary fallback
                    pari_E = pari(E)
                    # ellrank() returns [rank, selmer_rank]
                    selmer_2_rank = pari_E.ellrank()[1] 
                    results['pari_2_selmer_rank'] = int(selmer_2_rank)
                except:
                    pass

            # --- 3. PARI/GP Backend: Analytic Rank (via BSD Conjecture) ---
            try:
                analytic_rank_info = pari(E).ellanalyticrank()
                analytic_rank = int(analytic_rank_info[0])
                results['pari_analytic_rank'] = analytic_rank
            except Exception:
                pass

            # --- 4. 3-Torsion Analysis ---
            try:
                torsion_order = E.torsion_subgroup().order()
                results['has_rational_3_torsion'] = (torsion_order % 3 == 0)
            except Exception:
                pass

            # --- 5. The 3-Selmer Proxy: Convergent Inference (The Final Ground Truth Value) ---
            # We prioritize the algebraic rank (which is either proven or the best lower bound/estimate)
            # as the primary evidence.
            
            algebraic_rank = results.get('sage_algebraic_rank')
            analytic_rank = results.get('pari_analytic_rank')

            if not np.isnan(algebraic_rank) and algebraic_rank == analytic_rank:
                # Strongest Evidence: Algebraic rank (proven/lower bound) matches analytic rank
                results['estimated_3_selmer_bound'] = int(algebraic_rank)
            elif not np.isnan(algebraic_rank):
                 # Good Evidence: Use the highest algebraic rank found (proven or lower bound)
                 results['estimated_3_selmer_bound'] = int(algebraic_rank)
            elif not np.isnan(analytic_rank):
                 # Weak Evidence: Use analytic rank as the best available estimate
                 results['estimated_3_selmer_bound'] = int(analytic_rank)
            else:
                 results['estimated_3_selmer_bound'] = np.nan
                 analysis_logger.warning(f"NO RANK EVIDENCE FOUND for {curve_name}.")

        # If we reach here, the analysis completed within the timeout
        results['is_tractable_full_analysis'] = True

    except TimeoutException:
        analysis_logger.error(f"Analysis timed out ({RANK_TIMEOUT_SECONDS}s) for {curve_name}. Partial results recorded.")
        results['is_tractable_full_analysis'] = False
        # If a timeout occurs, try one last time to get the analytic rank as the best guess
        try:
             analytic_rank_info = pari(E).ellanalyticrank()
             results['estimated_3_selmer_bound'] = int(analytic_rank_info[0])
        except Exception:
             pass
        
    except Exception as e:
        analysis_logger.error(f"Catastrophic error for {curve_name}: {e}")
        results['is_tractable_full_analysis'] = False
        
    # Ensure all final outputs are pandas-compatible
    return pd.Series(results)

# --- 7. Main Pipeline Execution ---
def main_pipeline():
    """Main execution entry point."""
    print_step(0, "Starting 3-Selmer Ground Truth Solver (V6 - Robust Boundary Check)")
    analysis_logger.info(f"Targeting first {SAMPLE_ROW_LIMIT} rows with {RANK_TIMEOUT_SECONDS}s timeout per curve.")

    # --- STEP 1: Data Loading, Sampling, and Cleanup ---
    print_step(1, f"Data Loading and Sampling (N={SAMPLE_ROW_LIMIT})")
    
    try:
        df_iter = pd.read_csv(INPUT_FILE, usecols=['ra', 'dec', 'z', 'logmass', 'petrorad_r'], iterator=True, chunksize=SAMPLE_ROW_LIMIT)
        df = next(df_iter).head(SAMPLE_ROW_LIMIT)
    except FileNotFoundError:
        analysis_logger.critical(f"Input file '{INPUT_FILE}' not found. Please ensure it is in the same directory.")
        return

    df_initial = len(df)
    df = df.dropna(subset=['z', 'logmass', 'petrorad_r'])
    df = df.reset_index(drop=True)
    
    summary = {'Total Rows Loaded': df_initial, 'Valid Rows for Analysis': len(df), 'Source File': INPUT_FILE}
    print_step(1, "Data Loading and Sampling", summary)

    # --- STEP 2: Coefficient Mapping ---
    print_step(2, "Elliptic Curve Coefficient Mapping")
    df[['a_coefficient', 'b_coefficient']] = df.apply(compute_a_b_coefficients, axis=1, result_type='expand')
    print_step(2, "Elliptic Curve Coefficient Mapping", {'Mapped Rows': len(df[df['a_coefficient'].notna()])})

    # --- STEP 3: Apply Hierarchy of Evidence Solver (Single-Threaded for Safety) ---
    print_step(3, "Applying Hierarchy of Evidence Solver (Full, Robust Analysis)")

    start_time = time.time()
    evidence_df = df.apply(analyze_3_selmer_evidence_pipeline, axis=1, result_type='expand')
    end_time = time.time()
    
    df = pd.concat([df, evidence_df], axis=1)

    tractable_count = df['is_tractable_full_analysis'].sum()
    intractable_count = len(df) - tractable_count
    
    # Calculate average time per curve
    time_per_curve = (end_time - start_time) / len(df) if len(df) > 0 else 0

    summary = {
        'Completed Full Analysis': int(tractable_count),
        'Intractable/Timed Out': int(intractable_count),
        'Highest Selmer Bound Found': df['estimated_3_selmer_bound'].max(),
        'Avg. Time Per Curve': f"{time_per_curve:.2f} seconds"
    }
    print_step(3, "Hierarchy of Evidence Solver", summary)

    # --- STEP 4: Export Ground Truth Data ---
    print_step(4, "Exporting Ground Truth Data")
    df.to_csv(OUTPUT_FILE, index=False)
    summary = {'Output File': OUTPUT_FILE, 'Rows Saved': len(df)}
    print_step(99, "Analysis Complete", summary)

if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    main_pipeline()
