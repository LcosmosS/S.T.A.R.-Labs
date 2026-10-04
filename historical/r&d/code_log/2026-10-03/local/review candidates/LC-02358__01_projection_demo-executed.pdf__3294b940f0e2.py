           # 3. CI-generated Cremona labels
           if  RUNNING_IN_CI    and  os.path.exists(CI_LABELS):
                print("Using CI-generated Cremona labels")
                labels   = pd.read_csv(CI_LABELS)["label"].tolist()
                df  = pd.DataFrame({
                     "label": labels,
                     "rank": np.random.randint(0,        4, size=len(labels)),
                     "regulator": np.random.exponential(scale=1.0, size=len(labels)),
                     "conductor": np.random.lognormal(mean=5, sigma=1.0,␣

        ↪size=len(labels))
                })
                return   df,  "ci_labels"

           # 4. Synthetic fallback
           print("No arithmetic archives found — using synthetic invariants")
           n  = 300
           df  = pd.DataFrame({
                "rank": np.random.randint(0,        4, size=n),
                "regulator": np.random.exponential(scale=1.0, size=n),
                "conductor": np.random.lognormal(mean=5, sigma=1.0, size=n)
           })
           return   df,  "synthetic"
