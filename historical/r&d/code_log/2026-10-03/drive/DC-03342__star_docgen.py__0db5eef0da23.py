        print()
        print(
            "Extraction complete."
        )
        print()
        print(
            f"Manifest:"
        )
        print(
            f"  {manifest_path}"
        )
        print()
        print(
            f"Evidence index:"
        )
        print(
            f"  {evidence_path}"
        )
        print()


        return 0


    # --------------------------------------------------------
    # Ollama enrichment
    # --------------------------------------------------------


    if args.enrich:


        if not args.model:
            print()
            print(
                "ERROR: --model is required for "
                "Ollama enrichment."
