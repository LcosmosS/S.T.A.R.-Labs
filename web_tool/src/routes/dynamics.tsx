import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Formula, Metric } from "@/components/viz/formula";
import { DynamicsCanvas } from "@/components/viz/dynamics-canvas";
import { alphaQ } from "@/lib/star/physics";
import { LIMIT_META, type LimitId, useLab } from "@/lib/star/store";

export const Route = createFileRoute("/dynamics")({ component: DynamicsPage });

const LIMITS: LimitId[] = ["minimal", "gr", "local-only", "topo-only", "no-conformal", "frozen-y"];

function DynamicsPage() {
  const lab = useLab();
  const [running, setRunning] = useState(true);
  const [sample, setSample] = useState({ aMean: 1, residual: 0, forcePhi: 0, forceM: 0, forceQ: 0, agree: true });
  const aQ = alphaQ(lab);

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="steel">Unified matter</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Particle and fluid from one A</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          The variational paper's central claim is not a new force law pasted onto GR. Point particles and perfect
          fluids are two descriptions of S_m[Ψ_m, A²g]. Dots follow −∇ ln A. Arrows are the Euler field. At vanishing
          pressure they must agree.
        </p>
      </header>

      <Formula boxed>
        S<sub>p</sub> = −m ∫ A(φ, ℳ, 𝒥<sub>Q</sub>) ds
      </Formula>

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="⟨A⟩" value={sample.aMean.toFixed(3)} hint={lab.conformalOn ? "conformal on" : "A = 1"} />
        <Metric
          label="Dust residual"
          value={sample.residual.toFixed(3)}
          hint={lab.pressure === 0 ? (sample.agree ? "agrees with worldline" : "mismatch") : "p > 0 expected"}
        />
        <Metric label="α_Q" value={aQ.toFixed(3)} hint="β_Q / Λ_Q⁴" />
        <Metric label="p / ρ" value={lab.pressure.toFixed(2)} hint="dust at 0" />
      </div>

      <section className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
        <div className="flex flex-wrap items-center justify-between gap-3 px-5 py-3">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">
            Worldlines · Euler field · Ã = A² g
          </div>
          <Button size="sm" variant="secondary" onClick={() => setRunning((v) => !v)}>
            {running ? "Pause" : "Run"}
          </Button>
        </div>
        <DynamicsCanvas
          params={lab}
          running={running}
          onSample={setSample}
          className="h-[min(56vh,460px)] w-full"
        />
      </section>

      <section className="grid gap-6 lg:grid-cols-[1fr_0.9fr]">
        <div className="space-y-4 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Couplings</h2>
          <Knob label="β_Q" value={lab.betaQ} min={0} max={1.2} step={0.01} onChange={(v) => lab.set({ betaQ: v })} />
          <Knob label="Λ_Q" value={lab.lambdaScale} min={0.4} max={2} step={0.02} onChange={(v) => lab.set({ lambdaScale: v })} />
          <Knob label="α_φ" value={lab.alphaPhi} min={0} max={0.8} step={0.01} onChange={(v) => lab.set({ alphaPhi: v })} />
          <Knob label="α_A" value={lab.alphaA} min={0} max={0.8} step={0.01} onChange={(v) => lab.set({ alphaA: v })} />
          <Knob label="pressure p" value={lab.pressure} min={0} max={0.45} step={0.01} onChange={(v) => lab.set({ pressure: v })} />
          <div className="flex items-center justify-between pt-1">
            <span className="text-sm text-muted">Conformal A</span>
            <Switch checked={lab.conformalOn} onCheckedChange={(v) => lab.set({ conformalOn: v })} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted">Freeze Y (F_Q → 0)</span>
            <Switch checked={lab.freezeY} onCheckedChange={(v) => lab.set({ freezeY: v })} />
          </div>
        </div>
        <div className="space-y-3">
          <h2 className="font-display text-xl tracking-tight">Nested nulls (λ_Q, β_Q)</h2>
          <div className="grid gap-2 sm:grid-cols-2">
            {LIMITS.map((id) => (
              <button
                key={id}
                type="button"
                onClick={() => lab.applyLimit(id)}
                className="rounded-lg bg-elevated px-3 py-3 text-left shadow-[var(--shadow-border)] transition-shadow hover:shadow-[var(--shadow-border-hover)]"
              >
                <div className="font-mono text-[10px] uppercase tracking-[0.14em] text-steel">{LIMIT_META[id].pair}</div>
                <div className="mt-1 text-sm text-fg">{LIMIT_META[id].label}</div>
                <div className="text-xs text-muted">{LIMIT_META[id].note}</div>
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <Badge>Particle</Badge>
          <p className="mt-3 font-display text-lg tracking-tight">
            u^μ ∇_μ u^ν = −c² h^νμ ∇_μ ln A
          </p>
          <p className="mt-2 text-sm leading-relaxed text-muted">
            Automatically orthogonal to four-velocity: u_μ f^μ = 0, so u·u = −c² is preserved. The cohomological piece
            is −c² α_Q h^νμ ∇_μ 𝒥_Q.
          </p>
        </article>
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <Badge>Perfect fluid</Badge>
          <p className="mt-3 font-display text-lg tracking-tight">
            a^ν = −h^νμ ∇_μ p / (ρ+p) + T_m / (ρ+p) h^νμ ∇_μ ln A
          </p>
          <p className="mt-2 text-sm leading-relaxed text-muted">
            T_m = −ρ + 3p. Dust (p = 0) collapses to the worldline equation. That identity is the paper's consistency
            test — not an extra postulate.
          </p>
        </article>
      </section>
    </div>
  );
}

function Knob({
  label,
  value,
  min,
  max,
  step,
  onChange,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (v: number) => void;
}) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between font-mono text-[11px] text-muted">
        <span>{label}</span>
        <span className="tabular-nums text-fg">{value.toFixed(2)}</span>
      </div>
      <Slider min={min} max={max} step={step} value={[value]} onValueChange={(v) => onChange(v[0] ?? value)} />
    </div>
  );
}
