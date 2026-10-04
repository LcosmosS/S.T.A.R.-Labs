    manifest["total_pages"] = total_pages


    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


    return manifest_path, evidence_path




# ============================================================
# Ollama evidence enrichment
# ============================================================


def enrich_evidence(
    model: str,
    evidence_path: Path,
