import { createFileRoute } from "@tanstack/react-router";
import { useCallback, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { TorusMap } from "@/components/viz/charge-canvas";
import { FieldCanvas } from "@/components/viz/field-canvas";
import { Formula, Metric } from "@/components/viz/formula";
import type { FieldSample } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";

export const Route = createFileRoute("/cohomology")({ component: CohomologyPage });

function CohomologyPage() {
  const lab = useLab();
  const [sample, setSample] = useState<FieldSample>({
    q: 0,
    iqMean: 0,
    iqMax: 0,
    hNorm: 0,
    phiRms: 0,
    sourceJ: 0,
    aMean: 1,
  });
  const onSample = useCallback((s: FieldSample) => setSample(s), []);
  const params = {
    lambdaQ: lab.lambdaQ,
    alphaPhi: lab.alphaPhi,
    alphaA: lab.alphaA,
    topologyOn: lab.topologyOn,
    conformalOn: lab.conformalOn,
    freezeY: lab.freezeY,
    windingU: lab.windingU,
    windingV: lab.windingV,
    beta: lab.beta,
    gamma: lab.gamma,
  };

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="steel">ECC · RTCH</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Entropy cohomology</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Target manifold T² carries a closed 2-form ω with [ω] ≠ 0 in de Rham cohomology. The spacetime pullback
          F_Q = Φ*ω is closed because d_T ω = 0. The charge on a two-cycle is topological; I_Q is a local dynamical
          scalar and must not be substituted for Q.
        </p>
      </header>

      <div className="grid gap-4 md:grid-cols-2">
        <Formula boxed>
          Q<sub className="font-sans text-sm not-italic">RTCH</sub>[Σ<sub>2</sub>] = ∫ Φ<sup>*</sup>ω
        </Formula>
        <Formula boxed>
          I<sub className="font-sans text-sm not-italic">Q</sub> = ¼ F<sub>Q μν</sub> F<sub>Q</sub>
          <sup>μν</sup>
        </Formula>
      </div>

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="Q_RTCH" value={sample.q.toFixed(2)} hint="normalized degree" />
        <Metric label="deg (n,m)" value={`${lab.windingU} × ${lab.windingV}`} hint="covering degree" />
        <Metric label="⟨I_Q⟩" value={sample.iqMean.toExponential(2)} hint="local scalar" />
        <Metric label="max I_Q" value={sample.iqMax.toExponential(2)} hint="not quantized" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <figure className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <figcaption className="px-4 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">
            Pullback F_Q on a spatial slice · Σ₂ marked
          </figcaption>
          <FieldCanvas params={params} onSample={onSample} className="h-[320px] w-full" />
        </figure>
        <figure className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <figcaption className="px-4 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">
            Target T² with periodic identifications
          </figcaption>
          <TorusMap params={params} className="h-[320px] w-full" />
        </figure>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Winding of Φ</div>
          <p className="mt-2 text-sm text-muted">
            Changing covering degree (n, m) jumps Q by integers. Stretching the map changes I_Q continuously without
            altering the cohomology class.
          </p>
          <div className="mt-4 space-y-4">
            <div>
              <div className="flex justify-between font-mono text-xs">
                <span className="text-subtle">n · θ winding</span>
                <span className="tabular-nums">{lab.windingU}</span>
              </div>
              <Slider min={0} max={4} step={1} value={[lab.windingU]} onValueChange={(v) => lab.set({ windingU: v[0] ?? 1 })} />
            </div>
            <div>
              <div className="flex justify-between font-mono text-xs">
                <span className="text-subtle">m · φ winding</span>
                <span className="tabular-nums">{lab.windingV}</span>
              </div>
              <Slider min={0} max={4} step={1} value={[lab.windingV]} onValueChange={(v) => lab.set({ windingV: v[0] ?? 1 })} />
            </div>
          </div>
        </div>
        <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Dynamical couplings</div>
          <div className="mt-4 space-y-4">
            <Row label="Topological λ_Q" checked={lab.topologyOn} onChecked={(c) => lab.set({ topologyOn: c })} />
            <div>
              <div className="flex justify-between font-mono text-xs">
                <span className="text-subtle">λ_Q</span>
                <span className="tabular-nums">{lab.lambdaQ.toFixed(2)}</span>
              </div>
              <Slider min={0} max={3} step={0.05} value={[lab.lambdaQ]} onValueChange={(v) => lab.set({ lambdaQ: v[0] ?? 1 })} />
            </div>
            <Row label="Freeze Y^A" checked={lab.freezeY} onChecked={(c) => lab.set({ freezeY: c })} />
            <p className="text-sm text-muted">
              Frozen thermodynamic fields set F_Q → 0 locally and remove the cohomological source from the B
              equation. |H| = {sample.hNorm.toExponential(2)}, |J_Q| = {sample.sourceJ.toExponential(2)}.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Row({ label, checked, onChecked }: { label: string; checked: boolean; onChecked: (v: boolean) => void }) {
  return (
    <label className="flex h-11 items-center justify-between gap-4">
      <span className="text-sm">{label}</span>
      <Switch checked={checked} onCheckedChange={onChecked} />
    </label>
  );
}
