    return ollama(
        model=model,
        prompt=prompt,
        temperature=0.05,
    )




def synthesize_paper(
    evidence_path: Path,
    output: Path,
