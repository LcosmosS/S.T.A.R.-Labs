          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt
          python -m pip install pytest
      - name: Run unit tests
        env:
