            sage -python -m jupyter nbconvert --to notebook --execute "$nb"               --output "/tmp/$(basename "$nb")"               --ExecutePreprocessor.timeout=300               --ExecutePreprocessor.kernel_name=python3
          done
          sage -python - <<'PY'
          from pathlib import Path
          expected = {
              "00_registry_overview.ipynb",
              "01_preprocessing.ipynb",
              "02_arithmetic_reconstruction.ipynb",
              "03_mapping_benchmark.ipynb",
              "04_rank_environment.ipynb",
              "05_rank_topology.ipynb",
              "06_null_models.ipynb",
              "07_sfr_prediction.ipynb",
              "08_robustness.ipynb",
          }
          actual = {p.name for p in Path("notebooks").glob("*.ipynb")}
          assert actual == expected, f"controlled notebook set mismatch: {sorted(actual ^ expected)}"
          PY
          echo "executed all canonical controlled notebooks"
