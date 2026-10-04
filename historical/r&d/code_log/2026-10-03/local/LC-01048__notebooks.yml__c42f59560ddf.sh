        mkdir -p exports examples/exports
        for nb in examples/*-executed.ipynb; do
          base=$(basename "$nb" .ipynb)
          echo "Exporting $nb -> exports/${base}.html and exports/${base}.pdf"
          # HTML to central exports dir
          sage -python -m jupyter nbconvert --to html "$nb" --output-dir exports --output "${base}.html"
          # PDF (latex) to central exports dir
          sage -python -m jupyter nbconvert --to pdf "$nb" --output-dir exports --output "${base}.pdf"
        done


    - name: Upload artifacts
      uses: actions/upload-artifact@v4
