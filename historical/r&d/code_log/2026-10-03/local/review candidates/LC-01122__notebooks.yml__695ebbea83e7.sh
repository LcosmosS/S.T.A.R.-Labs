          sage -python -m pip install --upgrade pip
          sage -python -m pip install -r requirements.txt
          sage -python -m pip install nbconvert nbclient ipykernel
          sage -python -m pip install -e . --no-deps
          echo "PYTHONPATH=$GITHUB_WORKSPACE:$GITHUB_WORKSPACE/src" >> "$GITHUB_ENV"
      - name: Execute controlled notebooks
