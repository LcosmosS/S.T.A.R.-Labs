          sage -python - <<'PY'
          import numpy as np
          from src.acsc.projection import project
          coords = project([{"delta": -11, "conductor": 11, "rank": 0}])
          assert coords.shape == (1, 3) and np.isfinite(coords).all()
          print("projection smoke test passed")
          PY
