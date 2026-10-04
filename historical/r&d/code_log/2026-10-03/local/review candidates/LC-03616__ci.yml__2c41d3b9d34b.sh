          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

          if [ -f data/raw/ci_subset.csv ]; then
            git add data/raw/ci_subset.csv
            if git diff --staged --quiet; then
              echo "No changes to ci_subset.csv - skipping commit"
            else
