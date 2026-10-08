import os
import re
import sys 

# Path to repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ECDATA_ROOT = os.path.join(REPO_ROOT, "data", "ecdata")

LABEL_RE = re.compile(r"(\d+)([a-z]+)(\d+)$")


def extract_labels_from_ecdata():
    """
    Walk data/ecdata/<N>/<iso>/<label>
    and collect all valid Cremona labels.
    """
    labels = []

    # Check if directory exists and has content
    if not os.path.isdir(ECDATA_ROOT):
        print(f"ERROR: ECDATA_ROOT not found at: {ECDATA_ROOT}", file=sys.stderr)
        return labels
    
    try:
        for N in sorted(
            os.listdir(ECDATA_ROOT), key=lambda x: int(x) if x.isdigit() else float('inf')
        ):
            N_path = os.path.join(ECDATA_ROOT, N)
            if not os.path.isdir(N_path):
                continue

            for iso in sorted(os.listdir(N_path)):
                iso_path = os.path.join(N_path, iso)
                if not os.path.isdir(iso_path):
                    continue

                for fname in sorted(os.listdir(iso_path)):
                    # Expect filenames like "11a1", "37b2", etc.
                    if LABEL_RE.match(fname):
                        labels.append(fname)
    except Exception as e:
        print(f"ERROR: Failed to extract labels from ecdata: {e}", file=sys.stderr)
        return []

    return labels


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Cremona subset')
    parser.add_argument('--max-labels', type=int, default=1000, help='Maximum number of labels to generate')
    args = parser.parse_args()
    
    labels = extract_labels_from_ecdata()
    
    if not labels:
        print("ERROR: No labels found in ecdata directory", file=sys.stderr)
        print(f"Checked path: {ECDATA_ROOT}", file=sys.stderr)
        print(f"Path exists: {os.path.exists(ECDATA_ROOT)}", file=sys.stderr)
        print(f"Is directory: {os.path.isdir(ECDATA_ROOT)}", file=sys.stderr)
        if os.path.isdir(ECDATA_ROOT):
            try:
                print(f"Contents: {os.listdir(ECDATA_ROOT)}", file=sys.stderr)
            except Exception as e:
                print(f"Error listing contents: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Sort lexicographically for reproducibility
    labels = sorted(labels)
    
    # Print first N labels (default 1000)
    for L in labels[:args.max_labels]:
        print(L)


if __name__ == "__main__":
    main()
