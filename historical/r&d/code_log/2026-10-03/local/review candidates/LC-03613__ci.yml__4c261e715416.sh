          git submodule update --init --recursive --depth 1 2>/dev/null || {
            echo "Submodule initialization failed, attempting direct clone from GitHub..."
            
            if [ ! -d "data/ecdata" ] || [ -z "$(ls -A data/ecdata 2>/dev/null)" ]; then
              echo "Cloning JohnCremona/ecdata..."
              mkdir -p data/ecdata
              git clone --depth 1 https://github.com/JohnCremona/ecdata.git data/ecdata || true
            fi
            
            if [ ! -d "data/eclib" ] || [ -z "$(ls -A data/eclib 2>/dev/null)" ]; then
              echo "Cloning JohnCremona/eclib..."
              mkdir -p data/eclib
              git clone --depth 1 https://github.com/JohnCremona/eclib.git data/eclib || true
            fi
            
            if [ ! -d "data/lmfdb" ] || [ -z "$(ls -A data/lmfdb 2>/dev/null)" ]; then
              echo "Cloning LMFDB/lmfdb..."
              mkdir -p data/lmfdb
              git clone --depth 1 https://github.com/LMFDB/lmfdb.git data/lmfdb || true
            fi
          }
          echo "=== Submodule Status After Initialization ==="
