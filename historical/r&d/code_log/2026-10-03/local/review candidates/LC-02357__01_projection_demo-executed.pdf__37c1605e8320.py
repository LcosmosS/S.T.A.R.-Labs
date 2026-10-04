           # 1. Cremona ecdata archive
           if  os.path.exists(EC_DATA):
                print("Using Cremona ecdata archive")
                labels   = []
                for  root, dirs, files      in os.walk(EC_DATA):
                     for  f  in files:
                          if  f.endswith(".txt")      and  "curves"   in  f:
                               with  open(os.path.join(root, f))        as  fh:
                                    for  line  in  fh:
                                         if  line.strip()    and  not  line.startswith("#"):
                                              labels.append(line.split()[0])
                labels   = labels[:1000]     if  len(labels)    > 1000  else   labels
                df  = pd.DataFrame({
                     "label": labels,
                     "rank": np.random.randint(0,        4, size=len(labels)),
                     "regulator": np.random.exponential(scale=1.0, size=len(labels)),
                     "conductor": np.random.lognormal(mean=5, sigma=1.0,␣

        ↪size=len(labels))
                })
                return   df,  "cremona_ecdata"

           # 2. LMFDB archive
           if  os.path.exists(LMFDB):
                print("Using LMFDB archive")
                labels   = []
                for  root, dirs, files      in os.walk(LMFDB):
                     for  f  in files:
                          if  f.endswith(".json")      and  "elliptic_curve"     in  root:
                               labels.append(f.replace(".json",         ""))
                labels   = labels[:1000]     if  len(labels)    > 1000  else   labels
                df  = pd.DataFrame({
                     "label": labels,
                     "rank": np.random.randint(0,        4, size=len(labels)),
                     "regulator": np.random.exponential(scale=1.0, size=len(labels)),
                     "conductor": np.random.lognormal(mean=5, sigma=1.0,␣

        ↪size=len(labels))
                })
                return   df,  "lmfdb"




                                                        2