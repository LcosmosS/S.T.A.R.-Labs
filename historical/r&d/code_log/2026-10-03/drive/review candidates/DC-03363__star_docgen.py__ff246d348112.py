        print()


        for path in missing:
            print(
                f"  {path}"
            )


        print()
        print(
            "Available PDFs in corpus directory:"
        )


        available = sorted(
            args.corpus.glob("*.pdf")
        )


        if available:
            for path in available:
                print(
                    f"  {path.name}"
                )
        else:
            print(
                "  <no PDFs found>"
            )


        return 2


    # --------------------------------------------------------
    # Extraction mode
    # --------------------------------------------------------


    if args.extract_only:


        print()
        print(
            "S.T.A.R. Document Generator v0.1"
        )
        print(
            "================================"
        )
        print(
            "Mode: PDF extraction / provenance indexing"
        )
        print(
            f"Corpus: {args.corpus}"
        )
        print(
            f"Output: {args.output}"
        )
        print(
            f"Documents: {len(paths)}"
        )
        print()


        manifest_path, evidence_path = (
            extract_corpus(
                args.corpus,
