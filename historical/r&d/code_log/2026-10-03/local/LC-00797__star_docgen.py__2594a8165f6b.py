#!/usr/bin/env python3

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pymupdf
import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

DEFAULT_DOCS = [
    "Origins.pdf",
    "Research-Analysis+Testing.pdf",
    "Research-Analysis+Testing_pt2.pdf",
    "Research-Analysis+Testing_pt3.pdf",
    "Research-Analysis+Testing_pt3-25.pdf",
    "Research-Analysis+Testing_pt3-5.pdf",
    "Research-Analysis+Testing_pt3-75.pdf",
    "Research-Analysis+Testing_pt4.pdf",
    "Branch_Research-Analysis+Testing_pt4.pdf",
]


# ============================================================
# Utility functions
# ============================================================

def sha256(path: Path) -> str:
    """Return SHA-256 digest of a file."""

    h = hashlib.sha256()

    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


# ============================================================
# PDF extraction
# ============================================================

def extract_pdf_pages(path: Path):
    """
    Extract all pages from a PDF while preserving document hash
    and page-level provenance.
    """

    digest = sha256(path)

    document = pymupdf.open(path)

    try:
        for page_number, page in enumerate(document, start=1):
            yield {
                "document": path.name,
                "path": str(path),
                "sha256": digest,
                "page": page_number,
                "text": page.get_text("text"),
            }
    finally:
        document.close()


def features(text: str):
    """
    Lightweight deterministic classification of page contents.

    These features are descriptive only. They do not make
    scientific claims about the page.
    """

    return {
        "code_like": bool(
            re.search(
                r"\b("
                r"import\s+"
                r"|from\s+\S+\s+import\s+"
                r"|def\s+"
                r"|class\s+"
                r"|EllipticCurve"
                r"|pari/gp"
                r"|magma"
                r"|python"
                r"|sage"
                r")\b",
                text,
                re.IGNORECASE,
            )
        ),

        "result_like": bool(
            re.search(
                r"\b("
                r"results?"
                r"|output"
                r"|finding"
                r"|scientific finding"
                r"|null result"
                r"|R2"
                r"|MAE"
                r"|RMSE"
                r"|correlation"
                r"|accuracy"
                r"|error"
                r")\b",
                text,
                re.IGNORECASE,
            )
        ),

        "data_like": bool(
            re.search(
                r"\b("
                r"[\w.+-]+\.(?:csv|fits|parquet|json)"
                r"|dataset"
                r"|data source"
                r"|rows?"
                r"|table"
                r")\b",
                text,
                re.IGNORECASE,
            )
        ),

        "equation_like": bool(
            re.search(
                r"(=|≈|∼|\\frac|\\sum|\\prod|"
                r"\bE\s*\(|\bL\s*\(|\bH\s*\()",
                text,
            )
        ),
    }


# ============================================================
# Ollama
# ============================================================

def ollama_available() -> bool:
    """Return True if the Ollama API is reachable."""

    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=10,
        )
        response.raise_for_status()
        return True

    except requests.RequestException:
        return False


def ollama_models():
    """Return installed Ollama model names."""

    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        return [
            model.get("name")
            for model in data.get("models", [])
            if model.get("name")
        ]

    except (requests.RequestException, ValueError) as exc:
        raise RuntimeError(
            f"Unable to query Ollama at {OLLAMA_URL}: {exc}"
        ) from exc


def check_model(model: str):
    """Verify that the requested Ollama model is installed."""

    installed = ollama_models()

    if model not in installed:
        print()
        print("ERROR: Requested Ollama model is not installed.")
        print()
        print(f"Requested model: {model}")
        print()

        if installed:
            print("Installed models:")
            for name in installed:
                print(f"  {name}")
        else:
            print("No Ollama models are currently installed.")

        print()
        print(f"Install the model with:")
        print(f"  ollama pull {model}")
        print()

        return False

    return True


