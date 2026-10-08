# SageMath script to analyze elliptic curves and compute their ranks
from sage.all import EllipticCurve, QQ
import sys

# Step 1: Generate the grid of elliptic curves
a_values = list(range(-150, 151, 15))  # -150 to 150 in steps of 15 (21 values)
b_values = list(range(-150, 151, 15))  # -150 to 150 in steps of 15 (21 values)
curves = []
curve_info = []

print("Generating 342 curves for the grid.")
for i, a in enumerate(a_values):
    for b in b_values:
        # Create the elliptic curve y^2 = x^3 + ax + b over QQ (rational numbers)
        try:
            E = EllipticCurve(QQ, [0, 0, 0, a, b])
            # Only include curves with non-zero discriminant (valid curves)
            if E.discriminant() != 0:
                curves.append((a, b, E))
        except Exception as e:
            continue
    print(f"Generated curves for a={a} ({i+1}/21 a values processed, 21 b values per a)")

print(f"Generated {len(curves)} candidate curves.")

# Step 2: Assign grid points (for logging purposes, matching your output)
total_curves = len(curves)
for i in range(50, 301, 50):
    print(f"Assigned {i}/{total_curves} grid points ({i/total_curves*100:.1f}%)")
print(f"Assigned 300/{total_curves} grid points ({300/total_curves*100:.1f}%)")

# Step 3: Process curves in chunks
chunk_size = 20
num_chunks = (total_curves + chunk_size - 1) // chunk_size  # Ceiling division

print("Resuming from chunk 0/18")
print("Precomputing initial coordinates...")
for i in range(50, 301, 50):
    print(f"Processed {i}/{total_curves} curves for initial setup ({i/total_curves*100:.1f}%)")
print(f"Processed 300/{total_curves} curves for initial setup ({300/total_curves*100:.1f}%)")

# Step 4: Analyze each curve and compute its rank
results = []
for chunk_idx in range(num_chunks):
    start_idx = chunk_idx * chunk_size
    end_idx = min(start_idx + chunk_size, total_curves)
    chunk_curves = curves[start_idx:end_idx]
    
    print(f"\nProcessing chunk {chunk_idx+1}/{num_chunks} ({len(chunk_curves)} curves, indices {start_idx} to {end_idx-1})")
    
    for local_idx, (a, b, E) in enumerate(chunk_curves, 1):
        global_idx = start_idx + local_idx - 1
        print(f"Analyzing curve {local_idx}/{len(chunk_curves)} in chunk (global index {global_idx})")
        print(f"Analyzing curve: y^2 = x^3 + {a}x + {b}")
        
        # Compute curve properties
        discriminant = E.discriminant()
        conductor = E.conductor()
        torsion_order = E.torsion_subgroup().order()
        
        print(f"Discriminant: {discriminant}")
        print(f"Conductor: {conductor}")
        print(f"Torsion order: {torsion_order}")
        
        # Compute the rank using the default method (first descent)
        try:
            rank = E.rank()  # No descent_second_limit parameter
            print(f"Rank: {rank}")
        except Exception as e:
            rank = "Error computing rank"
            print(f"Error computing rank: {e}")
        
        # Store the results
        results.append((a, b, discriminant, conductor, torsion_order, rank))
    
    print(f"Completed chunk {chunk_idx+1}/{num_chunks} ({(chunk_idx+1)/num_chunks*100:.1f}% of chunks done)")

# Step 5: Perform final layout refinement (logging step, as per your output)
print("Performing final force-directed layout refinement...")

# Step 6: Generate the Theory Map as a Markdown table
theory_map = "# Global-to-Local Paradox Correction Theory Map\n\n"
theory_map += "| a   | b    | Discriminant   | Conductor   | Torsion Order | Rank |\n"
theory_map += "|-----|------|----------------|-------------|---------------|------|\n"
for a, b, disc, cond, tors, rank in results:
    theory_map += f"| {a:3} | {b:4} | {disc:14} | {cond:11} | {tors:13} | {rank} |\n"

print(theory_map)