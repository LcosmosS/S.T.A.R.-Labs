          sage -python scripts/build_ec_dataset_parallel.sage \
            --labels-file data/raw/ci_subset.csv \
            --output results/ci_ec_subset.csv \
            --workers 2 \
            --batch-size 50
