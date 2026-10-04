        python ci_diagnostics/diagnose_cosmology.py > ci_diagnostics/output.txt 2>&1 || true
        echo "=== DIAGNOSTICS OUTPUT ==="
        sed -n '1,200p' ci_diagnostics/output.txt

    - name: Validate sky survey loader
      run: |
