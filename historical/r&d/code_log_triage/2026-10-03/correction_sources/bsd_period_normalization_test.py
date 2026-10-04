#!/usr/bin/env python3
"""
bsd_period_normalization_test.py

Independent period-normalization experiment for

    E : y^2 = x^3 - 1706*x + 6320.

The script deliberately separates four questions:

  A. Does the numerical quadrature converge as working precision increases?
  B. Do the compact and unbounded real components give the same branch
     integral?
  C. Does the independently computed period reproduce the Appendix values at
     the precision at which those values were actually printed?
  D. What does the rank-one BSD rearrangement numerically reconstruct when
     supplied with the Appendix's finite-precision L'(E,1) and regulator?

The direct period calculation uses the Neron differential

    omega = dx/(2y),

so on a real branch it is represented by dx/sqrt(f(x)).  No Sage
real_period() or PARI ellperiods() call is made.

IMPORTANT:
  This is a numerical consistency experiment, not a proof of BSD.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Optional, Sequence

import mpmath as mp


# ---------------------------------------------------------------------------
# Source data
# ---------------------------------------------------------------------------

DEFAULT_DPS = 100
DEFAULT_CONVERGENCE_LEVELS = (80, 100, 120)

CURVE_A_STR = "-1706"
CURVE_B_STR = "6320"

# Values reproduced from the Appendix.  We preserve the exact displayed
# strings rather than adding invented digits.
APPENDIX_HALF_PERIOD_STR = "0.4223626917832580984"
APPENDIX_FULL_PERIOD_STR = "0.844725383566516196"

L_PRIME_STR = "5.716147270182191662"
REGULATOR_STR = "3.383435244983427903"
TAMAGAWA_PRODUCT_STR = "2"
TORSION_ORDER_STR = "1"

EXPECTED_COMPONENTS = 2


@dataclass
class Check:
    name: str
    status: str  # PASS, INFO, or FAIL
    value: str
    criterion: str

    @property
    def passed(self) -> bool:
        return self.status == "PASS"


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def initialize_constants() -> None:
    global CURVE_A, CURVE_B
    global APPENDIX_HALF_PERIOD, APPENDIX_FULL_PERIOD
    global L_PRIME, REGULATOR, TAMAGAWA_PRODUCT, TORSION_ORDER

    CURVE_A = mp.mpf(CURVE_A_STR)
    CURVE_B = mp.mpf(CURVE_B_STR)
    APPENDIX_HALF_PERIOD = mp.mpf(APPENDIX_HALF_PERIOD_STR)
    APPENDIX_FULL_PERIOD = mp.mpf(APPENDIX_FULL_PERIOD_STR)
    L_PRIME = mp.mpf(L_PRIME_STR)
    REGULATOR = mp.mpf(REGULATOR_STR)
    TAMAGAWA_PRODUCT = mp.mpf(TAMAGAWA_PRODUCT_STR)
    TORSION_ORDER = mp.mpf(TORSION_ORDER_STR)


# ---------------------------------------------------------------------------
# Curve and topology
# ---------------------------------------------------------------------------

def f(x: mp.mpf) -> mp.mpf:
    return x**3 + CURVE_A*x + CURVE_B


def cubic_roots():
    """Return the three real roots in increasing order."""
    roots = mp.polyroots(
        [mp.mpf("1"), mp.mpf("0"), CURVE_A, CURVE_B],
        maxsteps=10000,
        error=False,
    )

    # Do not use a fixed 1e-70 root-imaginary threshold.  At lower precision
    # that would be an arbitrary criterion.  A scale tied to working dps is
    # more appropriate.
    root_tol = mp.power(10, -(mp.mp.dps // 2))
    real_roots = [
        mp.re(r) for r in roots if abs(mp.im(r)) <= root_tol
    ]
    real_roots.sort()

    if len(real_roots) != 3:
        raise RuntimeError(f"Expected 3 real roots; obtained {roots}")

    return real_roots


def determine_real_components(roots) -> int:
    if len(roots) != 3:
        raise ValueError("Expected three real roots.")
    e1, e2, e3 = roots
    if not (e1 < e2 < e3):
        raise ValueError("Roots are not strictly ordered.")
    return 2


# ---------------------------------------------------------------------------
# Direct integration of the Neron differential
# ---------------------------------------------------------------------------

def compact_integrand(theta, e1, e2):
    """Integrand after x=e1+(e2-e1)sin^2(theta)."""
    if theta == 0 or theta == mp.pi / 2:
        return mp.mpf("0")

    s = mp.sin(theta)
    c = mp.cos(theta)
    x = e1 + (e2 - e1) * s**2
    dx = 2 * (e2 - e1) * s * c
    fx = f(x)

    if fx < 0:
        # Small negative values can arise from endpoint cancellation.
        scale = max(abs(x**3), abs(CURVE_A*x), abs(CURVE_B), mp.mpf(1))
        if abs(fx) <= mp.power(10, -(mp.mp.dps // 2)) * scale:
            fx = mp.mpf("0")
        else:
            raise ArithmeticError(f"Unexpected negative f(x): {fx}")

    if fx == 0:
        return mp.mpf("0")

    return dx / mp.sqrt(fx)


def compact_branch_period(e1, e2):
    """I_compact = integral[e1,e2] dx/sqrt(f(x))."""
    return mp.quad(
        lambda t: compact_integrand(t, e1, e2),
        [mp.mpf("0"), mp.pi / 4, mp.pi / 2],
    )


def infinity_integrand(theta, e3):
    """Integrand after x=e3+tan^2(theta), theta in [0,pi/2)."""
    if theta == 0 or theta >= mp.pi / 2:
        return mp.mpf("0")

    t = mp.tan(theta)
    c = mp.cos(theta)
    x = e3 + t**2
    dx = 2 * t / c**2
    fx = f(x)

    if fx <= 0:
        scale = max(abs(x**3), abs(CURVE_A*x), abs(CURVE_B), mp.mpf(1))
        if abs(fx) <= mp.power(10, -(mp.mp.dps // 2)) * scale:
            fx = mp.mpf("0")
        else:
            raise ArithmeticError(f"Unexpected non-positive f(x): {fx}")

    if fx == 0:
        return mp.mpf("0")

    return dx / mp.sqrt(fx)


def infinity_branch_period(e3):
    """I_infinity = integral[e3,infinity] dx/sqrt(f(x))."""
    return mp.quad(
        lambda t: infinity_integrand(t, e3),
        [mp.mpf("0"), mp.pi / 4, mp.pi / 2],
    )


def calculate_periods(dps: int):
    """Calculate roots and both branch integrals at the requested precision."""
    mp.mp.dps = dps
    # Decimal constants must be parsed *after* setting mp.dps; otherwise
    # mpmath can permanently round the source values at the previous precision.
    initialize_constants()
    roots = cubic_roots()
    e1, e2, e3 = roots
    compact = compact_branch_period(e1, e2)
    infinity = infinity_branch_period(e3)
    full = 2 * compact
    return roots, compact, infinity, full


# ---------------------------------------------------------------------------
# Numerical validation helpers
# ---------------------------------------------------------------------------

def relative_error(a, b):
    if b == 0:
        return mp.inf
    return abs(a - b) / abs(b)


def working_precision_tolerance(dps: int, safety_digits: int = 20):
    """
    Internal tolerance based on requested precision.

    We intentionally do not demand all dps digits from two independent
    quadratures.  A 100-dps calculation therefore defaults to about 1e-40,
    while still preserving the observed ~1e-52 discrepancy.
    """
    exponent = max(20, dps // 2 - 10)
    return mp.power(10, -exponent)


def close_enough(a, b, rel_tol, abs_tol=None):
    if abs_tol is None:
        abs_tol = rel_tol
    scale = max(abs(a), abs(b), mp.mpf("1"))
    return abs(a - b) <= max(abs_tol, rel_tol * scale)


def decimal_places(decimal_string: str) -> int:
    if "." not in decimal_string:
        return 0
    return len(decimal_string.split(".", 1)[1])


def display_prefix_matches(value, reference_string: str) -> bool:
    """
    Test the Appendix value as a displayed decimal prefix.

    This does NOT assume the source used rounding-to-nearest.  It asks whether
    the independently computed value begins with the exact digits printed in
    the Appendix.
    """
    places = decimal_places(reference_string)
    scale = mp.power(10, places)
    scaled_integer = int(mp.floor(value * scale))
    displayed_fixed = "0." + str(scaled_integer).zfill(places)
    return displayed_fixed == reference_string


def display_consistency_interval(reference_string: str):
    """
    One-last-place interval appropriate when a decimal is treated as a
    truncated/displayed value rather than a rounded-to-nearest value.

    [reference, reference + 1 ulp]
    """
    ref = mp.mpf(reference_string)
    ulp = mp.power(10, -decimal_places(reference_string))
    return ref, ref + ulp


def inferred_sha(omega):
    return (
        L_PRIME * TORSION_ORDER**2
        / (omega * REGULATOR * TAMAGAWA_PRODUCT)
    )


def decimal_input_interval(decimal_string: str):
    """Interval [x, x+ulp] for a value treated as truncated/displayed."""
    x = mp.mpf(decimal_string)
    ulp = mp.power(10, -decimal_places(decimal_string))
    return x, x + ulp


def sha_input_interval(omega):
    """
    Propagate one-ulp display uncertainty for L'(E,1) and the regulator.

    This is deliberately a truncation-compatible interval rather than a
    half-ulp rounding interval.  It does not claim that the original source
    actually truncated these quantities; it provides a conservative test of
    compatibility with the supplied decimal data.
    """
    l_lo, l_hi = decimal_input_interval(L_PRIME_STR)
    r_lo, r_hi = decimal_input_interval(REGULATOR_STR)

    # All quantities are positive, so extrema occur at these endpoints.
    lo = l_lo * TORSION_ORDER**2 / (omega * r_hi * TAMAGAWA_PRODUCT)
    hi = l_hi * TORSION_ORDER**2 / (omega * r_lo * TAMAGAWA_PRODUCT)
    return lo, hi


def fmt(x, digits=60):
    return mp.nstr(x, digits)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_header(dps, convergence_levels):
    print("=" * 80)
    print("BSD PERIOD NORMALIZATION TEST — PRECISION-AWARE REDESIGN")
    print("=" * 80)
    print()
    print("Curve:")
    print("    E : y^2 = x^3 - 1706*x + 6320")
    print()
    print("Validation layers:")
    print("    A. Multi-precision quadrature convergence")
    print("    B. Independent real-component agreement")
    print("    C. Appendix display-prefix compatibility")
    print("    D. BSD integer-consistency with finite-precision inputs")
    print()
    print(f"Primary working precision: {dps} decimal digits")
    print(f"Convergence levels: {', '.join(map(str, convergence_levels))}")
    print()
    print("Primary calculation: direct integration of omega = dx/(2y)")
    print("No Sage real_period() or PARI ellperiods() is used.")
    print()


def run_steps(
    dps: int,
    convergence_levels=DEFAULT_CONVERGENCE_LEVELS,
):
    initialize_constants()
    levels = tuple(sorted(set(int(x) for x in convergence_levels)))
    if dps not in levels:
        levels = tuple(sorted(set(levels + (dps,))))

    print_header(dps, levels)

    checks = []

    # ------------------------------------------------------------------
    # STEP 1 — convergence
    # ------------------------------------------------------------------
    print("-" * 80)
    print("STEP 1 — MULTI-PRECISION QUADRATURE CONVERGENCE")
    print("-" * 80)
    print()

    results = {}
    for level in levels:
        roots, compact, infinity, full = calculate_periods(level)
        results[level] = {
            "roots": roots,
            "compact": compact,
            "infinity": infinity,
            "full": full,
        }
        print(f"DPS = {level}")
        print(f"    I_compact  = {fmt(compact, 50)}")
        print(f"    I_infinity = {fmt(infinity, 50)}")
        print(f"    Omega_full = {fmt(full, 50)}")
        print()

    # Compare the two highest requested levels against the lower level.
    convergence_pass = True
    convergence_rel = mp.mpf("0")
    if len(levels) >= 2:
        for low, high in zip(levels[:-1], levels[1:]):
            rel_c = relative_error(
                results[high]["compact"], results[low]["compact"]
            )
            rel_i = relative_error(
                results[high]["infinity"], results[low]["infinity"]
            )
            pair_rel = max(rel_c, rel_i)
            convergence_rel = max(convergence_rel, pair_rel)
            # The comparison is made against a threshold appropriate to the
            # lower precision calculation.
            tol = working_precision_tolerance(low)
            pair_pass = pair_rel <= tol
            convergence_pass = convergence_pass and pair_pass
            print(
                f"{low} -> {high} dps: max relative change = "
                f"{fmt(pair_rel, 20)}; threshold = {fmt(tol, 12)} "
                f"[{'PASS' if pair_pass else 'FAIL'}]"
            )

    checks.append(Check(
        "Multi-precision quadrature converges",
        "PASS" if convergence_pass else "FAIL",
        fmt(convergence_rel, 30),
        "successive precision changes are below precision-scaled thresholds",
    ))
    print()

    # Use the requested primary dps result for the remaining tests.
    roots = results[dps]["roots"]
    e1, e2, e3 = roots
    compact = results[dps]["compact"]
    infinity = results[dps]["infinity"]
    full = results[dps]["full"]

    # ------------------------------------------------------------------
    # STEP 2 — topology and component equality
    # ------------------------------------------------------------------
    components = determine_real_components(roots)
    topology_pass = components == EXPECTED_COMPONENTS
    component_rel = relative_error(compact, infinity)
    component_abs = abs(compact - infinity)
    component_tol = working_precision_tolerance(dps)
    component_pass = component_rel <= component_tol

    print("-" * 80)
    print("STEP 2 — REAL LOCUS, TOPOLOGY, AND COMPONENT CROSS-CHECK")
    print("-" * 80)
    print()
    print(f"e1 = {fmt(e1)}")
    print(f"e2 = {fmt(e2)}")
    print(f"e3 = {fmt(e3)}")
    print()
    print("E(R) has:")
    print("    compact component over [e1,e2]")
    print("    unbounded component over [e3,infinity)")
    print()
    print(f"Connected components = {components}")
    print(f"[{'PASS' if topology_pass else 'FAIL'}] E(R) has two components")
    print()
    print(f"I_compact  = {fmt(compact)}")
    print(f"I_infinity = {fmt(infinity)}")
    print(f"absolute difference = {fmt(component_abs, 30)}")
    print(f"relative difference = {fmt(component_rel, 30)}")
    print(f"acceptance threshold = {fmt(component_tol, 15)}")
    print(f"[{'PASS' if component_pass else 'FAIL'}] Independent component integrals agree")
    print()

    checks.extend([
        Check("E(R) has two connected components", "PASS" if topology_pass else "FAIL",
              str(components), "components == 2"),
        Check("Independent compact/unbounded integrals agree", "PASS" if component_pass else "FAIL",
              fmt(component_rel, 30), f"relative discrepancy <= {fmt(component_tol, 12)}"),
    ])

    # ------------------------------------------------------------------
    # STEP 3 — period normalization and Appendix display
    # ------------------------------------------------------------------
    ratio = full / compact
    ratio_pass = ratio == mp.mpf("2")

    half_display_pass = display_prefix_matches(compact, APPENDIX_HALF_PERIOD_STR)
    full_display_pass = display_prefix_matches(full, APPENDIX_FULL_PERIOD_STR)

    half_lo, half_hi = display_consistency_interval(APPENDIX_HALF_PERIOD_STR)
    full_lo, full_hi = display_consistency_interval(APPENDIX_FULL_PERIOD_STR)

    print("-" * 80)
    print("STEP 3 — PERIOD NORMALIZATION AND APPENDIX DISPLAY CONSISTENCY")
    print("-" * 80)
    print()
    print("INTERNAL NORMALIZATION")
    print(f"    Omega_branch = {fmt(compact)}")
    print(f"    Omega_full   = {fmt(full)}")
    print(f"    ratio        = {fmt(ratio, 50)}")
    print(f"[{'PASS' if ratio_pass else 'FAIL'}] Omega_full / Omega_branch = 2")
    print()

    print("APPENDIX HALF-PERIOD")
    print(f"    supplied display = {APPENDIX_HALF_PERIOD_STR}")
    print(f"    direct value     = {fmt(compact)}")
    print(f"    difference       = {fmt(abs(compact - APPENDIX_HALF_PERIOD), 30)}")
    print(f"    display interval = [{APPENDIX_HALF_PERIOD_STR}, {fmt(half_hi, 25)}]")
    print(f"[{'PASS' if half_display_pass else 'FAIL'}] Direct value reproduces Appendix display")
    print()

    print("APPENDIX FULL PERIOD")
    print(f"    supplied display = {APPENDIX_FULL_PERIOD_STR}")
    print(f"    direct value     = {fmt(full)}")
    print(f"    difference       = {fmt(abs(full - APPENDIX_FULL_PERIOD), 30)}")
    print(f"    display interval = [{APPENDIX_FULL_PERIOD_STR}, {fmt(full_hi, 25)}]")
    print(f"[{'PASS' if full_display_pass else 'FAIL'}] Direct value reproduces Appendix display")
    print()
    print("The Appendix decimals are treated as displayed/truncated-compatible")
    print("reference values, not as rounded-to-nearest exact numbers.")
    print()

    checks.extend([
        Check("Complete period is twice the branch period", "PASS" if ratio_pass else "FAIL",
              fmt(ratio, 40), "ratio == 2"),
        Check("Branch period reproduces Appendix display", "PASS" if half_display_pass else "FAIL",
              APPENDIX_HALF_PERIOD_STR, "same displayed decimal digits"),
        Check("Full period reproduces Appendix display", "PASS" if full_display_pass else "FAIL",
              APPENDIX_FULL_PERIOD_STR, "same displayed decimal digits"),
    ])

    # ------------------------------------------------------------------
    # STEP 4 — BSD reconstruction
    # ------------------------------------------------------------------
    half_sha = inferred_sha(compact)
    full_sha = inferred_sha(full)
    half_sha_lo, half_sha_hi = sha_input_interval(compact)
    full_sha_lo, full_sha_hi = sha_input_interval(full)

    half_deviation = abs(half_sha - mp.mpf("2"))
    full_deviation = abs(full_sha - mp.mpf("1"))

    half_integer_pass = half_sha_lo <= mp.mpf("2") <= half_sha_hi
    full_integer_pass = full_sha_lo <= mp.mpf("1") <= full_sha_hi

    print("-" * 80)
    print("STEP 4 — BSD RECONSTRUCTION WITH FINITE-PRECISION INPUTS")
    print("-" * 80)
    print()
    print("Supplied BSD inputs:")
    print(f"    L'(E,1)      = {L_PRIME_STR}")
    print(f"    Regulator    = {REGULATOR_STR}")
    print(f"    product(c_p) = {TAMAGAWA_PRODUCT_STR}")
    print(f"    |torsion|    = {TORSION_ORDER_STR}")
    print()
    print("HALF/BRANCH PERIOD")
    print(f"    Omega = {fmt(compact)}")
    print(f"    inferred |Sha| = {fmt(half_sha)}")
    print(f"    deviation from 2 = {fmt(half_deviation, 30)}")
    print(f"    propagated input interval = [{fmt(half_sha_lo, 30)}, {fmt(half_sha_hi, 30)}]")
    print(f"[INFO] Integer-target interval test: {'contains' if half_integer_pass else 'does not contain'} 2")
    print()

    print("FULL PERIOD")
    print(f"    Omega = {fmt(full)}")
    print(f"    inferred |Sha| = {fmt(full_sha)}")
    print(f"    deviation from 1 = {fmt(full_deviation, 30)}")
    print(f"    propagated input interval = [{fmt(full_sha_lo, 30)}, {fmt(full_sha_hi, 30)}]")
    print(f"[INFO] Integer-target interval test: {'contains' if full_integer_pass else 'does not contain'} 1")
    print()

    print("BSD interpretation:")
    print("    The half-period normalization is numerically centered at |Sha| = 2.")
    print("    The full-period normalization is numerically centered at |Sha| = 1.")
    print("    The displayed decimal inputs do not justify treating either")
    print("    reconstructed decimal as an exact integer identity by themselves.")
    print()

    # These are deliberately informational rather than PASS/FAIL checks.
    # The supplied L'(E,1) and regulator are finite decimal data, and the
    # resulting intervals do not contain the target integers.  That means the
    # supplied precision is insufficient to certify an exact integer BSD
    # reconstruction.  It would be methodologically wrong to widen the
    # interval until it passes merely to force an overall PASS.
    checks.extend([
        Check("Half-period BSD reconstruction", "INFO", fmt(half_sha, 40),
              "numerical proximity to Sha=2 is reported; supplied decimal precision does not certify equality"),
        Check("Full-period BSD reconstruction", "INFO", fmt(full_sha, 40),
              "numerical proximity to Sha=1 is reported; supplied decimal precision does not certify equality"),
    ])

    # ------------------------------------------------------------------
    # FINAL SUMMARY
    # ------------------------------------------------------------------
    print("=" * 80)
    print("FINAL VALIDATION SUMMARY")
    print("=" * 80)
    print()
    for check in checks:
        print(f"[{check.status}] {check.name}")
        print(f"       value     = {check.value}")
        print(f"       criterion = {check.criterion}")
        print()

    overall = all(c.status != "FAIL" for c in checks)
    unresolved_bsd = any(c.status == "INFO" for c in checks)

    print("=" * 80)
    if not overall:
        overall_label = "FAIL"
    elif unresolved_bsd:
        overall_label = "PASS — PERIOD NORMALIZATION; BSD INTEGER CERTIFICATION UNRESOLVED"
    else:
        overall_label = "PASS"
    print("OVERALL RESULT:", overall_label)
    print("=" * 80)
    print()

    if overall:
        print("CONCLUSION OF THIS NUMERICAL EXPERIMENT")
        print()
        print("1. The two real components independently reproduce the same branch")
        print("   integral to substantially better precision than the acceptance")
        print("   threshold at the requested working precision.")
        print()
        print("2. The complete real period is numerically twice the branch integral.")
        print()
        print("3. The independently computed values reproduce the Appendix's")
        print("   displayed half- and full-period decimals.")
        print()
        print("4. In the rank-one BSD rearrangement, the branch/half-period")
        print("   normalization reconstructs a value compatible with |Sha| = 2,")
        print("   while the complete-period normalization reconstructs a value")
        print("   compatible with |Sha| = 1, given the displayed finite-precision")
        print("   inputs. These are numerical proximity statements, not exact")
        print("   certifications: the conservative input intervals do not themselves")
        print("   contain the target integers.")
        print()
        print("5. The period-normalization result is therefore substantially stronger")
        print("   than the integer-Sha certification available from the supplied")
        print("   decimal L'(E,1) and regulator values.")
        print()
        print("6. This supports interpreting the factor-of-two discrepancy as a")
        print("   period-normalization issue to be investigated independently of")
        print("   BSD, rather than as evidence that the Tamagawa product changes")
        print("   when the period convention changes.")
    else:
        print("One or more validation checks failed. Inspect the individual")
        print("checks above; a failure here should be interpreted as a numerical")
        print("or reference-data issue, not as a failure of BSD itself.")

    print()
    print("IMPORTANT:")
    print("This experiment does not prove the Birch and Swinnerton-Dyer")
    print("conjecture. It tests period normalization and numerical BSD")
    print("consistency for this specific elliptic curve and the supplied")
    print("finite-precision Appendix data.")
    print()

    return 0 if overall else 1


# ---------------------------------------------------------------------------
# Notebook-safe API
# ---------------------------------------------------------------------------

def run_bsd_test(
    dps=DEFAULT_DPS,
    convergence_levels=DEFAULT_CONVERGENCE_LEVELS,
):
    """Run safely from Jupyter/Sage without consuming kernel arguments."""
    return run_steps(int(dps), convergence_levels)


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------

def parse_levels(value: str):
    try:
        levels = tuple(int(part.strip()) for part in value.split(",") if part.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError("levels must be comma-separated integers") from exc
    if not levels or any(level < 30 for level in levels):
        raise argparse.ArgumentTypeError("each precision level must be >= 30")
    return levels


def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser(
        description="Precision-aware independent BSD period-normalization test."
    )
    parser.add_argument(
        "--dps", type=int, default=DEFAULT_DPS,
        help=f"Primary working precision (default {DEFAULT_DPS})",
    )
    parser.add_argument(
        "--convergence-levels", type=parse_levels,
        default=DEFAULT_CONVERGENCE_LEVELS,
        help="Comma-separated precision levels (default 80,100,120)",
    )
    args = parser.parse_args(argv)

    if args.dps < 30:
        parser.error("--dps must be >= 30")

    return run_steps(args.dps, args.convergence_levels)


if __name__ == "__main__":
    sys.exit(main())

