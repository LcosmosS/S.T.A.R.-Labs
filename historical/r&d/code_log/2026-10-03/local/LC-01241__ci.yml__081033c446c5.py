          python - <<'PY'
          import csv
          from pathlib import Path

          root = Path("registry")
          required = [
              "claim_evidence_v0.2.csv",
              "claim_experiment_crosswalk_v0.2.csv",
              "experiment_registry_v0.2.csv",
              "dataset_registry_v0.1.csv",
              "parameter_registry_v0.1.csv",
              "null_registry_v0.1.csv",
              "r&d_artifact_registry_v0.1.csv",
          ]
          for name in required:
              assert (root / name).exists(), f"missing registry: {name}"

          def rows(name):
              with (root / name).open(newline="", encoding="utf-8") as f:
                  return list(csv.DictReader(f))

          claims = rows("claim_evidence_v0.2.csv")
          crosswalk = rows("claim_experiment_crosswalk_v0.2.csv")
          experiments = rows("experiment_registry_v0.2.csv")
          datasets = rows("dataset_registry_v0.1.csv")
          parameters = rows("parameter_registry_v0.1.csv")
          nulls = rows("null_registry_v0.1.csv")
          artifacts = rows("r&d_artifact_registry_v0.1.csv")

          claim_ids = {r["Claim_ID"] for r in claims}
          exp_ids = [r["Experiment_ID"] for r in experiments]
          dataset_ids = {r["Dataset_ID"] for r in datasets}
          parameter_ids = {r["Parameter_Set_ID"] for r in parameters}
          null_ids = {r["Null_ID"] for r in nulls}

          assert len(exp_ids) == len(set(exp_ids)), "duplicate Experiment_ID"
          assert len(claim_ids) == len(claims), "duplicate Claim_ID"
          assert len(dataset_ids) == len(datasets), "duplicate Dataset_ID"
          assert len(parameter_ids) == len(parameters), "duplicate Parameter_Set_ID"
          assert len(null_ids) == len(nulls), "duplicate Null_ID"

          crosswalk_pairs = {(r["Claim_ID"], r["Experiment_ID"]) for r in crosswalk}
          for r in claims:
              assert r["Claim_ID"] in claim_ids
              assert r["Evidence_Requirement"].strip(), f"empty evidence requirement: {r['Claim_ID']}"

          for r in experiments:
              assert r["Mode"] == "controlled", f"non-controlled experiment in controlled registry: {r['Experiment_ID']}"
              for cid in r["Claim_IDs"].split(";"):
                  assert cid in claim_ids, f"unknown Claim_ID: {cid}"
                  assert (cid, r["Experiment_ID"]) in crosswalk_pairs, f"missing crosswalk: {cid}/{r['Experiment_ID']}"
              assert r["Dataset_ID"] in dataset_ids, f"unknown Dataset_ID: {r['Dataset_ID']}"
              assert r["Parameter_Set_ID"] in parameter_ids, f"unknown Parameter_Set_ID: {r['Parameter_Set_ID']}"
              assert r["Null_ID"] in null_ids, f"unknown Null_ID: {r['Null_ID']}"

          for r in crosswalk:
              assert r["Claim_ID"] in claim_ids
              assert r["Experiment_ID"] in set(exp_ids)
              assert r["Role"].strip()
              assert r["Required_Control"].strip()

          for r in artifacts:
              assert r["Artifact_ID"].strip()
              assert r["Path"].strip()
              assert r["Evidence_Status"] in {"historical_or_illustrative", "exploratory", "controlled"}

          print(
              f"validated {len(claims)} claims, {len(experiments)} experiments, "
              f"{len(datasets)} datasets, {len(parameters)} parameter sets, "
