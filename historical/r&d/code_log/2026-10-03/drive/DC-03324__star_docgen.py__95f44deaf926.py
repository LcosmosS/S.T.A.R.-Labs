    if not check_model(model):
        raise RuntimeError(
            f"Ollama model '{model}' is not installed."
        )


    print(
        f"Using Ollama model: {model}"
    )
    print()


    records = []


    with evidence_path.open(
        "r",
        encoding="utf-8",
    ) as source:


        for line_number, line in enumerate(
            source,
