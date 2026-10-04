            records.append(result)


    with enriched_path.open(
        "w",
        encoding="utf-8",
    ) as output_file:


        for record in records:
            output_file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )


    return enriched_path




# ============================================================
# Synthesis
# ============================================================


def load_jsonl(path: Path):
    """Load a JSONL file into a list."""


    records = []


    with path.open(
        "r",
        encoding="utf-8",
    ) as f:


        for line in f:
            line = line.strip()


            if line:
                records.append(
                    json.loads(line)
                )


    return records




def synthesize(
    model: str,
    evidence,
