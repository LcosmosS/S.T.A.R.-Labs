       RUNNING_IN_CI      = os.environ.get("GITHUB_ACTIONS",             "false")    ==   "true"

       CI_LABELS    =  "data/raw/ci_subset.csv"
       EC_DATA   =  "external/ecdata"
       LMFDB   = "external/lmfdb"

       print("Running in CI:", RUNNING_IN_CI)
       print("CI labels:", os.path.exists(CI_LABELS))
       print("Cremona ecdata:", os.path.exists(EC_DATA))
       print("LMFDB:", os.path.exists(LMFDB))

      Running in CI: True
      CI labels: False
      Cremona ecdata: False
      LMFDB: False




                                                             1