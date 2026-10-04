try:
    from src.tda.witness_complex import WitnessComplex
    from src.tda.symbolic_persistence import SymbolicPersistence

    WC = WitnessComplex(num_landmarks=30)
    L = WC.select_landmarks(X)
    W = WC.assign_witnesses(X, L)
    complex_data = WC.build_complex(X)

    SP = SymbolicPersistence(maxdim=1)
    diagrams = SP.barcodes(X)

    print("Computed witness complex and barcodes using src.tda")

except Exception as e:
    print("TDA modules not available; using ripser fallback if installed.", e)

    try:
        from ripser import ripser
        diagrams = ripser(X, maxdim=1)['dgms']
    except Exception as e2:
        print("ripser not available; skipping barcodes.", e2)
        diagrams = None
