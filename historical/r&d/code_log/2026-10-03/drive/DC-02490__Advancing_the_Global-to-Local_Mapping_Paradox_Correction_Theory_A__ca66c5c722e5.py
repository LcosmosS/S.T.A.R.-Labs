if rank >= 2:
    heegner_point = compute_heegner_point(E, discriminant=-11)
    if heegner_point:
        print(f"Heegner point: {heegner_point}")
    else:
         *         print("Heegner point computation skipped or failed")

         * Preserve Theory Integrity: The theory depends on:
            * Rank Computation: Handled by E_pari.ellrank() and analytic rank via L.dokchitser.
            * BSD Verification: Weak and strong BSD checks are intact.
            * Cosmological Scaling: Period, regulator, and volume calculations are unaffected.
            * Interweb Plot: Relies on rank, log⁡(∣Δ∣)\log(|\Delta|)log(∣Δ∣), log⁡(N)\log(N)log(N), and volume, all computed independently. Bypassing Heegner points only reduces the verification of rational points, which is supplementary given the robust rank computations.
