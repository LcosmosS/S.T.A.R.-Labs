import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Metric } from "@/components/viz/formula";
import { BarcodeCanvas, PcaCanvas, RankWebCanvas } from "@/components/viz/barcode-canvas";
import { runExperiment, type ExperimentResult } from "@/lib/star/rtch-e1";
import { runRankWeb, type RankWebResult } from "@/lib/star/rank-web";

export const Route = createFileRoute("/experiment")({ component: ExperimentPage });

type Kind = "catalog" | "torus" | "scrambled";

function ExperimentPage() {
  const [kind, setKind] = useState<Kind>("catalog");
  const [version, setVersion] = useState(0);
  const [busy, setBusy] = useState(false);
  const [webSeed, setWebSeed] = useState(0);

  const result = useMemo(() => {
    void version;
    return runExperiment({ kind, nNulls: 18, k: 8, nPairs: 28, seed: 20260917 + version });
  }, [kind, version]);

  const web = useMemo(() => runRankWeb(240, 20260919 + webSeed), [webSeed]);

  function rerun(next: Kind) {
    setBusy(true);
    setKind(next);
    setVersion((v) => v + 1);
    requestAnimationFrame(() => setBusy(false));
  }

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="steel">Active tests</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Falsifiable structure</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Two locked experiments. Topology treats rank as held-out of the metric. Rank–web asks whether rank tracks
          local-density environment on Φ(E). Neither is a proof that elliptic curves generate cosmic structure.
        </p>
      </header>

      <Tabs defaultValue="topology">
        <TabsList className="flex w-full flex-wrap">
          <TabsTrigger value="topology">RTCH-E1 topology</TabsTrigger>
          <TabsTrigger value="rankweb">Rank–web H₁–H₃</TabsTrigger>
        </TabsList>

        <TabsContent value="topology" className="mt-6 space-y-8">
          <TopologyPanel result={result} kind={kind} busy={busy} onRerun={rerun} />
        </TabsContent>

        <TabsContent value="rankweb" className="mt-6 space-y-8">
          <RankWebPanel result={web} onShuffle={() => setWebSeed((s) => s + 1)} />
        </TabsContent>
      </Tabs>
    </div>
  );
}