def ollama(model: str, prompt: str, temperature: float = 0.1) -> str:
    """
    Send a prompt to Ollama and return its generated response.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                },
            },
            timeout=600,
        )

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to Ollama at {OLLAMA_URL}: {exc}"
        ) from exc

    if not response.ok:
        raise RuntimeError(
            "Ollama returned an error:\n"
            f"HTTP {response.status_code}\n"
            f"{response.text}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"Ollama returned invalid JSON:\n{response.text[:1000]}"
        ) from exc

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

    Handles both plain JSON and JSON enclosed in Markdown fences.
    """

    raw = raw.strip()

    # Normal JSON
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Markdown fenced JSON
    fenced = re.search(
        r"```(?:json)?\s*(.*?)\s*```",
        raw,
        re.DOTALL | re.IGNORECASE,
    )

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
    """

    prompt = f"""
You are the evidence-extraction layer of a scientific archive.

Use ONLY the supplied PDF page.

Do not:
- use outside knowledge
- correct the source
- infer missing facts
- invent citations
- silently repair equations
- silently repair filenames

Return valid JSON with exactly these keys:

document
page
summary
research_questions
theoretical_claims
definitions
methods
code
data_files
datasets_or_data_sources
results
errors_or_failures
interpretations
explicit_limitations
provenance_notes

Preserve exact:
- filenames
- software versions
- numerical values
- equations
- code fragments
- parameter values
- result wording

where useful.

Mark analogies explicitly as interpretations.

If code or a result appears to continue onto another page,
state that in provenance_notes.

SOURCE DOCUMENT:
{page_record["document"]}

SOURCE PAGE:
{page_record["page"]}

SOURCE TEXT:
---
{page_record["text"]}
---
"""

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
    docs,
):
    """
    Extract deterministic PDF text and page-level provenance.

    This does NOT require Ollama.
    """

    manifest_path = output / "corpus_manifest.json"
    evidence_path = output / "page_evidence.jsonl"

    manifest = {
        "generator": "S.T.A.R. Document Generator v0.1",
        "generated_utc": utc_now(),
        "corpus": str(corpus),
        "documents": [],
    }

    total_pages = 0

    with evidence_path.open(
        "w",
        encoding="utf-8",
    ) as evidence_file:

        for document_number, pdf_path in enumerate(
            docs,
            start=1,
        ):

            print(
                f"[{document_number}/{len(docs)}] "
                f"Reading {pdf_path.name}"
            )

            digest = sha256(pdf_path)

            document_record = {
                "document": pdf_path.name,
                "path": str(pdf_path),
                "sha256": digest,
                "pages": 0,
            }

            for page_record in extract_pdf_pages(pdf_path):

                text = page_record["text"]

                record = {
                    **page_record,
                    "features": features(text),
                    "text_length": len(text),
                }

                evidence_file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

                document_record["pages"] += 1
                total_pages += 1

            manifest["documents"].append(
                document_record
            )

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
    output: Path,
):
    """
    Run Ollama against every extracted page and create a
    structured AI evidence index.
    """

    enriched_path = output / "ollama_page_evidence.jsonl"

    print()
    print("Checking Ollama...")
    print()

    if not ollama_available():
        raise RuntimeError(
            "Ollama is not reachable at "
            f"{OLLAMA_URL}"
        )

    if not check_model(model):
        raise RuntimeError(
            f"Ollama model '{model}' is not installed."
        )

    print(
        f"Using Ollama model: {model}"
    )
    print()

    records = []

    with evidence_path.open(
        "r",
        encoding="utf-8",
    ) as source:

        for line_number, line in enumerate(
            source,
            start=1,
        ):

            page_record = json.loads(line)

            print(
                f"[AI {line_number}] "
                f"{page_record['document']} "
                f"page {page_record['page']}"
            )

            result = extract_page_evidence(
                model,
                page_record,
            )

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
):
    """
    Synthesize a scientific paper from structured evidence.
    """

    data = json.dumps(
        evidence,
        ensure_ascii=False,
    )

    prompt = f"""
