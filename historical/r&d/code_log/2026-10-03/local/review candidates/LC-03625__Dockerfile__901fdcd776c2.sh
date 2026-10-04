      sage -python -m pip install --no-cache-dir -e /opt/lmfdb || true; \
    else \
      echo "LMFDB repo has no installable package metadata; use it as source in /opt/lmfdb"; \
    fi
