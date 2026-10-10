"""Reference checks only: never evaluate the actual cohort's graph or endpoint.

Run from the repository root with ``python -m research.independent_review...``
via runpy (see the accompanying report). This is an off-path verification
implementation, not off-author scientific approval or an activation tool.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from contextlib import ExitStack
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import subprocess
from unittest.mock import patch

import numpy as np
import pandas as pd
import sympy as sp

from src.control.execution import PreflightError, preflight_controlled_experiment
from src.control.registry import RegistrySnapshot
from src.experiments import exp_map_a03 as production
from src.experiments.exp_map_a01 import SplitMix64, _discriminant

ROOT = Path(__file__).resolve().parents[3]
SOURCE = "data/ecdata/allcurves/allcurves.00000-09999"
SPEC = "controlled_execution/specs/EXP-MAP-A03.json"
CONFIG = "preregistrations/EXP-MAP-A03/config.json"
SOURCE_SHA = "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968"
SOURCE_COMMIT = "25cec5ecfec8b9f016eb1631ac633194c2bed39f"


def require(condition, message):
    """Raise a verification error when a required integrity check fails."""
    if not condition:
        raise ValueError(message)


def sha(path):
    """Return the SHA-256 hex digest of the bytes at the given path."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    """Return a Git command's stdout from the governed repository root."""
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def reference_invariants(a):
    """Compute Delta through c6 rather than the production b8 formula."""
    a1, a2, a3, a4, a6 = a
    b2 = a1**2 + 4*a2
    b4 = a1*a3 + 2*a4
    b6 = a3**2 + 4*a6
    c4 = b2**2 - 24*b4
    c6 = -b2**3 + 36*b2*b4 - 216*b6
    numerator = c4**3 - c6**2
    require(numerator % 1728 == 0, "non-integral reference discriminant")
    delta = numerator // 1728
    require(delta != 0, "singular reference curve")
    return c4, delta, Fraction(c4**3, delta)


def symbolic_identity():
    """Prove the c4/c6 and b8 discriminant formulas agree symbolically.

    This checks an exact polynomial identity without loading observed ranks."""
    a1,a2,a3,a4,a6 = sp.symbols("a1 a2 a3 a4 a6")
    b2=a1**2+4*a2; b4=a1*a3+2*a4; b6=a3**2+4*a6
    b8=a1**2*a6+4*a2*a6-a1*a3*a4+a2*a3**2-a4**2
    c4=b2**2-24*b4; c6=-b2**3+36*b2*b4-216*b6
    delta=-b2**2*b8-8*b4**3-27*b6**2+9*b2*b4*b6
    require(sp.expand(c4**3-c6**2-1728*delta) == 0,
            "symbolic discriminant identity failed")


