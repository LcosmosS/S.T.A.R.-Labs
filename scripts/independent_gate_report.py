"""Dated, fail-closed read-only research-gate census.

Prints current canonical registry state; never promotes canonical statuses.
Does not run scientific experiments. Publication readiness is NOT computed as a
single score because proof review, null calibration and physical support differ.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path


def _read_rows(path: Path, key: str):
    with path.open(encoding="utf-8", newline="") as stream:
        rows=list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f"empty registry: {path}")
    names=[r[key] for r in rows]
    if len(names)!=len(set(names)):
        raise ValueError(f"duplicate {key} in {path}")
    return {r[key]:r for r in rows}


def inspect(root: Path) -> dict:
    r=root/"registry"
    experiments=_read_rows(r/"experiment_registry_v0.2.csv","Experiment_ID")
    datasets=_read_rows(r/"dataset_registry_v0.1.csv","Dataset_ID")
    params=_read_rows(r/"parameter_registry_v0.1.csv","Parameter_Set_ID")
    nulls=_read_rows(r/"null_registry_v0.1.csv","Null_ID")
    problems=[]
    entries=[]
    for name,row in sorted(experiments.items()):
        status=row["Status"]
        if row["Dataset_ID"] not in datasets:
            problems.append(f"{name}: unresolved dataset {row['Dataset_ID']}")
        if row["Parameter_Set_ID"] not in params:
            problems.append(f"{name}: unresolved parameter {row['Parameter_Set_ID']}")
        if row["Null_ID"] not in nulls:
            problems.append(f"{name}: unresolved null {row['Null_ID']}")
        execution=row["Controlled_Execution_Eligible"].strip().lower()=="true"
        controlled=row["Controlled_Support_Eligible"].strip().lower()=="true"
        physical=row["Physical_Support_Eligible"].strip().lower()=="true"
        if status not in ("planned","preregistered","executed","completed"):
            problems.append(f"{name}: review unknown status '{status}'")
        if execution and status=="planned":
            problems.append(f"{name}: planned yet execution flag true")
        if physical and not controlled:
            problems.append(f"{name}: physical support without controlled support")
        if controlled and not execution:
            problems.append(f"{name}: controlled support without execution eligibility")
        blocked=[]
        if status=="planned":
            blocked.append("canonical_preregistration_and_immutable_protocol_review")
        for field,which,idx in (("dataset",row["Dataset_ID"],datasets),
                                ("parameter",row["Parameter_Set_ID"],params),
                                ("null",row["Null_ID"],nulls)):
            if which not in idx:
                blocked.append(f"unknown_{field}")
        if not execution:
            blocked.append("separate_controlled_activation_approval")
        if not controlled:
            blocked.append("controlled_result_and_independent_replication_unverified")
        if not physical:
            blocked.append("mechanism_and_heldout_physical_validation_unverified")
        entries.append(dict(experiment_id=name,status=status,
                            execution_eligible=execution,controlled_support=controlled,
                            physical_support=physical,blocking_gates=blocked))
    return dict(authority="charter/STAR_Research_Charter_v0-2.pdf",
                experiment_count=len(entries),
                planned=sum(x["status"]=="planned" for x in entries),
                preregistered=sum(x["status"]=="preregistered" for x in entries),
                execution_eligible=sum(x["execution_eligible"] for x in entries),
                controlled_support=sum(x["controlled_support"] for x in entries),
                physical_support=sum(x["physical_support"] for x in entries),
                registry_integrity_violations=problems,
                no_scientific_experiment_was_run=True,
                entries=entries)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--require-all-preregistered",action="store_true")
    args=parser.parse_args(argv)
    report=inspect(args.root)
    print(json.dumps(report,indent=2,sort_keys=True))
    if report["registry_integrity_violations"]:
        return 2
    if args.require_all_preregistered and report["planned"]:
        return 3
    return 0


if __name__=="__main__":
    raise SystemExit(main())
