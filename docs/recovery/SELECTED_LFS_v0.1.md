# Selected existing Git LFS sources — v0.1

This is a **metadata selection of five already uploaded and independently downloaded** historical SDSS/MaNGA source candidates from PR #51, not a new data upload. The raw files stay at their SHA-256-addressed `data/intake/recovered/2026-10-08/` paths. The immutable original `manifest.json` and `recovery_lfs_verification.json` establish the saved byte identities.

`registry/recovered_lfs_selection_v0.1.json` is a separate, append-only research intake candidate layer. It is **not** a replacement for `dataset_registry_v0.1.csv`, is not a preregistration, does not establish exact SDSS/CasJobs job lineage, and does not alter flags.

Read-only checks:

```bash
python tools/verify_recovered_lfs_selection.py
git lfs pull --include='data/intake/recovered/2026-10-08/*'
python tools/verify_recovered_lfs_selection.py --require-local-hydration
pytest -q tests/test_recovered_lfs_selection.py
```

Do not use the original quarantined matching outputs as clean data. Two audited 1,495-row tables had no confirmed matches within 2 arcseconds, and this selection does not resolve them. Spherical matching, candidate-null testing and leakage-safe SFR reconstruction each require a new versioned protocol.

**LFS capability boundary:** This PR uploads **zero new** LFS objects; it points to **five previously verified** ones and records existing evidence. Connector-level Git object writes cannot upload new binary LFS content. Future recovered files require genuine `git lfs push`, independent `git lfs pull` into a clean cache, full SHA-256/size verification, rights/security review, and a separate commit before registering them.
