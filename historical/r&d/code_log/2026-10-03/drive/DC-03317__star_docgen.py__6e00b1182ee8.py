    if fenced:
        candidate = fenced.group(1).strip()


        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass


    raise ValueError("Model output was not valid JSON.")




# ============================================================
# Evidence extraction
# ============================================================


def extract_page_evidence(model: str, page_record: dict):
    """
    Ask Ollama to extract structured evidence from one page.
