          git config user.name "CI"
          git config user.email "ci@example.com"
          git add src/likelihoods/data/*.py
          git commit -m "CI: update embedded cosmology data" || echo "No changes"
          git push
