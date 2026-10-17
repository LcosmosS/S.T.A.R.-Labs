import { createFileRoute } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Formula, Metric } from "@/components/viz/formula";
import { EntropyField } from "@/components/viz/entropy-canvas";
import { OrbitCloud } from "@/components/viz/orbit-cloud";
import { FrozenSkyOverlay } from "@/components/viz/frozen-sky-overlay";
import { FILAMENTS, PROJECTED } from "@/lib/star/physics";
import { catalogStats } from "@/lib/star/catalog";
import { useLab } from "@/lib/star/store";
import { RepositoryStatus } from "@/components/repository-status";

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
          This historical 2_STARMAP.md illustration maps discriminant and conductor to angles, and regulator to radius.
          It uses 12 handwritten illustrative entries and 148 deterministic synthetic fixtures. Generated features
          depend on rank, so omitting a direct rank axis does not establish independence. The registered EXP-MAP-A01
          map, dataset, and null protocol are separate; no registered experiment runs here.
        </p>
      </header>

      <section aria-label="EXP-MAP-A01 primary execution evidence" className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <div className="flex flex-wrap items-center gap-2">
          <Badge>Verified primary execution · EXP-MAP-A01</Badge>
          <Badge tone="warn">Not independently replicated</Badge>
        </div>
        <h2 className="mt-3 font-display text-2xl tracking-tight">A01 arithmetic projection evidence</h2>
        <p className="mt-2 text-sm leading-relaxed text-muted">
          The preserved primary run analyzed 38,042 elliptic-curve representatives (64,687 source rows).
          Its locked k=10 arithmetic neighbor statistic was T = -114.40183841751903, with 0 of
          999 rank-permutation null statistics at least as extreme (one-sided p = 0.001; alpha = 0.01).
          This rejects only NULL-MAP-001. It does not establish a cosmological correspondence,
          independent reproduction, or controlled/physical support eligibility.
        </p>
        <p className="mt-3 text-sm text-muted">
          The point cloud below remains the separate illustrative/synthetic fixture display,
          <strong> not </strong> the 38,042-row A01 projection. Do not interpret it as observed A01 coordinates.
        </p>
        <div className="mt-4 flex flex-wrap gap-4 text-sm">
          <a className="text-primary underline underline-offset-4" href="https://github.com/LcosmosS/S.T.A.R.-Labs/tree/main/release_packages/EXP-MAP-A01-primary-execution-v0.1">
            Inspect immutable primary package
          </a>
          <a className="text-primary underline underline-offset-4" href="https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/release_packages/EXP-MAP-A01-primary-execution-v0.1/20261016T041335361140Z-e60fd05117fc/observed_projection.csv">
            Inspect A01 projection CSV
          </a>
          <a className="text-primary underline underline-offset-4" href="https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/release_packages/EXP-MAP-A01-primary-execution-v0.1/20261016T041335361140Z-e60fd05117fc/null_statistics.csv">
            Inspect null statistics
          </a>
        </div>
      </section>

      <RepositoryStatus />

      <Formula boxed>Y^A ∼ (log N_E, log |Δ_E|, r_E, log R_E, log |Ω_E|, …)</Formula>

      <div className="grid gap-4 sm:grid-cols-3">
        <Metric label="Points" value={String(PROJECTED.length)} />
        <Metric label="Graph links" value={String(FILAMENTS.length)} hint="3-NN illustration" />
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

      <FrozenSkyOverlay />

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
