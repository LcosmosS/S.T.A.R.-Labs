import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Formula, Metric } from "@/components/viz/formula";
import { EntropyField } from "@/components/viz/entropy-canvas";
import { OrbitCloud } from "@/components/viz/orbit-cloud";
import { FrozenSkyOverlay } from "@/components/viz/frozen-sky-overlay";
import { A01EvidenceViewer } from "@/components/viz/a01-evidence-viewer";
import { FILAMENTS, PROJECTED } from "@/lib/star/physics";
import { catalogStats } from "@/lib/star/catalog";
import { useLab } from "@/lib/star/store";
import { RepositoryStatus } from "@/components/repository-status";

export const Route = createFileRoute("/projection")({
  component: ProjectionPage,
});

/**
 * Provides distinct synthetic-demo and read-only A01 evidence display modes.
 * Synthetic selection updates only the illustrative lab state; the separate
 * astronomical viewer receives neither synthetic nor A01 arithmetic points.
 * @returns The projection page with mode controls and scientific scope labels.
 */
function ProjectionPage() {
  const [mode, setMode] = useState<"synthetic" | "evidence">("synthetic");
  const [hydrated, setHydrated] = useState(false);
  useEffect(() => setHydrated(true), []);
  const selected = useLab((s) => s.selectedLabel);
  const set = useLab((s) => s.set);
  const stats = catalogStats();
  const curve = PROJECTED.find((c) => c.label === selected);

  return (
    <div className="space-y-8">
      <header className="max-w-3xl">
        <Badge tone="warn">
          Arithmetic coordinates · separate display modes
        </Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">
          Arithmetic projection Φ(E)
        </h1>
        <div
          className="mt-5 flex flex-wrap gap-2"
          role="group"
          aria-label="Projection display mode"
          data-a01-hydrated={hydrated}
        >
          <button
            type="button"
            aria-pressed={mode === "synthetic"}
            onClick={() => setMode("synthetic")}
            className={`min-h-11 rounded-md border px-4 text-sm ${mode === "synthetic" ? "border-primary bg-primary text-primary-fg" : "border-border bg-surface text-fg"}`}
          >
            Synthetic Demo
          </button>
          <button
            type="button"
            aria-pressed={mode === "evidence"}
            onClick={() => setMode("evidence")}
            className={`min-h-11 rounded-md border px-4 text-sm ${mode === "evidence" ? "border-primary bg-primary text-primary-fg" : "border-border bg-surface text-fg"}`}
          >
            A01 Evidence
          </button>
        </div>
      </header>

      {mode === "evidence" ? (
        <A01EvidenceViewer />
      ) : (
        <div
          className="space-y-8"
          data-testid="synthetic-demo"
          data-fixture-count={PROJECTED.length}
        >
          <p className="max-w-3xl text-sm leading-relaxed text-muted">
            This historical 2_STARMAP.md illustration maps discriminant and
            conductor to angles, and regulator to radius. It uses 12 handwritten
            illustrative entries and 148 deterministic synthetic fixtures.
            Generated features depend on rank, so omitting a direct rank axis
            does not establish independence. The registered EXP-MAP-A01 map,
            dataset, and null protocol are separate; no registered experiment
            runs here.
          </p>

          <RepositoryStatus />

          <Formula boxed>
            Y^A ∼ (log N_E, log |Δ_E|, r_E, log R_E, log |Ω_E|, …)
          </Formula>

          <div className="grid gap-4 sm:grid-cols-3">
            <Metric label="Points" value={String(PROJECTED.length)} />
            <Metric
              label="Graph links"
              value={String(FILAMENTS.length)}
              hint="3-NN illustration"
            />
            <Metric
              label="⟨entropy⟩"
              value={stats.meanEntropy.toFixed(2)}
              hint="log |Δ|"
            />
          </div>

          <section className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
            <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">
              Φ(E) point cloud
            </div>
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
              <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">
                Entropy density
              </div>
              <EntropyField
                points={PROJECTED}
                className="h-56 w-full sm:h-72"
              />
            </div>
            <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
              <h2 className="font-display text-xl tracking-tight">
                {curve?.label ?? "Select a curve"}
              </h2>
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
                <p className="mt-3 text-sm text-muted">
                  Click a point in the cloud.
                </p>
              )}
            </div>
          </section>
        </div>
      )}

      <div className="space-y-3 border-t border-border pt-8">
        <p className="max-w-3xl text-sm text-muted">
          Separate observational display: the sky viewer below uses only its own
          admitted astronomical releases. Arithmetic A01 coordinates and
          synthetic fixtures are never sent to this sky layer.
        </p>
        <FrozenSkyOverlay />
      </div>
    </div>
  );
}

/**
 * Displays one already formatted property of a selected synthetic demo curve.
 * @param props - The property label and display value from the demo catalog.
 * @returns A styled definition-list term and value for the selected curve.
 */
function Item({ k, v }: { k: string; v: string }) {
  return (
    <div>
      <dt className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">
        {k}
      </dt>
      <dd className="font-mono tabular-nums text-fg">{v}</dd>
    </div>
  );
}
