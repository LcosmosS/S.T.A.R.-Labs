          sage -python -m pip install --upgrade pip
          sage -python -m pip install --no-cache-dir \
            numpy pandas tqdm plotly==5.18.0 corner ripser persim \
            nbconvert nbclient ipykernel nest_asyncio

      - name: Cache heavy data
        uses: actions/cache@v4
