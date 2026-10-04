M_0 = 1e12; /* Reference mass: 10^12 M_sun */
N = 229;    /* KBSS sample size */
M = vector(N, i, /* KBSS stellar masses */); /* Replace with real data */
* L_cosmo(s) = sum(i=1, N, (M_0 / M[i])^s);
* Or, using metallicity:
* pari
OH_0 = 8.69; /* Solar metallicity: 12 + log(O/H) */
N = 229;
OH = vector(N, i, /* KBSS 12 + log(O/H) values */);
* L_cosmo(s) = sum(i=1, N, (OH_0 / OH[i])^s);
* Normalization: Scale L_{\text{cosmo}}(1) to M_{*,\text{total}}, or use the intrinsic scatter (\sigma_{\text{int}}) to adjust ( K ).
* Cosmological Constants: Adjust \text{Reg}_{\text{cosmo}} or \text{Sha}_{\text{cosmo}} based on metallicity or SFR trends, e.g., \text{Sha}_{\text{cosmo}} \propto \langle \log(\text{O/H}) \rangle.
