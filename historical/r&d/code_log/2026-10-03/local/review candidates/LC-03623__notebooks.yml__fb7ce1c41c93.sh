          mkdir -p exports
          for nb in examples/*-executed.ipynb; do
            base=$(basename "$nb" .ipynb)
            sage -python -m jupyter nbconvert --to html "$nb" --output-dir exports --output "${base}.html"
            sage -python -m jupyter nbconvert --to pdf  "$nb" --output-dir exports --output "${base}.pdf"
          done

      - name: Upload artifacts
        uses: actions/upload-artifact@v6
