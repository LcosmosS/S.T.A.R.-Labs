        mkdir -p external
        git clone https://github.com/JohnCremona/ecdata.git external/ecdata || true
        git clone https://github.com/JohnCremona/eclib.git external/eclib || true
        git clone https://github.com/LMFDB/lmfdb.git external/lmfdb || true

    - name: Generate CI Cremona label subset
      run: |
