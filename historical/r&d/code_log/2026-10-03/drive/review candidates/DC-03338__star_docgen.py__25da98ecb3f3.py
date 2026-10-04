    if "error" in data:
        raise RuntimeError(
            f"Ollama error: {data['error']}"
        )


    if "response" not in data:
        raise RuntimeError(
            "Ollama response did not contain a 'response' field."
        )


    return data["response"]




# ============================================================
# JSON handling
# ============================================================


def parse_model_json(raw: str):
    """
    Parse JSON returned by the model.
