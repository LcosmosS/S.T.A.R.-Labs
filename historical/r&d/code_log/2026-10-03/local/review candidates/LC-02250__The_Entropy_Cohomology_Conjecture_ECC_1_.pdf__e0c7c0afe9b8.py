
**Result**:
- Concentrated attractor zones clustered near `L_cosmo(s)` = 2.3 and 3.1
- Regions of symbolic phase bifurcation matched observed redshift shell transitions.

**Interpretation**:
- Projection attractors emerged from symbolic entropy field topology.
- These attractors were later stabilized in stratified models and used as identity filters.

-----------------------------------------
V. SYMBOLIC STRATIFICATION SNAPSHOT

```python
def define_entropy_strata(x):
    if x < 2.5:
        return 'Low'
    elif 2.5 <= x < 3.0:
        return 'Mid'
    else:
        return 'High'

data['entropy_strata'] = data['L_cosmo(s)'].apply(define_entropy_strata)
