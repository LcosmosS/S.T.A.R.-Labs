#!/usr/bin/env python3
"""Validate prospective preregistration reviews without running experiments."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = "registry/preregistration_transition_candidates_v0.1.json"
CONFIG = "preregistrations/EXP-MAP-A03/config.json"


class PreregistrationReviewError(ValueError):
    pass


def require(value, message):
    if not value:
        raise PreregistrationReviewError(message)


def load_json(root: Path, relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def load_csv(root: Path, relative: str, id_field: str):
    with (root / relative).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        require(reader.fieldnames and id_field in reader.fieldnames, "Missing CSV identity")
        require(len(reader.fieldnames) == len(set(reader.fieldnames)), "Duplicate CSV field")
        rows = list(reader)
    require(all(None not in r and all(v is not None for v in r.values()) for r in rows),
            "Malformed CSV record")
    require(len({r[id_field] for r in rows}) == len(rows), "Duplicate registry identity")
    return {r[id_field]: r for r in rows}


def validate(root: Path = ROOT, *, ledger=None, config=None):
    ledger = ledger if ledger is not None else load_json(root, LEDGER)
    config = config if config is not None else load_json(root, CONFIG)
    require(ledger["schema_version"] == "candidate-preregistration-ledger-v0.1", "Wrong candidate schema")
    require(ledger["governing_charter"] == "charter/STAR_Research_Charter_v0-2.pdf", "Wrong charter")
    require(config["schema_version"] == "prospective-prereg-v1", "Wrong protocol schema")
    require(config["experiment_id"] == "EXP-MAP-A03", "Wrong experiment")
    require(config["scientific_scope"].endswith("NO cosmological data or physical support"),
            "Arithmetic-only scope must be explicit")
    require(config["input"]["source_sha256"] ==
            "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968",
            "Arithmetic source bytes not pinned")
    require(config["input"]["source_rows"] == 64687 and
            config["input"]["isogeny_representatives"] == 38042, "Incorrect arithmetic cohort")
    a01_manifest = load_json(root, "preregistrations/EXP-MAP-A01/dataset_manifest.json")
    require(config["input"]["source_sha256"] == a01_manifest["artifact"]["sha256"], "A01 source mismatch")
    require(config["input"]["source_gitlink"] == a01_manifest["source"]["git_commit"],
            "Source gitlink mismatch")
    require(config["mapping"]["rank_used_in_embedding"] is False and
            config["mapping"]["jitter"] is False and config["mapping"]["clipping"] is False,
            "Rank contamination in arithmetic embedding")
    require(config["null"]["realizations"] == 999 and config["null"]["seed"] == 4103 and
            config["null"]["rerolls"] is False and
            config["null"]["algorithm"] == "splitmix64-fisher-yates-v1", "Unfrozen null")
    require(config["endpoint"]["statistic"] ==
            "T_obs = - mean_over_edges(abs(rank_i-rank_j))" and
            config["inference"]["alpha"] == 0.005 and
            config["inference"]["primary_endpoint_count"] == 1, "Endpoint or threshold changed")
    require(config["mapping"]["j_zero_policy"].startswith("exclude_before_graph_and_before_rank_use"),
            "Undefined j=0 cannot be handled after checking ranks")
    require(config["outputs"] == ["summary.json","observed_mcj_projection.csv",
                                  "null_statistics.csv","exclusions_j_zero.csv"], "Output contract modified")
    require(all(v is False for k,v in config["controls"].items()
                if k in {"controlled_execution_eligible","controlled_support_eligible",
                         "physical_support_eligible"}), "Execution/support promotion prohibited")
    experiments = load_csv(root, "registry/experiment_registry_v0.2.csv", "Experiment_ID")
    params = load_csv(root, "registry/parameter_registry_v0.1.csv", "Parameter_Set_ID")
    nulls = load_csv(root, "registry/null_registry_v0.1.csv", "Null_ID")
    datasets = load_csv(root, "registry/dataset_registry_v0.1.csv", "Dataset_ID")
    claims = load_csv(root, "registry/claim_evidence_v0.2.csv", "Claim_ID")
    require(len(ledger["candidates"]) == 3, "Candidate set modified without new version")
    ids = [r["experiment_id"] for r in ledger["candidates"]]
    require(ids == ["EXP-MAP-A03", "EXP-DATA-A01", "EXP-CTRL-A02"], "Unexpected candidate priority")
    for candidate in ledger["candidates"]:
        exp_id = candidate["experiment_id"]
        require(exp_id in experiments, "Experiment missing from canonical registry")
        canonical = experiments[exp_id]
        require(candidate["canonical_status"] == canonical["Status"] == "planned",
                "Canonical lifecycle promoted without review")
        for name,key,lookup in [("qualified_experiment_id","Qualified_Experiment_ID",None),
                                ("dataset_id","Dataset_ID",datasets),
                                ("parameter_set_id","Parameter_Set_ID",params),
                                ("null_id","Null_ID",nulls)]:
            value=candidate[name]
            require(value == canonical[key], f"{exp_id}: identity mismatch {name}")
            if lookup is not None: require(value in lookup, f"{exp_id}: orphaned {name}")
        require(candidate["claim_ids"] == canonical["Claim_IDs"].split(";"),
                "Claim crosswalk mismatch")
        require(all(cid in claims for cid in candidate["claim_ids"]),
                "Unknown claim")
        require(all(candidate[k] is False for k in [
            "controlled_execution_eligible","controlled_support_eligible","physical_support_eligible"]),
            "Ledger eligibility promotion prohibited")
        require(all(canonical[k] == "false" for k in [
            "Controlled_Execution_Eligible","Controlled_Support_Eligible","Physical_Support_Eligible"]),
            "Canonical execution/support gate opened")
        require((root / candidate["protocol"]).is_file(), "Missing review protocol")
        if exp_id == "EXP-MAP-A03":
            require(candidate["config"] == CONFIG, "Config does not match reviewed file")
            require(candidate["design_status"] == "prospective_protocol_locked_pending_canonical_transition",
                    "Protocol review status changed without approval")
            require(params[candidate["parameter_set_id"]]["Preregistration_Status"] ==
                    "not_preregistered" and
                    nulls[candidate["null_id"]]["Preregistration_Status"] ==
                    "not_preregistered", "Canonical transition cannot occur silently")
        else:
            require(candidate["design_status"].startswith("design_only_blocked_"),
                    "Unbound experiment incorrectly marked locked")
    require(experiments["EXP-MAP-A01"]["Status"] == "preregistered", "A01 altered")
    require(all(experiments["EXP-MAP-A01"][k] == "false" for k in [
        "Controlled_Execution_Eligible","Controlled_Support_Eligible","Physical_Support_Eligible"]),
        "A01 cannot be activated in a prospective design PR")
    return len(ledger["candidates"])


if __name__ == "__main__":
    count = validate()
    print(f"PASS: {count} prospective candidate reviews; 0 execution/support promotions; "
          "A01 unchanged; canonical transitions pending.")
