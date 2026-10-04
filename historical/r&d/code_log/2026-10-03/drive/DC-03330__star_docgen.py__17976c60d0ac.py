        return 2


    if not check_model(model):
        return 2


    print()
    print(
        f"Synthesizing using model: {model}"
    )
    print()


    try:
        paper = synthesize(
            model,
            evidence,
