import numpy as np
K_subs = []
for _ in range(10):
    sub_df = df.sample(n=5000)
    M_0_sub = 10**np.median(sub_df['logmass'])
    L_sub = np.mean(M_0_sub / (10**sub_df['logmass']))
    Reg_sub = np.mean((10**sub_df['logmass']) / M_0_sub)
    K_subs.append(Reg_sub / L_sub)
* print(np.mean(K_subs), np.std(K_subs))
* Expect mean K_{\text{sub}} \approx 1, with small standard deviation (e.g., < 0.1).
