    args.corpus = (
        args.corpus
        .expanduser()
        .resolve()
    )


    args.output = (
        args.output
        .expanduser()
        .resolve()
    )


    args.output.mkdir(
        parents=True,
        exist_ok=True,
    )


    # --------------------------------------------------------
    # Validate corpus
    # --------------------------------------------------------


    if not args.corpus.exists():
        print()
        print(
            f"ERROR: Corpus directory does not exist:"
        )
        print(
            f"  {args.corpus}"
        )
        return 2


    if not args.corpus.is_dir():
        print()
        print(
            f"ERROR: Corpus path is not a directory:"
        )
        print(
            f"  {args.corpus}"
        )
        return 2


    paths = [
        args.corpus / filename
        for filename in args.docs
    ]


    missing = [
        path
        for path in paths
