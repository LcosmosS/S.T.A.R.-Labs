          python --version
          which python
          conda list | grep -E "sage|joblib" || true

      - name: Run tests
        shell: bash -l {0}
