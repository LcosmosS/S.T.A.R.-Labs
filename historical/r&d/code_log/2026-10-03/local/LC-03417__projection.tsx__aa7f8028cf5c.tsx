import { createFileRoute } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { OrbitCloud } from "@/components/viz/orbit-cloud";
import { Formula, Metric, Sym } from "@/components/viz/formula";
import { getCatalog } from "@/lib/star/catalog";
import { FILAMENTS, PROJECTED } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";

export const Route = createFileRoute("/projection")({ component: ProjectionPage });

function ProjectionPage() {
  const selectedLabel = useLab((s) => s.selectedLabel);
  const set = useLab((s) => s.set);
  const curve = PROJECTED.find((c) => c.label === selectedLabel) ?? PROJECTED[0]!;
  const catalog = getCatalog();
  const ranks = [0, 1, 2, 3, 4].map((r) => catalog.filter((c) => c.rank === r).length);

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="steel">ACSC</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Arithmetic–cosmic projection</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          The Arithmetic–Cosmic Structure Conjecture maps elliptic-curve invariants into a cosmological manifold.
          Rank, log-conductor and regulator become coordinates; sinusoidal and oblate corrections implement the
          global-to-local mapping paradox.
        </p>
      </header>

      <Formula boxed>
        Φ(E): (<Sym>r</Sym>, log <Sym>N</Sym>, Reg) → (<Sym>x</Sym>, <Sym>y</Sym>, <Sym>z</Sym>)
      </Formula>

      <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
        <div className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <OrbitCloud
            points={PROJECTED}
            links={FILAMENTS}
            selected={curve.label}
            onSelect={(label) => set({ selectedLabel: label })}
            autoRotate={false}
            className="h-[min(56vh,520px)] w-full"
          />
        </div>
        <aside className="space-y-5 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Selected curve</div>
          <div className="font-display text-3xl tracking-tight">{curve.label}</div>
          <div className="grid grid-cols-2 gap-4">
            <Metric label="Conductor N" value={curve.conductor.toLocaleString()} />
            <Metric label="Rank r" value={String(curve.rank)} />
            <Metric label="Regulator" value={curve.regulator.toFixed(4)} />
            <Metric label="Real period Ω" value={curve.omega.toFixed(4)} />
            <Metric label="Discriminant Δ" value={curve.disc.toExponential(2)} />
            <Metric label="Torsion" value={curve.torsion} />
          </div>
          <div className="font-mono text-xs text-muted">
            a-invariants [{curve.ainvs.join(", ")}]
          </div>
          <div className="font-mono text-xs text-muted">Isogeny class {curve.isogeny}</div>
          <div className="grid grid-cols-2 gap-4 pt-2">
            <Metric label="Entropy log|Δ|" value={curve.entropy.toFixed(2)} />
            <Metric label="Coh. class" value={curve.cohClass.toExponential(2)} />
          </div>
        </aside>
      </div>

      <section>
        <h2 className="font-display text-2xl tracking-tight">Rank spectrum</h2>
        <p className="mt-2 max-w-2xl text-sm text-muted">
          Higher rank is locally over-sampled at low redshift in the Hubble lab, matching the S.T.A.R. claim that
          structure-rich patches of Φ(E) drive the late-time H_eff enhancement.
        </p>
        <div className="mt-5 grid grid-cols-5 gap-3">
          {ranks.map((n, r) => (
            <div key={r} className="rounded-lg bg-surface p-4 shadow-[var(--shadow-border)]">
              <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Rank {r}</div>
              <div className="mt-2 font-mono text-2xl tabular-nums">{n}</div>
              <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-elevated">
                <div className="h-full bg-primary" style={{ width: `${(n / catalog.length) * 100}%` }} />
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