def reference_cohort():
    """Independently parse pinned ecdata and verify the rank-blind cohort.

    Check source bytes, representative membership, exact j=0 exclusions,
    c4/Delta, and principal-log coordinates. Never compute the cohort's
    neighbor graph, endpoint statistic, or registered null distribution."""
    raw=(ROOT/SOURCE).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==SOURCE_SHA, "source hash mismatch")
    require(len(raw)==2146401, "source size mismatch")
    lines=raw.decode("ascii").splitlines()
    labels=set(); classes=set(); accepted=[]; excluded=[]
    for line in lines:
        fields=line.split()
        require(len(fields)==6, "unexpected source field count")
        n=int(fields[0]); number=int(fields[2]); a=ast.literal_eval(fields[3])
        require(n>0 and number>0 and len(a)==5 and all(type(x) is int for x in a),
                "invalid source arithmetic fields")
        require(fields[1].isascii() and fields[1].isalpha() and fields[1].islower(),
                "invalid isogeny label")
        label=f"{n}{fields[1]}{number}"
        require(label not in labels, "duplicate source label")
        labels.add(label)
        if number!=1:
            continue
        key=f"{n}{fields[1]}"
        require(key not in classes, "duplicate isogeny representative")
        classes.add(key)
        c4,delta,j=reference_invariants(a)
        require(production.c4_from_ainvariants(tuple(a))==c4, "c4 disagreement")
        require(_discriminant(tuple(a))==delta, "Delta disagreement")
        point=production.project_arithmetic(tuple(a),n)
        if not j:
            require(point is None, "exact j=0 not excluded")
            excluded.append(label)
            continue
        # Read the rank only after the exact arithmetic selection.
        require(int(fields[4])>=0 and int(fields[5])>0, "invalid retained labels")
        direct=(math.log(n),math.log(abs(j)),0.0 if j>0 else math.pi)
        require(point[0]==direct[0] and point[2]==direct[2], "log branch disagreement")
        require(math.isclose(point[1],direct[1],rel_tol=0,abs_tol=1e-12),
                "principal logarithm disagreement above rounding tolerance")
        accepted.append((n,label,key,c4,delta))
    accepted.sort(key=lambda x:(x[0],x[1]))
    require((len(lines),len(classes),len(excluded),len(accepted)) ==
            (64687,38042,106,37936), "cohort count mismatch")
    # This loader constructs only the pinned projection, never its endpoint.
    config=json.loads((ROOT/CONFIG).read_text())
    frame, exclusions=production.load_locked_arithmetic(ROOT/SOURCE,config)
    require(frame.label.tolist()==[r[1] for r in accepted], "accepted membership disagreement")
    require(set(exclusions.label)==set(excluded), "exclusion membership disagreement")
    require(frame.c4.tolist()==[r[3] for r in accepted], "retained c4 mismatch")
    require(frame.delta.tolist()==[r[4] for r in accepted], "retained Delta mismatch")
    return {"source_rows":len(lines), "representatives":len(classes),
            "j_zero_exclusions":len(excluded), "accepted":len(accepted),
            "accepted_label_sha256":hashlib.sha256(
                ("\n".join(r[1] for r in accepted)+"\n").encode()).hexdigest(),
            "excluded_label_sha256":hashlib.sha256(
                ("\n".join(sorted(excluded))+"\n").encode()).hexdigest(),
            "log_check_absolute_tolerance":1e-12}


