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
