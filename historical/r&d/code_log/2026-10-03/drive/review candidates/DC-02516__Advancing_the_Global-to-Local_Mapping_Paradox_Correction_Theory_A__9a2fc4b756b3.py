if rank >= 2:
    heegner_point = compute_heegner_point(E, discriminant=-11)
    if heegner_point:
        print(f"Heegner point: {heegner_point}")
    else:
         *         print("Heegner point computation skipped or failed")

         * Preserve Theory Integrity: The theory depends on:
            * Rank Computation: Handled by E_pari.ellrank() and analytic rank via L.dokchitser.
