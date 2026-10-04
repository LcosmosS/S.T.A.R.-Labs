        if not evidence_path.exists():
            print()
            print(
                "ERROR: Evidence index does not exist:"
            )
            print(
                f"  {evidence_path}"
            )
            print()
            print(
                "Run --extract-only first."
            )
            print()


            return 2


        return synthesize_paper(
            evidence_path,
            args.output,
