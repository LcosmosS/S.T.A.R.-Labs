    except Exception as exc:
        print()
        print("ERROR during synthesis:")
        print(exc)
        return 1


    output_path = output / "synthesized_paper.md"


    output_path.write_text(
        paper,
        encoding="utf-8",
    )


    print()
    print("Synthesis complete.")
    print()
    print(f"Paper:")
    print(f"  {output_path}")
    print()


    return 0




# ============================================================
# Main
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description=(
            "S.T.A.R. Document Ingestion / "
            "Provenance Generator v0.1"
