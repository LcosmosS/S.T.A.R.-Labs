# A01/A03 DATA-ARITHMETIC — immutable two-state compatibility design v0.1

**Proposal, not approval or activation.** Governed by
[`charter/STAR_Research_Charter_v0-2.pdf`](../../charter/STAR_Research_Charter_v0-2.pdf).
This branch makes **no** registry transitions and does **not** execute either
registered endpoint. PR #77's revert remains authoritative on `main`
pending an independently approved activation PR. The original A03 frozen
execution spec, protocol/config, source/parameter/null and outcomes remain
byte-for-byte unchanged.

## Exact frozen and proposed identities

| Binding | Currently frozen inactive | Proposed A01-only active |
| --- | --- | --- |
| `DATA-ARITHMETIC` canonical row SHA-256 | `2fe4ab7f5763f39c6cde8392c3f7d8ff1a565e4664ce6e192640b99f3fe146d7` | `1b81e05ab90ce822c7dcbda88bdb206f191f6523fac03fea5ecdf55724de44c2` |
| `EXP-MAP-A01` row SHA-256 | `31f0137f1de87ba1b548758383b664dab13515205a3c2696b0c0edf573a5f4b3` | `97dac41c4d8a866d0abbcdf5515829328e92ea1fb3cf7b4d03e1d9b9c0b9c868` |
| `EXP-MAP-A03` row SHA-256 | `3b0bb9c77c80a19a0fca69103f084bb9368593d56d1e3bf037775fb74732794e` | **same, no promotion** |

These are SHA-256 digests of canonical JSON dictionary representations of
complete CSV records (UTF-8, sorted keys, compact separators), not hashes of
individual CSV lines. The original A03 spec MUST retain the **inactive**
dataset hash; the compatibility proof reconstructs it by reverting solely
`Controlled_Execution_Eligible=true` to `false` in an otherwise
**exactly** pinned post-activation dataset record. The A01 row must equal its
exact proposed active hash. Any partial toggle, support change, other
dataset-row edit, A03 experiment activation, malformed flag, missing reference,
or different scientific binding is forbidden.

Upstream JohnCremona/ecdata gitlink
`25cec5ecfec8b9f016eb1631ac633194c2bed39f`, source
`allcurves.00000-09999` SHA-256
`259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`,
64,687 source rows; A01 representatives 38,042; A03 exact j=0
exclusions 106 and accepted curves 37,936. Source/endpoint/seed/null
values, `EXP-MAP-A03` code and preregistration artifacts are unchanged.

## Fail-closed execution boundary

`src/control/shared_dataset_compatibility.py` accepts only these two full
row hashes, validates the exact existing A03 experiment binding, and proves
the unique one-field row difference. `src/control/execution.py` uses this
only if **the dataset digest alone** differs from A03's frozen spec;
all other row/file/provenance bindings remain required. Binding-only
preflight stays closed for eligible experiments; only inactive A03 can inspect
a dataset approved separately for A01. **Normal A03 preflight remains blocked**
by A03's own false experiment execution flag, regardless of dataset status.

A03's preregistration validator and reference checker inspect this proof if
the shared dataset later becomes eligible. Any unreviewed transition must
fail rather than substituting new A03 hashes into the frozen spec. This
compatibility change updates a verification tool for the two metadata
states: the historical A03 reference receipt retains its original verifier
SHA-256 and must not be overwritten. New CI receipts are versioned by commit.

## Mandatory independent review / activation boundary

1. Review this compatibility design and all negative mutation tests **without
   setting any canonical eligibility flag**; obtain an off-author approval
   for the software compatibility change.
2. Only after compatibility is on `main`, construct a clean, separate A01
   activation diff from the then-current HEAD. Preserve the dynamic audit
   validator, A03 locked records/spec/protocol, intake/LFS provenance,
   ALADIN Lite controls, and any new independent verification receipts.
3. Permit only A01 experiment and shared dataset execution flags `false→true`,
   A01's derived spec hashes/snapshot, and the minimal explicitly reviewed
   audit/validation logic necessary for that transition.
4. Require exact-head `A01 source-locked activation preflight`, A03
   preregistration/reference verification, full CI, and independent off-author
   **human APPROVED review** of the *final activation diff*. Software/bot
   approvals are not substitutes for authorization. Do not run 999 draws in CI.
5. Any new evidence requires its own prospective reviewed transaction; this
   proposal neither authorizes A01/A03 execution nor claims arithmetic or
   physical support. No sky-coordinate release is enabled.