def fixture(kind):
    """Construct a deterministic 40-row synthetic graph/null test fixture.

    The kind selects tied, duplicate, or seeded asymmetric coordinates.
    Synthetic ranks are diagnostic only, not observed cohort data."""
    n=40
    if kind=="duplicates":
        points=[(0.0,0.0,0.0) if i<14 else (float(i%5),float(i//5),0.0) for i in range(n)]
    elif kind=="ties":
        points=[(float(i%5),float(i//5),0.0) for i in range(n)]
    else:
        rng=np.random.default_rng(710)
        points=rng.normal(size=(n,3))
    frame=pd.DataFrame(points,columns=["x","y","z"])
    frame["conductor"]=[101+i//2 for i in range(n)]
    # a10 sorts before a2: numeric suffix ordering must not replace ASCII.
    frame["label"]=[f"{101+i//2}a{10 if i%2==0 else 2}" for i in range(n)]
    frame["rank"]=[(i*i+i//3)%5 for i in range(n)]
    return frame.sort_values(["conductor","label"]).reset_index(drop=True)


def reference_edges(frame):
    """Enumerate the undirected k=10 graph on at most 64 synthetic rows.

    Use squared Euclidean distances and ASCII labels to break ties.
    Refuse production-cohort sizes before accessing coordinate columns."""
    require(len(frame)<=64, "reference graph is restricted to synthetic fixtures")
    points=frame[["x","y","z"]].to_numpy(dtype=np.float64)
    labels=frame.label.tolist(); edges=set()
    for i,p in enumerate(points):
        candidates=[]
        for j,q in enumerate(points):
            if i!=j:
                d=q-p
                candidates.append((float(np.dot(d,d)),labels[j],j))
        for _,_,j in sorted(candidates)[:10]:
            edges.add(tuple(sorted((i,j))))
    return sorted(edges)


def reference_words(seed):
    """Yield an independent SplitMix64 unsigned 64-bit word stream.

    Keep the RNG state continuous across calls and use 64-bit modular
    arithmetic with the frozen SplitMix64 shift/multiply constants."""
    state=seed
    while True:
        state=(state+int("9e3779b97f4a7c15",16)) % (2**64)
        z=state
        z=((z^(z>>30))*int("bf58476d1ce4e5b9",16)) % (2**64)
        z=((z^(z>>27))*int("94d049bb133111eb",16)) % (2**64)
        yield z^(z>>31)


def reference_permutation(size,stream):
    """Generate a Fisher-Yates index permutation from an existing stream.

    Use rejection sampling to avoid modulo bias; do not reseed the
    stream between successive permutations or conductor strata."""
    values=list(range(size))
    for i in reversed(range(1,size)):
        upper=i+1; cutoff=(2**64//upper)*upper
        value=next(stream)
        while value>=cutoff:
            value=next(stream)
        j=value%upper
        values[i],values[j]=values[j],values[i]
    return values


def fixture_checks():
    """Compare reference PRNG, kNN, strata, and nulls on synthetic inputs.

    Check published-style vectors, rejection boundaries, rank-blind
    graph membership, continuing-stream permutations, and three-draw
    synthetic rank nulls. Never evaluate the registered cohort endpoint."""
    vectors=[0xe220a8397b1dcdaf,0x6e789e6aa1b965f4,0x06c45d188009454f]
    rng=SplitMix64(0)
    require([rng.next_u64() for _ in vectors]==vectors,"published-style seed-zero vectors failed")
    rng=SplitMix64(4103); stream=reference_words(4103)
    words=[next(stream) for _ in range(128)]
    require([rng.next_u64() for _ in words]==words, "PRNG word disagreement")
    rng=SplitMix64(4103); stream=reference_words(4103)
    for size in [0,1,2,10,17,40,3,13]:
        require(rng.permutation(size).tolist()==reference_permutation(size,stream),
                "continuing-stream Fisher-Yates disagreement")
    cutoff=(2**64//3)*3
    with patch.object(SplitMix64,"next_u64",side_effect=[cutoff,2**64-1,4]) as mocked:
        require(SplitMix64(4103).randbelow(3)==1 and mocked.call_count==3,
                "rejection boundary was accepted")
    records=[]
    for kind in ["ties","duplicates","asymmetric"]:
        frame=fixture(kind); edges=reference_edges(frame)
        require(production.mcj_neighbor_edges(frame).tolist()==[list(x) for x in edges],
                f"brute-force graph mismatch: {kind}")
        changed=frame.copy(); changed["rank"]=changed["rank"].iloc[::-1].tolist()
        require(np.array_equal(production.mcj_neighbor_edges(changed),production.mcj_neighbor_edges(frame)),
                "graph depends on rank")
        groups=[list(range(s*4,(s+1)*4)) for s in range(10)]
        require([g.tolist() for g in production.decile_groups(frame)]==groups,
                "stratum mismatch")
        ranks=frame["rank"].tolist(); stream=reference_words(4103); expected=[]
        trials=[]
        for _ in range(3):
            trial=ranks.copy()
            for group in groups:
                perm=reference_permutation(len(group),stream)
                for local,index in enumerate(group):
                    trial[index]=ranks[group[perm[local]]]
                require(Counter(trial[i] for i in group)==Counter(ranks[i] for i in group),
                        "within-stratum ranks changed")
            trials.append(trial)
            expected.append(float(-Fraction(sum(abs(trial[i]-trial[j]) for i,j in edges),len(edges))))
        actual=production._null_statistics_core(np.asarray(ranks),np.asarray(edges),
            [np.asarray(g) for g in groups],draws=3,seed=4103)
        require(np.allclose(actual,expected,rtol=0,atol=1e-15),
                f"three-draw null disagrees with original-rank continuing stream: {kind}")
        records.append({"fixture":kind,"rows":40,"edges":len(edges),
                        "null_draws":3,"null_statistics":actual.tolist(),
                        "permuted_rank_sha256":hashlib.sha256(json.dumps(trials).encode()).hexdigest()})
    # Unequal sizes exercise the exact floor(10*i/n) boundary rule.
    uneven=fixture("ties").iloc[:37]
    expected=[[i for i in range(37) if 10*i//37==s] for s in range(10)]
    require([g.tolist() for g in production.decile_groups(uneven)]==expected,"unequal stratum boundaries")
    return {"prng_words_checked":128,"seed_zero_vectors":vectors,
            "rejection_boundary_checked":True,"unequal_strata_checked":True,
            "fixtures":records}


def verify():
    """Produce a read-only, source-locked A03 pre-execution receipt.

    Block real-cohort graph, endpoint, null, and run functions before
    selecting source rows. Check frozen bindings, synthetic algorithms,
    both closed execution gates, and unmodified governed-file hashes.
    This does not execute EXP-MAP-A03 or confer scientific approval."""
    config=json.loads((ROOT/CONFIG).read_text())
    spec=json.loads((ROOT/SPEC).read_text())
    paths={SOURCE,SPEC,CONFIG,"charter/STAR_Research_Charter_v0-2.pdf",
           "registry/experiment_registry_v0.2.csv","registry/dataset_registry_v0.1.csv",
           "registry/data_provenance_registry_v0.1.csv"}
    paths.update(item["path"] for field in ["code_inputs","config_files"] for item in spec[field])
    before={p:sha(ROOT/p) for p in sorted(paths)}
    require(git("ls-tree","HEAD","data/ecdata").split()[2]==SOURCE_COMMIT,
            "repository gitlink differs from source commit")
    # The initial cohort pass forbids all graph/statistical/execution functions.
    blocked=["mcj_neighbor_edges","rank_coherence","_null_statistics_core",
             "full_null_statistics","fixture_null_statistics","run_protocol"]
    with ExitStack() as stack:
        for name in blocked:
            stack.enter_context(patch.object(production,name,side_effect=ValueError(
                "real-cohort statistical execution is prohibited in verification")))
        symbolic_identity()
        cohort=reference_cohort()
        prepared=preflight_controlled_experiment(ROOT,ROOT/SPEC,require_execution_eligibility=False)
        try:
            preflight_controlled_experiment(ROOT,ROOT/SPEC)
        except PreflightError as exc:
            require("not controlled-execution eligible" in str(exc), "unexpected execution blocker")
            gate_message=str(exc)
        else:
            raise ValueError("normal execution preflight unexpectedly opened")
    fixtures=fixture_checks()
    require(config["null"]["seed"]==4103 and config["null"]["realizations"]==999,
            "locked randomization changed")
    require(config["inference"]["alpha"]==0.005 and
            config["inference"]["sidedness"]=="one_sided_greater", "inference changed")
    require(config["outputs"]==list(production.OUTPUT_FILENAMES)==spec["output_paths"],
            "output contract changed")
    resolved=RegistrySnapshot.load(ROOT).resolve("EXP-MAP-A03")
    flags={}
    for label,row in [("experiment",resolved.experiment),("dataset",resolved.dataset)]:
        flags[label]={k:row[k] for k in ["Controlled_Execution_Eligible",
            "Controlled_Support_Eligible","Physical_Support_Eligible"]}
        require(set(flags[label].values())=={"false"}, "eligibility gate opened")
    require(before=={p:sha(ROOT/p) for p in sorted(paths)},"governed bytes modified")
    return {"verification_status":"PASS","recorded_utc":datetime.now(timezone.utc).isoformat(),
            "governed_repository_commit":git("rev-parse","HEAD"),
            "source_commit":SOURCE_COMMIT,"charter_sha256":before["charter/STAR_Research_Charter_v0-2.pdf"],
            "input_sha256":before,"verifier_sha256":sha(Path(__file__)),
            "cohort":cohort,"synthetic_checks":fixtures,"registry_flags":flags,
            "registry_bindings":prepared.resolved.record_hashes,
            "binding_only_preflight":"PASS","normal_preflight":"BLOCKED_AS_REQUIRED",
            "normal_preflight_message":gate_message,"real_cohort_blocked_functions":blocked,
            "registered_experiment_executed":False,"actual_cohort_endpoint_computed":False,
            "off_author_scientific_approval":False,"governed_bytes_unchanged":True,
            "environment":{"python":platform.python_version(),"platform":platform.platform(),
                "packages":{name:importlib.metadata.version(name) for name in
                    ["numpy","pandas","scipy","sympy","PyYAML"]}}}


def main():
    """Run the verifier and print JSON, optionally creating a new receipt.

    The --output destination uses exclusive file creation; an existing
    receipt is never overwritten. Leave all governed inputs unchanged."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    report=verify()
    serialized=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8",newline="\n") as out:
            out.write(serialized)
    print(serialized)


if __name__=="__main__":
    main()
