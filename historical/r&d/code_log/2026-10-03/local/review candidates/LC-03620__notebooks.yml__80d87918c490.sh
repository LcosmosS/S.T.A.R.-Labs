          mkdir -p results exports
          for nb in examples/*.ipynb; do
            echo "Running $nb"
            sage -python -m jupyter nbconvert \
              --to notebook \
              --execute "$nb" \
