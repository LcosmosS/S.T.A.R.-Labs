# Save this as parse_cremona_chunks.py in your repo and run it on the host. 
#It reads cremona_db_copy/cremona/curvedata/* (or curvedata.gz) and writes cremona_raw_parsed.csv with parsed fields and the raw line.
# python3 parse_cremona_chunks.py

# parse_cremona_chunks.py
import os, gzip, csv, re, sys

CREM = "cremona_db_copy/cremona"
OUT = "cremona_raw_parsed.csv"

def iter_files():
    gz = os.path.join(CREM, "curvedata.gz")
    if os.path.isfile(gz):
        yield gz
        return
    d = os.path.join(CREM, "curvedata")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.startswith("curvedata."):
                yield os.path.join(d, fn)
        return
    top = os.path.join(CREM, "curvedata")
    if os.path.isfile(top):
        yield top

label_re = re.compile(r"^\s*([0-9]+[a-z]\d+)\b", re.I)
ainv_re = re.compile(r"\[(-?\d+(?:,\s*-?\d+)*)\]")
j_re = re.compile(r"j[_ ]?invariant[:=]?\s*([0-9Ee\+\-\.]+)|j\s*=\s*([0-9Ee\+\-\.]+)")
disc_re = re.compile(r"discriminant[:=]?\s*(-?\d+)|disc[:=]?\s*(-?\d+)")
cond_from_label = re.compile(r"^([0-9]+)")

with open(OUT, "w", newline="", encoding="utf-8") as outf:
    writer = csv.writer(outf)
    writer.writerow(["label","conductor","a_invariants_raw","j_raw","discriminant_raw","raw_line"])
    for path in iter_files():
        print("Reading", path, file=sys.stderr)
        opener = gzip.open if path.endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
            for ln in fh:
                ln = ln.rstrip("\n")
                if not ln:
                    continue
                label = ""
                m = label_re.match(ln)
                if m:
                    label = m.group(1)
                else:
                    parts = ln.split()
                    if parts:
                        label = parts[0]
                cond = ""
                m2 = cond_from_label.match(label)
                if m2:
                    cond = m2.group(1)
                else:
                    toks = ln.split()
                    if len(toks) > 1 and toks[1].isdigit():
                        cond = toks[1]
                ainv = None
                m3 = ainv_re.search(ln)
                if m3:
                    ainv = "[" + m3.group(1) + "]"
                jv = None
                m4 = j_re.search(ln)
                if m4:
                    jv = m4.group(1) or m4.group(2)
                disc = None
                m5 = disc_re.search(ln)
                if m5:
                    disc = m5.group(1) or m5.group(2)
                writer.writerow([label, cond, ainv, jv, disc, ln])
print("Wrote", OUT)