You are the scientific synthesis layer.

Write an extremely detailed scientific paper using ONLY
the supplied evidence records from these PDFs:

Origins.pdf
Research-Analysis+Testing.pdf
Research-Analysis+Testing_pt.2.pdf
Research-Analysis+Testing_pt.3.pdf
Branch_Rersearch-Analysis+Testing_pt.4.pdf

Do not invent or silently correct facts.

Distinguish:
- source facts
- source interpretations
- proposed methods
- computational failures
- null results
- inferences

Preserve disagreements.

Do not claim finite computational checks prove universal
mathematical conjectures.

Keep BSD-inspired analogy separate from mathematical claims
about BSD.

Every substantive corpus-derived claim must end with:

[Source: filename, p. N]

or:

[Sources: filename, pp. N-M; other.pdf, p. K]

Reproduce source code only when it is actually present.

If code is fragmented across pages, explicitly identify it
as a fragmented reconstruction.

Explicitly list every named data file and dataset.

When the corpus identifies whether something is:
- simulated
- synthetic
- observed
- derived

preserve that classification.

If the corpus does not establish something, write:

"not established by the supplied corpus."

Structure the paper as:

Title
Abstract
Provenance and Scope
Origins
Problem Formulation
Mathematical Framework
BSD Motivation
Cartographic/Cosmological Construction
Computational Program
Software
Code/Algorithms
Data and File Provenance
Experimental Design
Results
Errors and Failed Runs
Null Results/Falsification
Cross-Document Synthesis
Contradictions/Unresolved Issues
Limitations
Reproducibility
Proposed Next Experiments
Conclusion
Appendix A Code Inventory
Appendix B Data Inventory
Appendix C Page-Level Provenance

