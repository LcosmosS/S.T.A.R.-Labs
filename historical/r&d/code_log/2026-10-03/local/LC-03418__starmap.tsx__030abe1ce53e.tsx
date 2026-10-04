import { createFileRoute } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { EntropyField } from "@/components/viz/entropy-canvas";
import { OrbitCloud } from "@/components/viz/orbit-cloud";
import { Metric } from "@/components/viz/formula";
import { CLUSTERS, KAPPA_UCF } from "@/lib/star/catalog";
import { FILAMENTS, PROJECTED } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";

export const Route = createFileRoute("/starmap")({ component: StarMapPage });

function StarMapPage() {
  const selectedLabel = useLab((s) => s.selectedLabel);
  const set = useLab((s) => s.set);
  const selected = PROJECTED.find((p) => p.label === selectedLabel);
  const highRank = PROJECTED.filter((p) => p.rank >= 2).length;
  const meanEnt = PROJECTED.reduce((s, p) => s + p.entropy, 0) / PROJECTED.length;

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="steel">S.T.A.R.M.A.P.</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Cosmic cartography</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          High-fidelity topography of the arithmetic sky: filaments from nearest-neighbour persistence on Φ(E),
          entropy field M(x) as a kernel density of log|Δ|, and supercluster anchors from the UCF scaling a ≈ −κ r.
        </p>
      </header>

      <div className="grid gap-4 sm:grid-cols-3">
        <Metric label="Filaments" value={String(FILAMENTS.length)} hint="k = 3 persistence edges" />
        <Metric label="Rank ≥ 2" value={String(highRank)} hint="local structure bias" />
        <Metric label="⟨log|Δ|⟩" value={meanEnt.toFixed(2)} hint="entropy proxy" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <figure className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <figcaption className="px-4 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">
            Arithmetic cosmic web
          </figcaption>
          <OrbitCloud
            points={PROJECTED}
            links={FILAMENTS}
            selected={selectedLabel}
            onSelect={(label) => set({ selectedLabel: label })}
            className="h-[360px] w-full"
          />
        </figure>
        <figure className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <figcaption className="px-4 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">
            Entropy field M(x) · rank ≥ 2 marked
          </figcaption>
          <EntropyField points={PROJECTED} className="h-[360px] w-full" />
        </figure>
      </div>

      {selected ? (
        <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Focused curve</div>
          <div className="mt-1 font-display text-2xl">{selected.label}</div>
          <p className="mt-2 text-sm text-muted">
            Rank {selected.rank}, conductor {selected.conductor.toLocaleString()}, Ω = {selected.omega.toFixed(4)}.
            Entropy proxy log|Δ| = {selected.entropy.toFixed(2)}.
          </p>
        </div>
      ) : null}

      <section>
        <h2 className="font-display text-2xl tracking-tight">UCF cluster lattice</h2>
        <p className="mt-2 max-w-2xl text-sm text-muted">
          Virgo is the geometric origin (r = 54 Mly, a = −1706) with data-driven κ = {KAPPA_UCF}. Comoving volumes and
          cohomology classes follow entropy × (rank + 1) / √r.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          {CLUSTERS.map((c) => (
            <article key={c.name} className="rounded-xl bg-surface p-4 shadow-[var(--shadow-border)]">
              <div className="font-display text-xl tracking-tight">{c.name}</div>
              <div className="mt-3 space-y-2 font-mono text-xs tabular-nums text-muted">
                <div className="flex justify-between">
                  <span>r</span>
                  <span className="text-fg">{c.rMly} Mly</span>
                </div>
                <div className="flex justify-between">
                  <span>a</span>
                  <span className="text-fg">{c.derivedA}</span>
                </div>
                <div className="flex justify-between">
                  <span>H factor</span>
                  <span className="text-fg">{c.hFactor.toFixed(4)}</span>
                </div>
                <div className="flex justify-between">
                  <span>rank</span>
                  <span className="text-fg">{c.rank}</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
