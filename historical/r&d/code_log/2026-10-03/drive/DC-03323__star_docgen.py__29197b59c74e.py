    enriched_path = output / "ollama_page_evidence.jsonl"


    print()
    print("Checking Ollama...")
    print()


    if not ollama_available():
        raise RuntimeError(
            "Ollama is not reachable at "
            f"{OLLAMA_URL}"
