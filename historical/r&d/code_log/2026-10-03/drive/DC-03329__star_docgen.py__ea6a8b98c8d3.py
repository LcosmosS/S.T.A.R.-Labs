    print()
    print("Loading evidence...")
    print()


    evidence = load_jsonl(evidence_path)


    if not evidence:
        print("ERROR: Evidence index is empty.")
        return 2


    print(
        f"Loaded {len(evidence)} evidence records."
    )


    print()
    print("Checking Ollama...")
    print()


    if not ollama_available():
        print(
            f"ERROR: Ollama is not reachable at "
            f"{OLLAMA_URL}"
