        sage -python -m pip install --upgrade pip setuptools wheel
        # core runtime libs used by your code and notebook execution
        sage -python -m pip install --no-cache-dir \
          numpy pandas tqdm scikit-learn flask pymongo gunicorn \
          ripser persim \
