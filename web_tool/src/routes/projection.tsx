import { createFileRoute } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Formula, Metric } from "@/components/viz/formula";
import { EntropyField } from "@/components/viz/entropy-canvas";
import { OrbitCloud } from "@/components/viz/orbit-cloud";
import { FrozenSkyOverlay } from "@/components/viz/frozen-sky-overlay";
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
          This historical 2_STARMAP.md illustration maps discriminant and conductor to angles, and regulator to radius.
          It uses 12 handwritten illustrative entries and 148 deterministic synthetic fixtures. Generated features
          depend on rank, so omitting a direct rank axis does not establish independence. The registered EXP-MAP-A01
          map, dataset, and null protocol are separate; no registered experiment runs here.
        </p>
      </header>

      <section aria-label="Independent scientific review status" className="rounded-xl border border-border bg-surface p-5">
        <div className="flex items-center gap-3">
          <Badge tone="warn">Independent review required</Badge>
          <h2 className="text-sm font-medium text-fg">A01 activation and observational provenance are separate gates</h2>
        </div>
        <p className="mt-2 max-w-3xl text-sm leading-relaxed text-muted">
          The October 8, 2026 review docket found the source-locked A01 preflight technically passing.
          PR #64 was subsequently merged, setting execution eligibility true despite no recorded
          independent GitHub APPROVED review. Do not treat that transition as scientific approval or run A01
          before an independent governance resolution. SDSS provenance remains unknown; H I-MaNGA raw FITS
          source bytes are verified, but no observational coordinate release has been admitted. This viewer
          cannot convert a local file hash or a sky overlay into scientific evidence.
        </p>
        <p className="mt-2 text-xs text-muted">
          Governing document: <code>charter/STAR_Research_Charter_v0-2.pdf</code>. Inspect merged
          <a className="ml-1 underline underline-offset-2" href="https://github.com/LcosmosS/S.T.A.R.-Labs/pull/64" target="_blank" rel="noopener noreferrer">activation PR #64</a>
          {" · "}<a className="underline underline-offset-2" href="https://github.com/LcosmosS/S.T.A.R.-Labs/issues/67" target="_blank" rel="noopener noreferrer">execution and independent reproduction Issue #67</a>.
          This dated note is not a live GitHub approval signal.
        </p>
      </section>

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
