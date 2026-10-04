    raw = ollama(
        model=model,
        prompt=prompt,
        temperature=0.1,
    )


    try:
        result = parse_model_json(raw)


    except ValueError:
        result = {
            "document": page_record["document"],
            "page": page_record["page"],
            "parse_error": True,
            "raw_model_output": raw,
        }


    return result




# ============================================================
# Extraction mode
# ============================================================


def extract_corpus(
    corpus: Path,
    output: Path,
