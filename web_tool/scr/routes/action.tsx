import { createFileRoute } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Formula, Metric } from "@/components/viz/formula";
import { FieldCanvas } from "@/components/viz/field-canvas";
import { alphaQ, type FieldSample } from "@/lib/star/physics";
import { LIMIT_META, type LimitId, useLab } from "@/lib/star/store";
import { useState } from "react";

export const Route = createFileRoute("/action")({ component: ActionPage });

const TERMS = [
  { id: "EH", title: "Einstein–Hilbert", body: "S_EH = (1/16πG) ∫ R √−g. Standard GR curvature, plus GHY on ∂M.", status: "established" as const },
  { id: "φ", title: "Scalar", body: "S_φ = −∫ [½ (∇φ)² + V(φ)] √−g. Sourced by α_φ T_m whenever A depends on φ.", status: "established" as const },
  { id: "Y", title: "Thermodynamic sigma model", body: "S_Y = −∫ [½ G_AB ∂Y^A ∂Y^B + U(Y)] √−g. Target Christoffel Γ^A_BC enter the EL equation.", status: "established" as const },
  { id: "B", title: "Two-form kinetic", body: "S_B = −½ ∫ H ∧ *H with H = dB. Gauge B → B + dΛ leaves H invariant.", status: "established" as const },
  { id: "top", title: "Topological coupling", body: "S_top = λ_Q ∫ B ∧ F_Q. Metric-independent: no direct T_μν, yet it sources B and Y.", status: "conjectural" as const },
  { id: "m", title: "Matter", body: "S_m[Ψ_m, Ã = A²(φ, ℳ, 𝒥_Q) g]. Conserved w.r.t. the physical metric, not the Einstein frame.", status: "conjectural" as const },
];

const EQUATIONS = [
  { title: "Einstein", tex: "G_μν = 8πG (Tᵐ + Tᵠ + Tʸ + Tᴮ + T^{Q,m})_{μν}" },
  { title: "Scalar", tex: "□φ − V'(φ) + α_φ T_m = 0" },
  { title: "Two-form", tex: "d * H + λ_Q F_Q = 0" },
  { title: "Bianchi", tex: "dH = 0,   dF_Q = 0" },
  { title: "Exchange", tex: "∇_μ T_m^{μν} = T_m ∇^ν ln A" },
];

const LIMITS: LimitId[] = ["minimal", "gr", "local-only", "topo-only", "no-conformal", "frozen-y"];

function ActionPage() {
  const lab = useLab();
  const [sample, setSample] = useState<FieldSample>({ q: 0, iqMean: 0, iqMax: 0, hNorm: 0, phiRms: 0, sourceJ: 0, aMean: 1 });
  const aQ = alphaQ(lab);

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge>RTCH master action</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Fully variational field system</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Diffeomorphism-invariant field theory on (M, g) with scalar φ, thermodynamic map Y^A : M → 𝒯, and two-form B.
          ω is closed and cohomologically nontrivial — it is not d(dℳ), because d² = 0.
        </p>
      </header>

      <Formula boxed>
        S<sub className="font-sans text-sm not-italic">RTCH</sub> = S<sub>EH</sub> + S<sub>φ</sub> + S<sub>Y</sub> + S<sub>B</sub> + S<sub>top</sub> + S<sub>m</sub> + S<sub>GHY</sub>
      </Formula>

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="λ_Q" value={lab.lambdaQ.toFixed(2)} hint={lab.topologyOn ? "topological source" : "off"} />
        <Metric label="β_Q" value={lab.betaQ.toFixed(2)} hint="local coupling" />
        <Metric label="α_Q" value={aQ.toFixed(3)} hint="β_Q / Λ_Q⁴" />
        <Metric label="⟨A⟩" value={sample.aMean.toFixed(3)} hint="matter conformal factor" />
      </div>

      <section className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
        <div className="flex items-center justify-between px-5 py-3">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">F_Q on a two-cycle · 𝒥_Q heatmap</div>
          <div className="font-mono text-[10px] text-muted">Q ≈ {sample.q.toFixed(2)} · ⟨𝒥_Q⟩ {sample.iqMean.toFixed(3)}</div>
        </div>
        <FieldCanvas params={lab} onSample={setSample} className="h-[min(42vh,360px)] w-full" />
      </section>

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {TERMS.map((t) => (
          <article key={t.id} className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
            <div className="flex items-center justify-between">
              <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-steel">{t.id}</span>
              <Badge tone={t.status === "established" ? "ok" : "warn"}>{t.status}</Badge>
            </div>
            <h2 className="mt-2 font-display text-xl tracking-tight">{t.title}</h2>
            <p className="mt-2 text-sm leading-relaxed text-muted">{t.body}</p>
          </article>
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Parameters</h2>
          <Knob label="λ_Q" value={lab.lambdaQ} min={0} max={2} onChange={(v) => lab.set({ lambdaQ: v })} />
          <Knob label="β_Q" value={lab.betaQ} min={0} max={1.2} onChange={(v) => lab.set({ betaQ: v })} />
          <Knob label="Λ_Q" value={lab.lambdaScale} min={0.4} max={2} onChange={(v) => lab.set({ lambdaScale: v })} />
          <Knob label="winding n" value={lab.windingU} min={1} max={4} step={1} onChange={(v) => lab.set({ windingU: v })} />
          <Knob label="winding m" value={lab.windingV} min={1} max={4} step={1} onChange={(v) => lab.set({ windingV: v })} />
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted">Topology on</span>
            <Switch checked={lab.topologyOn} onCheckedChange={(v) => lab.set({ topologyOn: v })} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted">Conformal A</span>
            <Switch checked={lab.conformalOn} onCheckedChange={(v) => lab.set({ conformalOn: v })} />
          </div>
        </div>
        <div>
          <h2 className="font-display text-xl tracking-tight">Euler–Lagrange</h2>
          <div className="mt-4 space-y-3">
            {EQUATIONS.map((e) => (
              <div key={e.title} className="rounded-lg bg-elevated px-4 py-3 shadow-[var(--shadow-border)]">
                <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">{e.title}</div>
                <div className="mt-1 font-display text-lg tracking-tight">{e.tex}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section>
        <h2 className="font-display text-xl tracking-tight">Limits</h2>
        <div className="mt-3 grid gap-2 sm:grid-cols-3">
          {LIMITS.map((id) => (
            <button
              key={id}
              type="button"
              onClick={() => lab.applyLimit(id)}
              className="rounded-lg bg-elevated px-3 py-3 text-left shadow-[var(--shadow-border)] hover:shadow-[var(--shadow-border-hover)]"
            >
              <div className="font-mono text-[10px] text-steel">{LIMIT_META[id].pair}</div>
              <div className="text-sm">{LIMIT_META[id].label}</div>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

function Knob({
  label,
  value,
  min,
  max,
  step = 0.01,
  onChange,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  onChange: (v: number) => void;
}) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between font-mono text-[11px] text-muted">
        <span>{label}</span>
        <span className="tabular-nums text-fg">{Number.isInteger(step) ? String(value) : value.toFixed(2)}</span>
      </div>
      <Slider min={min} max={max} step={step} value={[value]} onValueChange={(v) => onChange(v[0] ?? value)} />
    </div>
  );
}
