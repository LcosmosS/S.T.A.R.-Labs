import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CLAIMS, CORE_QUESTIONS, type ClaimStatus } from "@/lib/star/claims";

export const Route = createFileRoute("/charter")({ component: CharterPage });

const STATUS_TONE: Record<ClaimStatus, "default" | "steel" | "warn" | "ok" | "danger"> = {
  "ACTIVE TEST": "steel",
  EXPLORATORY: "warn",
  PRELIMINARY: "warn",
  OPEN: "default",
  SUPPORTED: "ok",
  SPECULATIVE: "warn",
  RECLASSIFIED: "default",
  FALSIFIED: "danger",
  DERIVED: "ok",
};

function CharterPage() {
  const [q, setQ] = useState("");
  const [status, setStatus] = useState<ClaimStatus | "all">("all");
  const rows = useMemo(() => {
    const query = q.trim().toLowerCase();
    return CLAIMS.filter((c) => {
      if (status !== "all" && c.status !== status) return false;
      if (!query) return true;
      return (
        c.id.toLowerCase().includes(query) ||
        c.statement.toLowerCase().includes(query) ||
        c.module.toLowerCase().includes(query)
      );
    });
  }, [q, status]);

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge>Research Charter v1</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">What S.T.A.R. actually asks</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          The project is not “elliptic curves determine the universe.” It asks whether arithmetic invariants can be
          mapped into geometric and topological structures that produce statistically nontrivial, reproducible
          correspondence with independent astronomical data.
        </p>
      </header>

      <Tabs defaultValue="charter">
        <TabsList className="flex w-full flex-wrap">
          <TabsTrigger value="charter">Charter</TabsTrigger>
          <TabsTrigger value="registry">Claim registry</TabsTrigger>
        </TabsList>

        <TabsContent value="charter" className="mt-6 space-y-8">
          <section className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
            <h2 className="font-display text-xl tracking-tight">The program does not assume</h2>
            <ul className="mt-3 grid gap-2 text-sm leading-relaxed text-muted sm:grid-cols-2">
              <li>Elliptic curves generate cosmic structure.</li>
              <li>Rank is cosmic time or gravitational potential.</li>
              <li>Arithmetic replaces Einstein’s equations.</li>
              <li>Dark matter is torsion; dark energy is rank growth.</li>
              <li>A unique or bijective arithmetic-to-cosmic map exists.</li>
              <li>BSD is required for the mapping.</li>
            </ul>
          </section>

          <section>
            <h2 className="font-display text-2xl tracking-tight">Five core questions</h2>
            <ol className="mt-4 grid gap-3">
              {CORE_QUESTIONS.map((qst) => (
                <li key={qst.id} className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
                  <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-steel">{qst.id}</div>
                  <h3 className="mt-1 font-display text-xl tracking-tight">{qst.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted">{qst.body}</p>
                </li>
              ))}
            </ol>
          </section>

          <section className="grid gap-4 md:grid-cols-3">
            <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
              <Badge tone="ok">Layer I</Badge>
              <h3 className="mt-2 font-display text-lg">Empirical structure</h3>
              <p className="mt-2 text-sm text-muted">Does it correspond? Rank, topology, SFR, density — with nulls.</p>
            </article>
            <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
              <Badge tone="steel">Layer II–III</Badge>
              <h3 className="mt-2 font-display text-lg">Geometry, then physics</h3>
              <p className="mt-2 text-sm text-muted">Build h_arith and F_arith as mathematics first. Compare to fields later.</p>
            </article>
            <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
              <Badge>Layer IV</Badge>
              <h3 className="mt-2 font-display text-lg">First principles last</h3>
              <p className="mt-2 text-sm text-muted">RTCH, ECC, and H₀ are downstream of independent correspondence.</p>
            </article>
          </section>

          <blockquote className="rounded-xl bg-elevated p-5 font-display text-lg leading-snug tracking-tight shadow-[var(--shadow-border)]">
            Do not ask whether the theory can be made to fit the universe. Ask whether a fixed mathematical construction
            predicts structure that was not used to construct it.
          </blockquote>
        </TabsContent>

        <TabsContent value="registry" className="mt-6 space-y-6">
          <p className="max-w-2xl text-sm leading-relaxed text-muted">
            Historical statements are preserved. Their scientific status is set by the Charter, not by the original
            wording. A claim is not evidence for the claim.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search claim id or text" aria-label="Search claims" />
            <div className="flex flex-wrap gap-1">
              {(["all", "ACTIVE TEST", "DERIVED", "SUPPORTED", "EXPLORATORY", "SPECULATIVE", "FALSIFIED"] as const).map(
                (s) => (
                  <button
                    key={s}
                    type="button"
                    onClick={() => setStatus(s)}
                    className={`h-11 rounded-md px-3 text-xs ${status === s ? "bg-primary text-primary-fg" : "bg-elevated text-muted shadow-[var(--shadow-border)]"}`}
                  >
                    {s === "all" ? "All" : s}
                  </button>
                ),
              )}
            </div>
          </div>
          <div className="space-y-3">
            {rows.map((c) => (
              <article key={c.id} className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-mono text-xs text-fg">{c.id}</span>
                  <Badge>{c.module}</Badge>
                  <Badge>{c.category}</Badge>
                  <Badge tone={STATUS_TONE[c.status]}>{c.status}</Badge>
                </div>
                <p className="mt-3 text-sm leading-relaxed text-fg">{c.statement}</p>
                <p className="mt-2 text-xs leading-relaxed text-muted">{c.support}</p>
                <p className="mt-1 font-mono text-[10px] uppercase tracking-[0.12em] text-subtle">Next · {c.next}</p>
              </article>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
