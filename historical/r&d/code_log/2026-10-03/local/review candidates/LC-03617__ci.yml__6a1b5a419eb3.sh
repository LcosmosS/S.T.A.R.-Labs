              git commit -m "ci: update ci_subset.csv (auto-generated from ecdata)"
              git push || echo "Push skipped (may need permissions)"
              echo "Successfully committed and pushed updated ci_subset.csv"
            fi
