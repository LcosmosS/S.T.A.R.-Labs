import os
import re

# Path to repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CURVEDATA_DIR = os.path.join(REPO_ROOT, "data", "ecdata", "curvedata")

LABEL_RE = re.compile(r"(\d+)([a-z]+)(\d+)$")


def extract_labels_from_chunks():
    """
    Parse data/ecdata/curvedata/curvedata.*
    and extract Cremona labels from each line.
    """
    labels = []

    for fname in sorted(os.listdir(CURVEDATA_DIR)):
        if not fname.startswith("curvedata."):
            continue

        path = os.path.join(CURVEDATA_DIR, fname)
        with open(path) as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                label = parts[0]
                if LABEL_RE.match(label):
                    labels.append(label)

    return labels


def main():
    labels = extract_labels_from_chunks()

    # Sort lexicographically for reproducibility
    labels = sorted(labels)

    # Print first 1000 labels
    for L in labels[:1000]:
        print(L)


if __name__ == "__main__":
    main()
