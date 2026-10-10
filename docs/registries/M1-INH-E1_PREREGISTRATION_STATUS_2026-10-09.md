# M1-INH-E1 — website display of frozen protocol versus formal status (2026-10-09)

**Governing charter:** `charter/STAR_Research_Charter_v0-2.pdf`.
**Formal source of record:** `registry/theory_obstruction_registry_v0.1.csv` (`THEORY-SEARCH-v0.1:M1-INH-E1`).
**Frozen protocol:** `preregistrations/M1-INH-E1/protocol.md`.

## Why two labels must remain visible

M1-INH-E1 has a fully defined **frozen preregistration protocol on file** specifying the Szekeres–Szafron class, its complete elliptic-evolution record and branches, E1a–E1c obligations, limitations and failure rules. Its governing header and formal registry both still say **`planned`**. The independent mathematical review docket at `research/gates/P0_M1_INDEPENDENT_REVIEW.md` explicitly directs that M1 must not be advanced from `planned` pending external mathematical replication.

Therefore the web tool must display **both**:

- **Protocol on file:** frozen/preregistered design document exists and has a SHA-256 bound to the read-only registry website snapshot.
- **Formal registry lifecycle:** `planned` (no approved preregistration-status promotion, no execution or reviewed theorem). E1a, E1b, E1c are independently still `planned` in the canonical registry.

This preserves the user's distinction between having a registered, frozen scientific design and having obtained an independently authorized lifecycle transition. `Mode=controlled` for numerical studies denotes a proposed methodology, not a completed controlled experiment. M1 is a theory obstruction program, **not** an entry in the controlled numerical experiment registry.

## Automatic display and controls

The website discovers all formally `preregistered` and `preregistered_*` records from both controlled-experiment and theory-program registries, instead of maintaining a manual allowlist. The M1 protocol is additionally shown in a **frozen-protocol-on-file / registry-planned** section because it has a committed protocol path but is not formally promoted. No canonical registry or frozen protocol bytes are modified by this display PR.

No controlled execution, controlled support, physical support, theorem acceptance, astronomical matching, or ALADIN Lite release is activated.

## ALADIN Lite

As of this review, `web_tool/content/sky-overlay-releases.v1.json` contains `sources: []`. The corrected ALFALFA display extract is a hash-bound candidate with `approvalStatus=pending_independent_review`; publisher/integrity checks and the CI sky gate cannot independently authenticate the scientific reviewer. An off-author, exact-hash review receipt and a separate, approved release-manifest transition are required before ALADIN can offer real observational coordinates.

Related records: `web_tool/content/CI_FROZEN_SKY_RELEASE_GATE.md`, `web_tool/content/sky-overlay-candidates.v1.json`, `research/gates/P0_M1_INDEPENDENT_REVIEW.md`.
