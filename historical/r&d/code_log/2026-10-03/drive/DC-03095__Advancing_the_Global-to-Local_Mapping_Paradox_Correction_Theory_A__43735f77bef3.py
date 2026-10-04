     cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA) if omega else 0
     raw_volume = omega * reg * cosmo_scale**3 if omega and reg else 0
     denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(rank, 1e13)
     comoving_volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
