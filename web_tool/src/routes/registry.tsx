import { createFileRoute, Link } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Metric } from "@/components/viz/formula";
import snapshot from "@/lib/star/registry-snapshot.json";

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
  const candidate = snapshot.candidate;
  const gates = candidate.gateState;
  const config = candidate.config;
  const rows = useMemo(() => {
    const value = query.trim().toLowerCase();
    return snapshot.experiments.filter((row) =>
      [row.Experiment_ID, row.Qualified_Experiment_ID, row.Claim_IDs, row.Dataset_ID, row.Status].some((field) => field.toLowerCase().includes(value)),
    );
  }, [query]);

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

      <div className="grid gap-4 sm:grid-cols-3">
        <Metric label="Recorded experiments" value={String(snapshot.experiments.length)} hint={snapshot.namespace} />
        <Metric label="Execution eligible" value={String(snapshot.declaredExecutionEligibleCount)} hint="Declared registry flags; not a runner preflight" />
        <Metric label="Canonical claims" value={String(snapshot.claims.length)} hint="Support eligibility remains separately recorded" />
      </div>

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
        <Input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search experiment, dataset, claim, or status" aria-label="Search experiment registry" />
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
                  <td className="px-4 py-3"><Badge>{row.Status}</Badge></td>
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
