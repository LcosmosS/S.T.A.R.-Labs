# Research content v1 — epistemic display contract

This is a **versioned, read-only presentation layer** distinct from `registry/*`, the preregistered protocols, the controlled runner, and the synthetic fixture engine. Records are `illustrative_model`, `historical_exploratory`, `derived_mathematics` (formal result under specified assumptions), or `archival_reference`. There is **no published 'scientifically supported physical correspondence' tier** in v1. All three eligibility fields must be `false`, enforced at generation time and in tests.

Contents include historical Φ, alternative mappings, a BSD-inspired *cosmological* bin-count series, Betti meanings, an epistemic dependency diagram, registered E1a reduction, crossmatching reconstruction flow, the identity d²=0, and an inert recovered CasJobs notebook output. Source references remain links to audited repository artifacts; no original pickle, arbitrary notebook, proprietary survey output, or private file is executed in the browser.

To publish changes:

```bash
cd web_tool
npm run research:sync
npm run research:check
npm test
npm run typecheck
npm run build
```

Build and preview browser checks must pass on desktop and mobile, including navigation, filtering, source links, console and horizontal overflow; GitHub Actions results are not a substitute for browser testing. Deployment is restricted to `main` and `prototype/starmap`; this PR does not deploy production. Review the model and snapshot diff together. The educational corpus **does not auto-promote** claims when source documents or registries change.

The original user's BSD/SFR report is not uploaded. An explicitly labeled extraction of its reported constructs and limitations appears in `historical-sfr-report-context.v1.md`; metrics therein are not a verified dataset provenance record.
