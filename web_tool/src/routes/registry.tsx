import { createFileRoute, Link } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Metric } from "@/components/viz/formula";
import snapshot from "@/lib/star/registry-snapshot.json";
import skyReleases from "../../content/sky-overlay-releases.v1.json";
import skyCandidates from "../../content/sky-overlay-candidates.v1.json";
import lfsSelection from "@/lib/star/recovered-lfs-snapshot.json";
import { getPreregisteredEntries, getPendingTheoryProtocols, isPreregisteredStatus } from "@/lib/star/experiment-lifecycle";

export const Route = createFileRoute("/registry")({ component: RegistryPage });

function downloadSnapshot() {
  const url = URL.createObjectURL(new Blob([`${JSON.stringify(snapshot, null, 2)}\n`], { type: "application/json" }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `starmap-registry-${snapshot.contentSha256.slice(0, 12)}.json`;
  anchor.click();
  URL.revokeObjectURL(url);
}

function RegistryPage() {
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const preregistered = useMemo(() => getPreregisteredEntries(snapshot), []);
  const pendingTheory = useMemo(() => getPendingTheoryProtocols(snapshot), []);
  const candidate = snapshot.candidate;
  const gates = candidate.gateState;
  const config = candidate.config;
  const rows = useMemo(() => {
    const value = query.trim().toLowerCase();
    return snapshot.experiments.filter((row) =>
      (statusFilter !== "preregistered" || isPreregisteredStatus(row.Status)) &&
      [row.Experiment_ID, row.Qualified_Experiment_ID, row.Claim_IDs, row.Dataset_ID, row.Status].some((field) => field.toLowerCase().includes(value)),
    );
  }, [query, statusFilter]);

  return (
    <div className="space-y-8">
      <header className="max-w-3xl">
        <Badge tone="steel">Read-only repository snapshot</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Research gates and provenance</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          This view copies canonical repository records and their source hashes into the deployed prototype.
          It reports recorded eligibility; it does not run preflight, execute experiments, edit registries, or promote
          scientific support. A passing website build or a saved demonstration does not establish scientific evidence.
        </p>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Snapshot updates require regenerating it from repository source and deploying a reviewed change.
          <Link to="/charter" className="ml-1 text-steel underline underline-offset-4">Read the canonical claim records</Link>.
        </p>
      </header>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Metric label="Recorded experiments" value={String(snapshot.experiments.length)} hint={snapshot.namespace} />
        <Metric label="Preregistered protocols" value={String(preregistered.length)} hint="Numerical + theory records; not execution" />
        <Metric label="Execution eligible" value={String(snapshot.declaredExecutionEligibleCount)} hint="Declared registry flags; not a runner preflight" />
        <Metric label="Canonical claims" value={String(snapshot.claims.length)} hint="Support eligibility remains separately recorded" />
        <Metric label="Admitted sky releases" value={String(skyReleases.sources.length)} hint="Reviewed display-only; no inference" />
      </div>

      <section id="preregistered-summary" className="space-y-3">
        <h2 className="font-display text-2xl tracking-tight">Preregistered research protocols</h2>
        <p className="max-w-3xl text-sm leading-relaxed text-muted">
          Formal preregistration labels are derived from versioned canonical registry states,
          not inferred from source-folder names. A preregistered design may still have planned
          sub-stages and no controlled execution permission. Theory obstructions are distinct
          from numerical controlled experiments.
        </p>
        <div className="grid gap-3 md:grid-cols-2">
          {preregistered.map((entry) => (
            <article key={entry.namespace + ":" + entry.id} className="min-w-0 rounded-xl bg-surface p-4 shadow-[var(--shadow-border)]">
              <Badge tone="steel">{entry.status}</Badge>
              <h3 className="mt-2 font-mono text-sm">{entry.id}</h3>
              <p className="mt-1 text-xs text-muted">{entry.kind} · {entry.namespace}</p>
              <p className="mt-2 text-xs text-muted">Preregistration is not controlled execution, independent proof, or physical support.</p>
              {entry.protocolPath ? (
                <a className="mt-2 inline-block text-xs text-steel underline underline-offset-4"
                  href={`https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/${entry.protocolPath}`}
                  target="_blank" rel="noopener noreferrer">Review frozen protocol</a>
              ) : null}
            </article>
          ))}
        </div>
        {pendingTheory.length > 0 ? (
          <div className="mt-4 space-y-3">
            <h3 className="font-display text-lg">Frozen protocols pending formal status review</h3>
            <p className="max-w-3xl text-xs leading-relaxed text-muted">
              A registered protocol file is not proof of formal preregistration approval.
              These records remain planned in the canonical registry until independent review
              authorizes a transition.
            </p>
            {pendingTheory.map((entry) => (
              <article key={entry.id} className="rounded-xl border border-border bg-surface p-4">
                <Badge tone="warn">Frozen protocol on file · registry: {entry.status}</Badge>
                <h4 className="mt-2 font-mono text-sm">{entry.id}</h4>
                <p className="mt-2 text-xs text-muted">No execution authorization or independent theorem certification.</p>
                <a className="mt-2 inline-block text-xs text-steel underline underline-offset-4"
                  href={`https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/${entry.protocolPath}`}
                  target="_blank" rel="noopener noreferrer">Read frozen protocol</a>
              </article>
            ))}
          </div>
        ) : null}
      </section>

      <section id="sky-admission" className="space-y-3 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <h2 className="font-display text-xl">ALADIN Lite sky-release admission</h2>
        <p className="max-w-3xl text-sm leading-relaxed text-muted">
          The CI `sky:check` gate verifies publisher-source receipts, exact hydrated data bytes,
          the hashed coordinate derivative and the committed reviewer decision. Only a
          separately authorized release-manifest transition can make a sky dataset selectable.
          CI passing is not, by itself, independent scientific authorization.
        </p>
        <p role="status" className="text-sm">
          Currently {skyReleases.sources.length} dataset release(s) admitted for display.
        </p>
        {skyCandidates.candidates.map((candidate) => (
          <p key={candidate.datasetId} className="text-xs text-muted">
            <span className="font-mono">{candidate.datasetId}</span> · Candidate status: {candidate.approvalStatus}
            {" · "}No inference or physical-support promotion
          </p>
        ))}
        <a href="https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/web_tool/content/sky-overlay-releases.v1.json"
          className="inline-block text-xs text-steel underline underline-offset-4" target="_blank" rel="noopener noreferrer">
          Inspect exact committed release manifest
        </a>
      </section>

      <section id="archival-lfs" className="space-y-4">
        <h2 className="font-display text-2xl tracking-tight">Selected historical LFS sources</h2>
        <p className="max-w-3xl text-sm leading-relaxed text-muted">
          These are five already uploaded and independently downloaded archival source candidates from PR #51,
          not new LFS uploads. Their local byte identities are recorded, but upstream catalog lineage and any
          experiment-ready association remain unverified. The separate candidate selection does not change
          this page’s canonical dataset or experiment gates.
        </p>
        <div className="grid gap-3 lg:grid-cols-2">
          {lfsSelection.assets.map((asset) => (
            <article key={asset.artifactId} className="min-w-0 rounded-xl bg-surface p-4 shadow-[var(--shadow-border)]">
              <Badge tone="warn">Historical · not controlled</Badge>
              <h3 className="mt-2 break-all font-mono text-xs">{asset.artifactId}</h3>
              <p className="mt-2 text-xs text-muted">{asset.kind.toUpperCase()} · {asset.bytes.toLocaleString()} bytes</p>
              <p className="mt-2 break-all font-mono text-[10px] text-muted">SHA-256: {asset.sha256}</p>
              <p className="mt-2 break-all text-xs text-muted">{asset.recoveredSource}</p>
              <p className="mt-2 text-xs text-muted">
                Execution: {String(asset.controlledExecutionEligible)} · Controlled support: {String(asset.controlledSupportEligible)}
                {" · "}Physical support: {String(asset.physicalSupportEligible)}
              </p>
            </article>
          ))}
        </div>
        <p className="text-xs text-muted">
          <a href="https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/registry/recovered_lfs_selection_v0.1.json"
             target="_blank" rel="noopener noreferrer" className="text-steel underline underline-offset-4">
             Read the separate versioned selection registry
          </a>
          . No raw survey data or serialized model is loaded in the browser.
        </p>
      </section>

      <section id="preregistrations" className="space-y-4">
        <div>
          <h2 className="font-display text-2xl tracking-tight">Theory preregistrations</h2>
          <p className="mt-2 text-sm leading-relaxed text-muted">
            Preregistered or planned obstruction and parent-theory programs in THEORY-SEARCH-v0.1.
            Protocol status, each stage's progress, and all execution/support gates are displayed
            separately. Theory registration does not establish a controlled statistical experiment.
          </p>
        </div>
        <div className="grid gap-4 lg:grid-cols-2">
          {snapshot.preregistrations.map((preregistration) => {
            const record = preregistration.record;
            const preregistrationGates = preregistration.gateState;
            return (
              <article key={preregistration.id} id={preregistration.id} className="min-w-0 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
                <Badge tone={isPreregisteredStatus(record.Status) ? "steel" : "warn"}>
                  {record.Status === "planned" ? "Frozen protocol on file · registry planned" : record.Status}
                </Badge>
                <h3 className="mt-3 font-display text-xl tracking-tight">{preregistration.id}</h3>
                <p className="mt-2 text-sm leading-relaxed">{record.Name}</p>
                <p className="mt-3 text-sm leading-relaxed text-muted">
                  {"Primary_Question" in record ? record.Primary_Question : record.Terminal_Conclusion}
                </p>
                <dl className="mt-4 grid gap-4 sm:grid-cols-2">
                  <Gate label="Registry identity" value={preregistration.qualifiedId} />
                  <Gate label="Claim" value={record.Claim_ID} />
                  <Gate label="Controlled execution eligible" value={String(preregistrationGates.controlledExecutionEligible)} />
                  <Gate label="Controlled support eligible" value={String(preregistrationGates.controlledSupportEligible)} />
                  <Gate label="Physical support eligible" value={String(preregistrationGates.physicalSupportEligible)} />
                  <Gate label="Universal no-go claim" value={String(record.Universal_NoGo_Claim)} />
                </dl>
                {preregistration.stages.length > 0 ? (
                  <dl className="mt-4 grid gap-4 sm:grid-cols-3">
                    {preregistration.stages.map((stage) => <Gate key={stage.name} label={stage.name} value={stage.status} />)}
                  </dl>
                ) : typeof record.Candidate_Count === "string" && typeof record.Observable_Embargo === "string" ? (
                  <dl className="mt-4 grid gap-4 sm:grid-cols-2">
                    <Gate label="Registered candidates" value={record.Candidate_Count} />
                    <Gate label="Observable embargo" value={record.Observable_Embargo} />
                  </dl>
                ) : null}
                {preregistration.candidates.length > 0 ? (
                  <ul className="mt-4 space-y-3 text-sm leading-relaxed" aria-label={`${preregistration.id} candidates`}>
                    {preregistration.candidates.map((theory) => (
                      <li key={theory.Qualified_Candidate_ID}>
                        <span className="font-mono text-xs">{theory.Candidate_ID}</span> · {theory.Name}
                        <span className="mt-1 block break-all font-mono text-xs text-muted">{theory.Audit_Status}</span>
                      </li>
                    ))}
                  </ul>
                ) : null}
                <p className="mt-4 text-xs leading-relaxed text-muted">{record.Notes}</p>
                <a className="mt-4 inline-block py-2 text-sm text-steel underline underline-offset-4" href={`https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/${preregistration.protocolPath}`}>
                  Read the full {preregistration.id} protocol
                </a>
                <dl className="mt-3">
                  <Gate label="Protocol SHA-256 in this snapshot" value={preregistration.protocolSha256} />
                </dl>
              </article>
            );
          })}
        </div>
      </section>

      <section className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <Badge tone="warn">{candidate.records.experiment.Status}</Badge>
            <h2 className="mt-2 font-display text-2xl tracking-tight">{candidate.id}</h2>
            <p className="mt-1 break-all font-mono text-[11px] text-muted">{candidate.records.experiment.Qualified_Experiment_ID}</p>
          </div>
          <Button variant="secondary" onClick={downloadSnapshot}>Download registry snapshot</Button>
        </div>
        <p className="mt-4 text-sm leading-relaxed text-muted">{candidate.records.experiment.Current_Audit_Assessment}</p>
        <dl className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <Gate label="Experiment execution eligible" value={String(gates.experimentExecutionEligible)} />
          <Gate label="Dataset execution eligible" value={String(gates.datasetExecutionEligible)} />
          <Gate label="Controlled support eligible" value={String(gates.controlledSupportEligible)} />
          <Gate label="Physical support eligible" value={String(gates.physicalSupportEligible)} />
          <Gate label="Source provenance status" value={gates.provenanceStatus} />
          <Gate label="Parameter / null preregistration" value={`${gates.parameterPreregistrationStatus} / ${gates.nullPreregistrationStatus}`} />
        </dl>
        <p className="mt-4 text-sm leading-relaxed text-muted">
          Five registry-record hashes match the controlled specification; all three preregistration-file hashes and
          configuration match it. These binding checks do not verify a live execution environment or authorize a run.
        </p>
      </section>

      <section className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <h2 className="font-display text-2xl tracking-tight">Registered protocol and browser demonstration</h2>
        <p className="mt-2 text-sm text-muted">The browser demonstration is separate from {config.protocol_version}.</p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[600px] text-left text-sm">
            <thead className="text-muted">
              <tr><th className="py-3 pr-4">Property</th><th className="py-3 pr-4">EXP-MAP-A01</th><th className="py-3">Browser topology demonstration</th></tr>
            </thead>
            <tbody className="divide-y divide-border">
              <Comparison label="Inputs" registered={`${config.input.analysis_rows.toLocaleString("en-US")} first-isogeny representatives`} demo="12 handwritten + 148 seeded synthetic fixtures" />
              <Comparison label="Mapping" registered={`Fixed log coordinates; elevation = ${config.projection.rank_scale} × rank`} demo="Historical angle/regulator illustration and feature metric" />
              <Comparison label="Endpoint / neighbors" registered={`${config.endpoint.name}; k = ${config.endpoint.k}`} demo="H0 persistence and kNN graph cycles; k = 8" />
              <Comparison label="Nulls" registered={`${config.null.realizations} fixed-base rank permutations`} demo="18 independent-column permutations" />
              <Comparison label="Generator / seed" registered={`${config.null.prng}; seed ${config.null.seed}`} demo="Mulberry32; exploratory rerunnable seeds" />
              <Comparison label="Inference" registered={`Single one-sided endpoint; α = ${config.inference.alpha}`} demo="Diagnostic p-values; minimum 1/19 ≈ 0.053" />
              <Comparison label="Scientific status" registered="Preregistered; execution gate remains separately controlled" demo="Educational; unregistered; no controlled or physical support" />
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Registered source identity</h2>
          <p className="mt-3 text-sm leading-relaxed text-muted">{candidate.records.provenance.Source_Name}</p>
          <p className="mt-2 text-sm leading-relaxed text-muted">{candidate.manifest.experiment_selection.policy}</p>
          <dl className="mt-4 space-y-3">
            <Gate label="Upstream revision" value={candidate.manifest.source.git_commit} />
            <Gate label="Source rows" value={String(candidate.manifest.artifact.expected_rows)} />
            <Gate label="Source artifact" value={candidate.manifest.artifact.path} />
            <Gate label="Registered SHA-256" value={candidate.manifest.artifact.sha256} />
          </dl>
          <p className="mt-4 text-xs leading-relaxed text-muted">Source identity is copied from the manifest; the deployed website does not reacquire or rehash the source dataset.</p>
        </article>
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Bound registry records</h2>
          <dl className="mt-4 space-y-3">
            {Object.entries(candidate.recordSha256).map(([name, digest]) => <Gate key={name} label={`${name} SHA-256`} value={digest} />)}
          </dl>
        </article>
      </section>

      <section className="space-y-4">
        <div>
          <h2 className="font-display text-2xl tracking-tight">Recorded experiment eligibility</h2>
          <p className="mt-2 text-sm text-muted">Flags are copied verbatim from experiment_registry_v0.2.csv. Search never changes a gate.</p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <Input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search experiment, dataset, claim, or status" aria-label="Search experiment registry" />
          <label className="flex items-center gap-2 text-xs text-muted">
            Lifecycle
            <select aria-label="Filter experiment lifecycle" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}
              className="min-h-11 rounded-md border border-border bg-elevated px-3 text-sm text-fg">
              <option value="all">All recorded experiments</option>
              <option value="preregistered">Preregistered only</option>
            </select>
          </label>
        </div>
        <div className="overflow-x-auto rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <table className="w-full min-w-[800px] text-left text-sm">
            <thead className="text-muted">
              <tr>
                {['Experiment', 'Status', 'Dataset', 'Execution', 'Controlled support', 'Physical support'].map((name) => <th key={name} className="px-4 py-3 text-xs font-medium">{name}</th>)}
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {rows.map((row) => (
                <tr key={row.Qualified_Experiment_ID}>
                  <td className="px-4 py-3 font-mono text-xs">{row.Experiment_ID}</td>
                  <td className="px-4 py-3"><Badge tone={isPreregisteredStatus(row.Status) ? "steel" : "warn"}>{row.Status}</Badge></td>
                  <td className="px-4 py-3 font-mono text-xs text-muted">{row.Dataset_ID}</td>
                  <td className="px-4 py-3 font-mono text-xs">{row.Controlled_Execution_Eligible}</td>
                  <td className="px-4 py-3 font-mono text-xs">{row.Controlled_Support_Eligible}</td>
                  <td className="px-4 py-3 font-mono text-xs">{row.Physical_Support_Eligible}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {rows.length === 0 ? <p className="p-4 text-sm text-muted">No recorded experiments match this search.</p> : null}
        </div>
      </section>

      <section className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <h2 className="font-display text-2xl tracking-tight">Snapshot source hashes</h2>
        <p className="mt-2 break-all font-mono text-xs text-muted">Snapshot digest: {snapshot.contentSha256}</p>
        <p className="mt-2 text-sm text-muted">Generated from these {snapshot.sources.length} canonical files. The repository check fails if the website copy becomes stale.</p>
        <dl className="mt-4 space-y-4">
          {snapshot.sources.map((source) => <Gate key={source.path} label={source.path} value={source.sha256} />)}
        </dl>
      </section>
    </div>
  );
}

function Gate({ label, value }: { label: string; value: string }) {
  return <div><dt className="break-words text-xs text-muted">{label}</dt><dd className="mt-1 break-all font-mono text-xs text-fg">{value}</dd></div>;
}

function Comparison({ label, registered, demo }: { label: string; registered: string; demo: string }) {
  return <tr><th scope="row" className="py-3 pr-4 text-xs font-medium text-muted">{label}</th><td className="py-3 pr-4 text-xs">{registered}</td><td className="py-3 text-xs text-muted">{demo}</td></tr>;
}
