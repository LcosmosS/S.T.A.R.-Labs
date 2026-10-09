# M1-INH-E1 — proposed preregistration lifecycle recognition (2026-10-09)

**Authority:** `charter/STAR_Research_Charter_v0-2.pdf`. **Namespace:** `THEORY-SEARCH-v0.1`. **Claim:** `CLAIM-ACSC-MECH-002`.

## Exact, limited transition

The frozen original `preregistrations/M1-INH-E1/protocol.md` was filed with the obstruction program in `planned` status and already defines the precise Szekeres–Szafron sector, the complete elliptic-evolution record `𝔈`, invariant/branch conventions, and E1a/E1b/E1c stopping and interpretation rules. Its mathematical protocol bytes and recorded SHA-256 remain **untouched**; the original `Status: planned` header is historical rather than silently rewritten.

This prospective registry maintenance PR proposes only:

- `registry/theory_obstruction_registry_v0.1.csv: M1-INH-E1.Status`: `planned` → `preregistered` (recognition of the protocol already frozen on file).
- All three substage statuses (`Substage_A/B/C`) remain `planned`, reflecting no independently authorized completed or audited stage.
- `Controlled_Execution_Eligible`, `Controlled_Support_Eligible`, `Physical_Support_Eligible` and `Universal_NoGo_Claim` remain `false`.
- No changes to `P0-SF-v0.1`, the five closed-search candidates, crosswalks, arithmetic preregistrations, experimental data, publisher bytes, null models or astronomy/ALADIN admission.
- The read-only web snapshot must show the current registry status, separately from any protocol's historical governance heading or claims of result completion.

**This PR is a proposed lifecycle correction, not retrospective execution authorization.** The independent reviewer must confirm that the existing unchanged frozen protocol qualifies for the label `preregistered`; if not, the correct disposition is to retain `planned` until a separately approved registration transition. Mathematical derivation packages and constructive witness proposals remain review submissions rather than automatically established theorems.

## Aladin data release boundary

`web_tool/content/sky-overlay-releases.v1.json` continues to contain zero admitted dataset scopes. Successful source integrity/publisher provenance CI (including Pipe3D, GEMA or corrected ALFALFA) does not independently authenticate a human review. A future display-only approval needs an exact hash-bound derivative, positional-role/selection evidence, and an accountable off-author review receipt; only a subsequent reviewed PR may modify the release manifest. This change does not admit a sky release.

See the [versioned dataset candidate](../../web_tool/content/sky-overlay-candidates.v1.json), the [CI admission contract](../../web_tool/content/CI_FROZEN_SKY_RELEASE_GATE.md), and the [M1 frozen protocol](../../preregistrations/M1-INH-E1/protocol.md).
