import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import content from "@/lib/star/research-content-snapshot.json";

export const Route = createFileRoute("/research")({ component: ResearchPage });
const LABELS: Record<string, string> = {
  illustrative_model: "Illustrative model",
  historical_exploratory: "Historical / unverified",
  derived_mathematics: "Mathematical derivation",
  archival_reference: "Archive reference only",
};
const SOURCE_BASE = "https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/";
function ResearchPage() {
  const [hydrated, setHydrated] = useState(false);
  useEffect(() => { setHydrated(true); }, []);
  const [query, setQuery] = useState("");
  const [kind, setKind] = useState("all");
  const items = useMemo(() => content.entries.filter(entry => {
    const text = [entry.title, entry.description, entry.expression, entry.id].join(" ").toLowerCase();
    return (kind === "all" || entry.kind === kind) && text.includes(query.toLowerCase().trim());
  }), [kind, query]);
  return <div className="space-y-8" data-research-hydrated={hydrated ? "true" : "false"}>
    <header className="max-w-3xl">
      <Badge tone="steel">Versioned, read-only catalog · {content.version}</Badge>
      <h1 className="mt-3 font-display text-4xl tracking-tight">Research constructs and source artifacts</h1>
      <p className="mt-3 text-sm leading-relaxed text-muted">
        Projections, formulae, diagrams, reductions and recovered notebook references are classified before display.
        A mathematical identity or archived computation is not evidence of an arithmetic–cosmic mechanism.
        No entry here authorizes a controlled run or establishes physical support.
      </p>
    </header>
    <div className="flex flex-col gap-3 sm:flex-row">
      <Input aria-label="Search research content" placeholder="Search constructs or sources" value={query} onChange={e => setQuery(e.target.value)} />
      <select aria-label="Filter research content type" className="min-h-11 rounded-md border border-border bg-elevated px-3 text-sm text-fg" value={kind} onChange={e => setKind(e.target.value)}>
        <option value="all">All types</option>
        <option value="projection">Projections</option>
        <option value="formula">Formulae</option>
        <option value="diagram">Diagrams</option>
        <option value="reduction">Reductions</option>
        <option value="notebook">Notebook references</option>
      </select>
    </div>
    <p role="status" className="text-xs text-muted">Displaying {items.length} of {content.entries.length} reviewed catalog records.</p>
    <section aria-label="Classified research entries" className="grid gap-4 xl:grid-cols-2">
      {items.map(entry => <article key={entry.id} className="min-w-0 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <div className="flex flex-wrap items-center gap-2">
          <Badge tone={entry.status === "derived_mathematics" ? "steel" : "warn"}>{LABELS[entry.status]}</Badge>
          <span className="font-mono text-[10px] uppercase tracking-widest text-subtle">{entry.kind} · {entry.epistemic} · {entry.id}</span>
        </div>
        <h2 className="mt-3 font-display text-xl tracking-tight">{entry.title}</h2>
        <p className="mt-3 break-words rounded-lg bg-elevated p-3 font-mono text-xs leading-relaxed text-fg">{entry.expression}</p>
        {entry.steps.length > 0 && <ol className="mt-3 flex flex-wrap items-center gap-2" aria-label="Conceptual diagram steps">
          {entry.steps.map((step, i) => <li key={step} className="rounded-md border border-border px-2 py-2 text-xs text-fg">{i + 1}. {step}{i < entry.steps.length - 1 ? " →" : ""}</li>)}
        </ol>}
        <p className="mt-3 text-sm leading-relaxed">{entry.description}</p>
        <p className="mt-3 text-xs leading-relaxed text-muted"><strong>Limit:</strong> {entry.caveat}</p>
        <p className="mt-3 text-xs text-muted">Controlled execution: false · Controlled support: false · Physical support: false</p>
        <a className="mt-4 inline-block break-all text-xs text-steel underline underline-offset-4" href={SOURCE_BASE + entry.sourcePath} target="_blank" rel="noopener noreferrer">
          View cited repository source
        </a>
      </article>)}
    </section>
    {items.length === 0 && <p className="text-sm text-muted">No entries match these filters.</p>}
    <footer className="max-w-3xl border-t border-border pt-5 text-xs leading-relaxed text-muted">
      Governed by STAR Research Charter v0.2. This separate interpretive catalog does not modify any canonical registry,
      preregistration, experimental record, scientific eligibility gate or archived source file.
      The source report used for the historical SFR context was user-provided, not uploaded as validated repository evidence.
    </footer>
  </div>;
}
