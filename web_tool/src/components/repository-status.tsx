import { Badge } from "@/components/ui/badge";
import snapshot from "@/lib/star/registry-snapshot.json";
import releases from "../../content/sky-overlay-releases.v1.json";
import { executionSummary } from "@/lib/star/repository-status";

const LABS_URL = "https://github.com/LcosmosS/S.T.A.R.-Labs";
const EVIDENCE_COMMIT = "f6d8bc8e954d5923ab9fa512ffcc6320d4c4018b";
const SOURCE_COMMIT = "1b0f2d7853608bfbab79cf2dc04b002f1f193eb2";
const RUN_ID = "20261016T041335361140Z-e60fd05117fc";
const PACKAGE_URL = `${LABS_URL}/tree/${EVIDENCE_COMMIT}/release_packages/EXP-MAP-A01-primary-execution-v0.1`;
const EVIDENCE_URL = `${LABS_URL}/blob/${EVIDENCE_COMMIT}/release_packages/EXP-MAP-A01-primary-execution-v0.1`;

/** The saved primary result is separate from this app's illustrative fixtures. */
export function A01PrimaryEvidence({ headingAs = "h2" }: { headingAs?: "h2" | "h3" }) {
  const Heading = headingAs;
  const gates = snapshot.candidate.gateState;
  return <section aria-label="EXP-MAP-A01 primary execution evidence" className="space-y-4 rounded-xl border border-border bg-surface p-5">
    <Badge tone="steel">Primary execution · independent replication outstanding</Badge>
    <Heading className="font-display text-xl tracking-tight">EXP-MAP-A01: bounded arithmetic result</Heading>
    <p className="text-sm leading-relaxed text-muted">
      The preserved investigator-A primary run reports local rank/elevation coherence against the locked
      NULL-MAP-001 arithmetic rank-permutation null. It rejects that null at α = 0.01 for the single preregistered endpoint.
    </p>
    <dl className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <div className="min-w-0">
        <dt className="text-xs text-muted">Observed T</dt>
        <dd className="mt-1 break-all font-mono text-sm tabular-nums">-114.40183841751903</dd>
      </div>
      <div>
        <dt className="text-xs text-muted">Corrected permutation p</dt>
        <dd className="mt-1 font-mono text-sm tabular-nums">0.001</dd>
      </div>
      <div>
        <dt className="text-xs text-muted">Null exceedances</dt>
        <dd className="mt-1 font-mono text-sm tabular-nums">0 / 999</dd>
      </div>
      <div>
        <dt className="text-xs text-muted">Analysis rows</dt>
        <dd className="mt-1 font-mono text-sm tabular-nums">38,042 / 64,687 source rows</dd>
      </div>
    </dl>
    <p className="text-sm leading-relaxed text-muted">
      T = −mean(|elevationᵢ − elevationⱼ|) on the fixed k = 10 arithmetic neighbor graph; larger T means greater
      local coherence. Exceedances count T_null ≥ T_observed. The locked correction is
      p = (1 + 0) / (999 + 1) = 0.001, the smallest attainable p-value with 999 permutations, not zero.
      The cohort selects curve-number-1 isogeny representatives.
    </p>
    <p className="text-sm leading-relaxed text-muted">
      This arithmetic null does not test a survey-selection-matched cosmological null or distinguish ACSC from
      other arithmetic structure. No cosmological correspondence or physical ACSC support is established.
      Independent rerun and replication remain outstanding; archive/hash inspection is package verification.
      The 160 browser fixtures and canvases are illustrations, separate from this recorded result.
    </p>
    <p className="text-sm leading-relaxed text-muted">
      Current registry gates: experiment execution eligible: {String(gates.experimentExecutionEligible)};
      dataset execution eligible: {String(gates.datasetExecutionEligible)};
      controlled-support eligible: {String(gates.controlledSupportEligible)};
      physical-support eligible: {String(gates.physicalSupportEligible)}.
      {" "}{executionSummary(gates)} Earlier package descriptions of disabled execution describe their historical state.
    </p>
    <p className="break-all text-xs leading-relaxed text-muted">
      Preserved primary transaction: {RUN_ID} · source revision {SOURCE_COMMIT}.
    </p>
    <div className="flex flex-wrap gap-x-4 gap-y-2 text-xs text-steel">
      <a href={`${EVIDENCE_URL}/${RUN_ID}/summary.json`} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">Saved run summary</a>
      <a href={PACKAGE_URL} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">Immutable primary package</a>
      <a href={`${EVIDENCE_URL}/verification.json`} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">Package verification receipt</a>
      <a href={`${LABS_URL}/commit/${SOURCE_COMMIT}`} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">Pinned execution source</a>
      <a href={`${LABS_URL}/pull/104`} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">Evidence intake · PR #104</a>
    </div>
  </section>;
}

/** Shared presentation prevents research, registry and projection status drift. */
export function RepositoryStatus() {
  const a03 = snapshot.experiments.find(row => row.Experiment_ID === "EXP-MAP-A03");
  return <section aria-label="Current repository status" className="space-y-4 rounded-xl border border-border bg-surface p-5">
    <Badge tone="steel">Repository records · read only</Badge>
    <h2 className="font-display text-xl tracking-tight">Repository status and published packages</h2>
    <A01PrimaryEvidence headingAs="h3" />
    <p className="text-sm leading-relaxed text-muted">
      EXP-MAP-A03: {a03?.Status}; execution eligible: {a03?.Controlled_Execution_Eligible}.
      Its pre-execution archive is separate from an original controlled run or independent replication.
    </p>
    <p className="text-sm leading-relaxed text-muted">
      Observational sky releases admitted for display: {releases.sources.length}.
      Display admission authorizes neither cross-matching nor population inference or physical support.
    </p>
    {releases.sources.map(release => <p key={release.datasetId} className="text-xs leading-relaxed text-muted">
      {release.datasetId} · {release.coordinateRole} · {release.sourceRows.toLocaleString()} publisher rows · {release.reviewStatus}.
      {" "}<a className="text-steel underline underline-offset-4" href={`https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/${release.reviewPath}`} target="_blank" rel="noopener noreferrer">Read display review receipt</a>
    </p>)}
    <ul className="space-y-4">
      {snapshot.publications.map(publication => <li key={publication.id} className="min-w-0 border-t border-border pt-3">
        <h3 className="text-sm font-medium">{publication.title}</h3>
        <p className="mt-1 text-xs leading-relaxed text-muted">{publication.status}</p>
        <div className="mt-2 flex flex-wrap gap-x-4 gap-y-2 text-xs text-steel">
          <a href={publication.doi} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">Version-specific DOI · {publication.id}</a>
          <a href={publication.release} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">GitHub release · {publication.id}</a>
          {publication.reviewLinks.map(url => <a key={url} href={url} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">Review lineage · PR #{url.split("/").at(-1)}</a>)}
        </div>
      </li>)}
    </ul>
    <p className="break-all text-[10px] leading-relaxed text-muted">
      Repository snapshot SHA-256: {snapshot.contentSha256}. Publication descriptions come from the hashed repository README;
      DOI links do not independently verify deposited bytes. This deployed snapshot is not a live GitHub status feed.
    </p>
  </section>;
}
