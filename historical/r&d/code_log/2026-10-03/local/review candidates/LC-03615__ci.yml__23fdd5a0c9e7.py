          mkdir -p data/raw results
          echo "=== Generating clean CI subset from ecdata (Final) ==="

          cat > generate_ci_subset.sage << 'EOF'
          from sage.all import *
          import csv
          import os

          print("Generating clean CI subset from ecdata submodule...")

          ecdata_path = "data/ecdata"
          labels = []

          # Priority 1: alllabels directory
          alllabels_dir = os.path.join(ecdata_path, "alllabels")
          if os.path.isdir(alllabels_dir):
              print("Reading from alllabels directory...")
              for root, dirs, files in os.walk(alllabels_dir):
                  for file in files:
                      if file.endswith((".txt", ".csv")) or "alllabels" in file.lower():
                          filepath = os.path.join(root, file)
                          try:
                              with open(filepath) as f:
                                  for line in f:
                                      label = line.strip()
                                      if label and not label.startswith('#') and len(label) > 3:
                                          labels.append(label)
                                      if len(labels) >= 800:
                                          break
                          except:
                              continue
                          if len(labels) >= 800:
                              break
                  if len(labels) >= 800:
                      break

          # Priority 2: curves directory
          if len(labels) < 100:
              print("Falling back to curves directory...")
              curves_dir = os.path.join(ecdata_path, "curves")
              if os.path.isdir(curves_dir):
                  for root, dirs, files in os.walk(curves_dir):
                      for file in files:
                          if file.endswith((".csv", ".txt")) and len(file) > 3:
                              base = file.split('.')[0]
                              if base and len(base) > 3 and base not in labels:
                                  labels.append(base)
                              if len(labels) >= 800:
                                  break
                      if len(labels) >= 800:
                          break

          print(f"Collected {len(labels)} labels.")

          # Final hardcoded fallback
          if len(labels) == 0:
              print("WARNING: Using hardcoded fallback")
              labels = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","26a1","37a1","37b1","43a1"]

          # Write clean CSV
          with open("data/raw/ci_subset.csv", "w", newline="") as f:
              writer = csv.writer(f)
              writer.writerow(["label"])
              for label in labels:
                  writer.writerow([label])

          print("CI subset written successfully.")
          print("First 10 labels:", labels[:10])
          EOF

                    sage generate_ci_subset.sage

                    echo "=== Final ci_subset.csv Contents ==="
                    cat data/raw/ci_subset.csv
          
      - name: Commit CI Subset to Repository
        shell: bash -l {0}
