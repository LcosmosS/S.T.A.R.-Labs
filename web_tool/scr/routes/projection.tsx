import { createFileRoute } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Formula, Metric } from "@/components/viz/formula";
import { EntropyField } from "@/components/viz/entropy-canvas";
import { OrbitCloud } from "@/components/viz/orbit-cloud";
import { FILAMENTS, PROJECTED } from "@/lib/star/physics";
import { catalogStats } from "@/lib/star/catalog";
import { useLab } from "@/lib/star/store";

export const Route = createFileRoute("/projection")({ component: ProjectionPage });

function ProjectionPage() {
  const selected = useLab((s) => s.selectedLabel);
  const set = useLab((s) => s.set);
  const stats = catalogStats();
  const curve = PROJECTED.find((c) => c.label === selected);

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="warn">ACSC · conjectural map</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Arithmetic projection Φ(E)</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Elliptic-curve invariants are placed on a 3-manifold by a density-equalizing map of log-conductor, with rank
          as a mild offset. The RTCH paper is careful: this does not establish that those invariants are thermodynamic
          fields. It supplies a possible Y^A(E) on which the cohomological machinery can act.
        </p>
      </header>

      <Formula boxed>Y^A ∼ (log N_E, log |Δ_E|, r_E, log R_E, log |Ω_E|, …)</Formula>

      <div className="grid gap-4 sm:grid-cols-3">
        <Metric label="Points" value={String(PROJECTED.length)} />
        <Metric label="Filaments" value={String(FILAMENTS.length)} hint="3-NN" />
        <Metric label="⟨entropy⟩" value={stats.meanEntropy.toFixed(2)} hint="log |Δ|" />
      </div>

      <section className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
        <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Φ(E) point cloud</div>
        <OrbitCloud
          points={PROJECTED}
          links={FILAMENTS}
          selected={selected}
          onSelect={(label) => set({ selectedLabel: label })}
          className="h-[min(52vh,440px)] w-full"
        />
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Entropy density</div>
          <EntropyField points={PROJECTED} className="h-56 w-full sm:h-72" />
        </div>
        <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">{curve?.label ?? "Select a curve"}</h2>
          {curve ? (
            <dl className="mt-4 grid grid-cols-2 gap-3 text-sm">
              <Item k="conductor N" v={String(curve.conductor)} />
              <Item k="rank" v={String(curve.rank)} />
              <Item k="regulator" v={curve.regulator.toFixed(5)} />
              <Item k="real period Ω" v={curve.omega.toFixed(5)} />
              <Item k="discriminant" v={String(curve.disc)} />
              <Item k="Faltings h" v={curve.faltingsHeight.toFixed(3)} />
              <Item k="torsion" v={curve.torsion} />
              <Item k="isogeny" v={curve.isogeny} />
            </dl>
          ) : (
            <p className="mt-3 text-sm text-muted">Click a point in the cloud.</p>
          )}
        </div>
      </section>
    </div>
  );
}

function Item({ k, v }: { k: string; v: string }) {
  return (
    <div>
      <dt className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">{k}</dt>
      <dd className="font-mono tabular-nums text-fg">{v}</dd>
    </div>
  );
}
