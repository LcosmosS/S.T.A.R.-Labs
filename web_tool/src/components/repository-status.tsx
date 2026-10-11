import { Badge } from "@/components/ui/badge";
import snapshot from "@/lib/star/registry-snapshot.json";
import releases from "../../content/sky-overlay-releases.v1.json";
import { executionSummary } from "@/lib/star/repository-status";

/** Shared presentation prevents research, registry and projection status drift. */
export function RepositoryStatus() {
  const a03 = snapshot.experiments.find(row => row.Experiment_ID === "EXP-MAP-A03");
  return <section aria-label="Current repository status" className="space-y-4 rounded-xl border border-border bg-surface p-5">
    <Badge tone="steel">Repository records · read only</Badge>
    <h2 className="font-display text-xl tracking-tight">Repository status and published packages</h2>
    <p className="text-sm leading-relaxed text-muted">
      EXP-MAP-A01: {executionSummary(snapshot.candidate.gateState)}
      {" "}Controlled support: {String(snapshot.candidate.gateState.controlledSupportEligible)};
      physical support: {String(snapshot.candidate.gateState.physicalSupportEligible)}.
    </p>
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
