 from joblib import Parallel, delayed, parallel_backend


  with parallel_backend('threading', n_jobs=4):
      # Your parallel code here