function TopologyPanel({
  result,
  kind,
  busy,
  onRerun,
}: {
  result: ExperimentResult;
  kind: Kind;
  busy: boolean;
  onRerun: (k: Kind) => void;
}) {
  return (
    <>
      <p className="max-w-2xl text-sm leading-relaxed text-muted">
        A persistent feature of a finite point cloud is evidence at a scale — not a proof that the arithmetic state
        space is a manifold with H^k ≠ 0. Rank is held out of the metric. Structure is compared to N1: independent
        column permutation, preserving every marginal.
      </p>

      <div className="flex flex-wrap gap-2">
        <Button size="sm" variant={kind === "catalog" ? "default" : "secondary"} onClick={() => onRerun("catalog")}>
          Catalog
        </Button>
        <Button size="sm" variant={kind === "torus" ? "default" : "secondary"} onClick={() => onRerun("torus")}>
          Torus control
        </Button>
        <Button size="sm" variant={kind === "scrambled" ? "default" : "secondary"} onClick={() => onRerun("scrambled")}>
          N1 scramble
        </Button>
      </div>

      <Verdict result={result} busy={busy} />

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="n" value={String(result.n)} hint={`${result.features.length} features`} />
        <Metric label="H0 max pers." value={result.h0Max.toFixed(3)} hint={`p = ${result.nullH0.p.toFixed(3)} vs N1`} />
        <Metric label="kNN β₁" value={String(result.betti1)} hint={`p = ${result.nullBetti.p.toFixed(3)}`} />
        <Metric label="⟨tortuosity⟩" value={result.geodesic.meanTort.toFixed(3)} hint={`p = ${result.nullTort.p.toFixed(3)}`} />
      </div>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">H0 persistence</div>
          <BarcodeCanvas intervals={result.intervals} className="h-56 w-full" />
        </div>
        <div className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Scalar embedding</div>
          <PcaCanvas points={result.pca} className="h-56 w-full" />
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Null protocol</h2>
          <ul className="mt-3 space-y-2 text-sm leading-relaxed text-muted">
            <li>N1 — independently permute each intrinsic column.</li>
            <li>Primary features: log N, sgn log |Δ|, log |j|, Faltings height, log R.</li>
            <li>Graph geodesics exclude direct kNN neighbors, so reported tortuosity is a multi-edge path.</li>
            <li>Positive control uses a sampled torus in R³, not Fibonacci or golden-ratio maps.</li>
          </ul>
        </article>
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Geodesic sample</h2>
          <div className="mt-3 overflow-x-auto">
            <table className="w-full text-left font-mono text-[11px]">
              <thead className="text-subtle">
                <tr>
                  <th className="py-1 pr-3">i</th>
                  <th className="py-1 pr-3">j</th>
                  <th className="py-1 pr-3">graph</th>
                  <th className="py-1 pr-3">chord</th>
                  <th className="py-1">τ</th>
                </tr>
              </thead>
              <tbody>
                {result.geodesic.pairs.slice(0, 6).map((p) => (
                  <tr key={`${p.i}-${p.j}`} className="text-fg">
                    <td className="py-1 pr-3 tabular-nums">{p.i}</td>
                    <td className="py-1 pr-3 tabular-nums">{p.j}</td>
                    <td className="py-1 pr-3 tabular-nums">{p.graph.toFixed(3)}</td>
                    <td className="py-1 pr-3 tabular-nums">{p.chord.toFixed(3)}</td>
                    <td className="py-1 tabular-nums">{p.tortuosity.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>
      </section>

      <section>
        <h2 className="font-display text-xl tracking-tight">Caveats</h2>
        <ul className="mt-3 max-w-2xl space-y-2 text-sm leading-relaxed text-muted">
          {result.caveats.map((c) => (
            <li key={c}>{c}</li>
          ))}
        </ul>
      </section>
    </>
  );
}

function RankWebPanel({ result, onShuffle }: { result: RankWebResult; onShuffle: () => void }) {
  const envOrder = ["void", "filament", "cluster"] as const;
  const rankLabels = ["rank 0", "rank 1", "rank ≥2"];
  return (
    <>
      <p className="max-w-2xl text-sm leading-relaxed text-muted">
        ACSC-008 / CROSS-001: does arithmetic rank track cosmic-web morphology? Environments are kNN-density tertiles
        on Φ(E) — a geometric analogue of void / filament / cluster, not a survey classification. The null shuffles
        ranks while freezing the point cloud.
      </p>

      <div className="flex flex-wrap items-center gap-2">
        <Button size="sm" variant="secondary" onClick={onShuffle}>
          Reshuffle null seed
        </Button>
        <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">
          {result.nPerm} permutations
        </span>
      </div>

      <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <div className="flex flex-wrap items-center gap-2">
          <Badge tone={result.p < 0.05 ? "warn" : "ok"}>{result.p < 0.05 ? "associated" : "null-consistent"}</Badge>
          <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">
            χ² = {result.chi2.toFixed(2)} · p = {result.p.toFixed(3)}
          </span>
        </div>
        <p className="mt-3 text-sm leading-relaxed text-fg">{result.verdict}</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="n" value={String(result.n)} hint="Φ(E) points" />
        <Metric label="χ²" value={result.chi2.toFixed(2)} hint={`null ⟨χ²⟩ ${result.permMean.toFixed(2)}`} />
        <Metric label="p (shuffle)" value={result.p.toFixed(3)} hint={`${result.nPerm} perms`} />
        <Metric
          label="⟨r⟩ cluster"
          value={result.meanRank.cluster.toFixed(2)}
          hint={`void ${result.meanRank.void.toFixed(2)}`}
        />
      </div>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">
            Rank vs local density
          </div>
          <RankWebCanvas points={result.environments} className="h-56 w-full" />
        </div>
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Rank × environment</h2>
          <p className="mt-1 font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">Counts on Φ(E)</p>
          <div className="mt-3 overflow-x-auto">
            <table className="w-full text-left font-mono text-[11px]">
              <thead className="text-subtle">
                <tr>
                  <th className="py-1 pr-3" />
                  {envOrder.map((e) => (
                    <th key={e} className="py-1 pr-3 capitalize">
                      {e}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.table.map((row, i) => (
                  <tr key={rankLabels[i]} className="text-fg">
                    <td className="py-1 pr-3 text-muted">{rankLabels[i]}</td>
                    {row.map((n, j) => (
                      <td key={`${i}-${j}`} className="py-1 pr-3 tabular-nums">
                        {n}
                      </td>
                    ))}
                  </tr>
                ))}
                <tr className="text-muted">
                  <td className="py-1 pr-3">n</td>
                  {envOrder.map((e) => (
                    <td key={e} className="py-1 pr-3 tabular-nums">
                      {result.counts[e]}
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
          <ul className="mt-4 space-y-1 text-sm leading-relaxed text-muted">
            <li>Mean rank · void {result.meanRank.void.toFixed(2)}</li>
            <li>Mean rank · filament {result.meanRank.filament.toFixed(2)}</li>
            <li>Mean rank · cluster {result.meanRank.cluster.toFixed(2)}</li>
          </ul>
        </article>
      </section>

      <section>
        <h2 className="font-display text-xl tracking-tight">Caveats</h2>
        <ul className="mt-3 max-w-2xl space-y-2 text-sm leading-relaxed text-muted">
          <li>Density tertiles live in the arithmetic projection, not in a galaxy survey.</li>
          <li>A significant χ² is a geometric association on Φ — not an identification of rank with clusters.</li>
          <li>The catalog mixes named LMFDB curves with a synthetic fill; treat p-values as laboratory diagnostics.</li>
          <li>Locked alternative: shuffle ranks (done here). Next: alternative maps MCJ / PTD / FT as controls.</li>
        </ul>
      </section>
    </>
  );
}

function Verdict({ result, busy }: { result: ExperimentResult; busy: boolean }) {
  const tone = result.kind === "torus" ? "ok" : result.nullH0.p < 0.05 || result.nullBetti.p < 0.05 ? "warn" : "default";
  return (
    <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
      <div className="flex flex-wrap items-center gap-2">
        <Badge tone={tone}>{result.kind}</Badge>
        <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">
          {result.nNulls} nulls · k = {result.k}
          {busy ? " · running" : ""}
        </span>
      </div>
      <p className="mt-3 text-sm leading-relaxed text-fg">{result.verdict}</p>
    </div>
  );
}
