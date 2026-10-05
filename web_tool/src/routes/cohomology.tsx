import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Formula, Metric } from "@/components/viz/formula";
import { FieldCanvas } from "@/components/viz/field-canvas";
import { TorusMap } from "@/components/viz/charge-canvas";
import { type FieldSample } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";

export const Route = createFileRoute("/cohomology")({ component: CohomologyPage });

function CohomologyPage() {
  const lab = useLab();
  const [sample, setSample] = useState<FieldSample>({ q: 0, iqMean: 0, iqMax: 0, hNorm: 0, phiRms: 0, sourceJ: 0, aMean: 1 });

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="steel">Entropy cohomology</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Global charge, local scalar</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          A closed two-form ω on thermodynamic state space pulls back to F_Q = Φ*ω. Because d_𝒯 ω = 0, d F_Q = 0.
          The integral on a two-cycle is topological. The pointwise invariant 𝒥_Q = ¼ F_Q² is not. Mixing them is the
          error the paper exists to prevent.
        </p>
      </header>

      <div className="grid gap-4 md:grid-cols-2">
        <Formula boxed>
          Q<sub className="font-sans text-sm not-italic">RTCH</sub>[Σ₂] = ∫<sub>Σ₂</sub> Φ<sup>*</sup>ω
        </Formula>
        <Formula boxed>
          𝒥<sub>Q</sub> = ¼ F<sub>Q μν</sub> F<sub>Q</sub>
          <sup>μν</sup>
        </Formula>
      </div>

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="Q / 4π²" value={sample.q.toFixed(3)} hint="global / topological" />
        <Metric label="⟨𝒥_Q⟩" value={sample.iqMean.toFixed(3)} hint="local scalar" />
        <Metric label="max 𝒥_Q" value={sample.iqMax.toFixed(3)} />
        <Metric label="‖H‖" value={sample.hNorm.toFixed(3)} hint="λ_Q F_Q source" />
      </div>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Pullback density on Σ₂</div>
          <FieldCanvas params={lab} onSample={setSample} className="h-64 w-full sm:h-80" />
        </div>
        <div className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <div className="px-5 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Target T² · winding (n, m)</div>
          <TorusMap params={lab} className="h-64 w-full sm:h-80" />
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Winding</h2>
          <div>
            <div className="mb-1 flex justify-between font-mono text-[11px] text-muted">
              <span>n</span>
              <span className="tabular-nums text-fg">{lab.windingU}</span>
            </div>
            <Slider min={0} max={4} step={1} value={[lab.windingU]} onValueChange={(v) => lab.set({ windingU: v[0] ?? 1 })} />
          </div>
          <div>
            <div className="mb-1 flex justify-between font-mono text-[11px] text-muted">
              <span>m</span>
              <span className="tabular-nums text-fg">{lab.windingV}</span>
            </div>
            <Slider min={0} max={4} step={1} value={[lab.windingV]} onValueChange={(v) => lab.set({ windingV: v[0] ?? 1 })} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted">Freeze Y</span>
            <Switch checked={lab.freezeY} onCheckedChange={(v) => lab.set({ freezeY: v })} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted">Topological λ_Q</span>
            <Switch checked={lab.topologyOn} onCheckedChange={(v) => lab.set({ topologyOn: v })} />
          </div>
        </div>
        <div className="space-y-3">
          <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
            <Badge tone="ok">Established</Badge>
            <p className="mt-3 text-sm leading-relaxed text-muted">
              Pullback of a closed form is closed. If [ω] ≠ 0 in H²_dR(𝒯), the integral on a homologous two-cycle is
              invariant. d² = 0 forbids ω = d(dℳ) as a nontrivial class.
            </p>
          </article>
          <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
            <Badge tone="warn">Conjectural</Badge>
            <p className="mt-3 text-sm leading-relaxed text-muted">
              That thermodynamic state space carries such a class, that 𝒥_Q is the physically relevant local invariant,
              and that A should depend on it, are model assumptions — not theorems.
            </p>
          </article>
        </div>
      </section>
    </div>
  );
}