EVIDENCE:
{data}
"""

    return ollama(
        model=model,
        prompt=prompt,
        temperature=0.05,
    )


def synthesize_paper(
    evidence_path: Path,
    output: Path,
    model: str,
):
    """
    Generate the final scientific synthesis.
    """

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
        )
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
        )

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
        )
    )

    parser.add_argument(
        "--corpus",
        type=Path,
        required=True,
        help="Directory containing source PDFs",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory",
    )

    parser.add_argument(
        "--model",
        default=None,
        help="Ollama model used for synthesis",
    )

    parser.add_argument(
        "--docs",
        nargs="+",
        default=DEFAULT_DOCS,
        help=(
            "PDF filenames to process. "
            "Defaults to the five S.T.A.R. corpus documents."
        ),
    )

    parser.add_argument(
        "--extract-only",
        action="store_true",
        help=(
            "Extract and index evidence without "
            "using Ollama."
        ),
    )

    parser.add_argument(
        "--synthesize-only",
        action="store_true",
        help=(
            "Synthesize a paper from an existing "
            "evidence index."
        ),
    )

    parser.add_argument(
        "--enrich",
        action="store_true",
        help=(
            "Run Ollama page-level evidence extraction "
            "after deterministic PDF extraction."
        ),
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # Validate modes
    # --------------------------------------------------------

    selected_modes = sum(
        [
            args.extract_only,
            args.synthesize_only,
            args.enrich,
        ]
    )

    if selected_modes == 0:
        parser.error(
            "Specify --extract-only, --enrich, "
            "or --synthesize-only"
        )

    if selected_modes > 1:
        parser.error(
            "Only one operating mode may be selected "
            "at a time."
        )

    # --------------------------------------------------------
    # Normalize paths
    # --------------------------------------------------------

    args.corpus = (
        args.corpus
        .expanduser()
        .resolve()
    )

    args.output = (
        args.output
        .expanduser()
        .resolve()
    )

    args.output.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Validate corpus
    # --------------------------------------------------------

    if not args.corpus.exists():
        print()
        print(
            f"ERROR: Corpus directory does not exist:"
        )
        print(
            f"  {args.corpus}"
        )
        return 2

    if not args.corpus.is_dir():
        print()
        print(
            f"ERROR: Corpus path is not a directory:"
        )
        print(
            f"  {args.corpus}"
        )
        return 2

    paths = [
        args.corpus / filename
        for filename in args.docs
    ]

    missing = [
        path
        for path in paths
        if not path.exists()
    ]

    if missing:
        print()
        print(
            "ERROR: The following PDF files "
            "were not found:"
        )
        print()

        for path in missing:
            print(
                f"  {path}"
            )

        print()
        print(
            "Available PDFs in corpus directory:"
        )

        available = sorted(
            args.corpus.glob("*.pdf")
        )

        if available:
            for path in available:
                print(
                    f"  {path.name}"
                )
        else:
            print(
                "  <no PDFs found>"
            )

        return 2

    # --------------------------------------------------------
    # Extraction mode
    # --------------------------------------------------------

    if args.extract_only:

        print()
        print(
            "S.T.A.R. Document Generator v0.1"
        )
        print(
            "================================"
        )
        print(
            "Mode: PDF extraction / provenance indexing"
        )
        print(
            f"Corpus: {args.corpus}"
        )
        print(
            f"Output: {args.output}"
        )
        print(
            f"Documents: {len(paths)}"
        )
        print()

        manifest_path, evidence_path = (
            extract_corpus(
                args.corpus,
                args.output,
                paths,
            )
        )

        print()
        print(
            "Extraction complete."
        )
        print()
        print(
            f"Manifest:"
        )
        print(
            f"  {manifest_path}"
        )
        print()
        print(
            f"Evidence index:"
        )
        print(
            f"  {evidence_path}"
        )
        print()

        return 0

    # --------------------------------------------------------
    # Ollama enrichment
    # --------------------------------------------------------

    if args.enrich:

        if not args.model:
            print()
            print(
                "ERROR: --model is required for "
                "Ollama enrichment."
            )
            print()
            print(
                "Example:"
            )
            print(
                "  --model llama3"
            )
            print()

            return 2

        if not check_model(args.model):
            return 2

        evidence_path = (
            args.output /
            "page_evidence.jsonl"
        )

        if not evidence_path.exists():

            print()
            print(
                "ERROR: Evidence index does not exist:"
            )
            print(
                f"  {evidence_path}"
            )
            print()
            print(
                "Run --extract-only first."
            )
            print()

            return 2

        try:
            enriched_path = enrich_evidence(
                args.model,
                evidence_path,
                args.output,
            )

        except Exception as exc:
            print()
            print(
                "ERROR during Ollama enrichment:"
            )
            print(exc)
            return 1

        print()
        print(
            "Ollama enrichment complete."
        )
        print()
        print(
            f"Output:"
        )
        print(
            f"  {enriched_path}"
        )
        print()

        return 0

    # --------------------------------------------------------
    # Synthesis mode
    # --------------------------------------------------------

    if args.synthesize_only:

        if not args.model:
            print()
            print(
                "ERROR: --model is required "
                "for synthesis."
            )
            print()
            print(
                "Example:"
            )
            print(
                "  --model llama3"
            )
            print()

            return 2

        if args.model.upper() == "YOUR_MODEL":
            print()
            print(
                "ERROR: Replace YOUR_MODEL with "
                "an installed Ollama model."
            )
            print()

            return 2

        evidence_path = (
            args.output /
            "page_evidence.jsonl"
        )

        if not evidence_path.exists():
            print()
            print(
                "ERROR: Evidence index does not exist:"
            )
            print(
                f"  {evidence_path}"
            )
            print()
            print(
                "Run --extract-only first."
            )
            print()

            return 2

        return synthesize_paper(
            evidence_path,
            args.output,
            args.model,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())