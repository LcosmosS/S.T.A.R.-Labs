import { createFileRoute } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Formula, Metric } from "@/components/viz/formula";
import { type LimitId, useLab } from "@/lib/star/store";

export const Route = createFileRoute("/action")({ component: ActionPage });

const TERMS = [
  { id: "EH", title: "Einstein–Hilbert", body: "S_EH = (1/16πG) ∫ R ε_g. Standard GR curvature, plus GHY on ∂M." },
  { id: "φ", title: "Scalar", body: "S_φ = −∫ [½ (∇φ)² + V(φ)] ε_g. Sourced by α_φ T_m whenever A depends on φ." },
  { id: "Y", title: "Thermodynamic sigma model", body: "S_Y = −∫ [½ G_AB ∂Y^A ∂Y^B + U(Y)] ε_g. Target Christoffel Γ^A_BC enter the EL equation." },
  { id: "B", title: "Two-form kinetic", body: "S_B = −½ ∫ H ∧ *H with H = dB. Gauge B → B + dΛ leaves H invariant." },
  { id: "top", title: "Topological coupling", body: "S_top = λ_Q ∫ B ∧ F_Q. Metric-independent: T_μν^top = 0, yet it sources B and Y." },
  { id: "m", title: "Matter", body: "S_m[Ψ_m, Ã = A²(φ, M) g]. Matter is conserved w.r.t. the physical metric, not the Einstein frame." },
];

const LIMITS: Array<{ id: LimitId; label: string; note: string }> = [
  { id: "minimal", label: "Minimal RTCH", note: "All couplings on" },
  { id: "no-topology", label: "λ_Q = 0", note: "d*H = 0, no J_Q" },
  { id: "no-conformal", label: "A = 1", note: "Geodesics recovered" },
  { id: "gr", label: "GR limit", note: "A = 1 and λ_Q = 0" },
  { id: "frozen-y", label: "Frozen Y", note: "F_Q vanishes locally" },
];

const EQUATIONS = [
  { title: "Einstein", tex: "G_μν = 8πG (T^m + T^φ + T^Y + T^B)_μν" },
  { title: "Scalar", tex: "□φ − V'(φ) + α_φ T_m = 0" },
  { title: "State fields", tex: "□Y^A + Γ^A_BC ∇Y^B ∇Y^C − G^{AB}∂_B U = G^{AB}(J_B^{(Q)} + α_B T_m)" },
  { title: "Two-form", tex: "d*H + λ_Q F_Q = 0" },
  { title: "Bianchi", tex: "dH = 0,   dF_Q = 0" },
];

function ActionPage() {
  const lab = useLab();
  const Anote = lab.conformalOn ? "A(φ, M) active" : "A = 1";
  const topNote = lab.topologyOn && lab.lambdaQ !== 0 ? "topological source on" : "topological source off";

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge>RTCH master action</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Fully variational field system</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Diffeomorphism-invariant relativistic field theory on (M, g) with scalar φ, thermodynamic map Y^A : M → T,
          and two-form B. The construction is the rigorous RTCH implementation of ECC: ω is closed and cohomologically
          nontrivial — it is not d(dM).
        </p>
      </header>

      <Formula boxed>
        S<sub className="font-sans text-sm not-italic">RTCH</sub> = S<sub>EH</sub> + S<sub>φ</sub> + S<sub>Y</sub> + S<sub>B</sub> + S<sub>top</sub> + S<sub>m</sub> + S<sub>GHY</sub>
      </Formula>

      <div className="grid gap-4 sm:grid-cols-3">
        <Metric label="λ_Q" value={lab.lambdaQ.toFixed(2)} hint={topNote} />
        <Metric label="α_φ" value={lab.conformalOn ? lab.alphaPhi.toFixed(2) : "0"} hint={Anote} />
        <Metric label="α_A" value={lab.conformalOn ? lab.alphaA.toFixed(2) : "0"} hint="thermodynamic coupling" />
      </div>

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {TERMS.map((t) => (
          <article key={t.id} className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
            <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-steel">{t.id}</div>
            <h2 className="mt-2 font-display text-xl tracking-tight">{t.title}</h2>
            <p className="mt-2 text-sm leading-relaxed text-muted">{t.body}</p>
          </article>
        ))}
      </section>

      <section>
        <h2 className="font-display text-2xl tracking-tight">Euler–Lagrange system</h2>
        <div className="mt-4 space-y-3">
          {EQUATIONS.map((e) => (
            <div key={e.title} className="rounded-lg bg-elevated px-4 py-3 shadow-[var(--shadow-border)]">
              <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">{e.title}</div>
              <div className="mt-1 font-display text-lg tracking-tight">{e.tex}</div>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="font-display text-2xl tracking-tight">Standard-physics limits</h2>
        <p className="mt-2 max-w-2xl text-sm text-muted">
          Independently testable contractions of the master action. GR geodesics and Einstein-frame conservation are
          recovered when both novel couplings are off.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          {LIMITS.map((l) => (
            <Button key={l.id} variant="secondary" onClick={() => lab.applyLimit(l.id)} title={l.note}>
              {l.label}
            </Button>
          ))}
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Conformal factor A(φ, M)</div>
          <label className="mt-4 flex h-11 items-center justify-between">
            <span className="text-sm">Matter coupling on</span>
            <Switch checked={lab.conformalOn} onCheckedChange={(c) => lab.set({ conformalOn: c })} />
          </label>
          <Field label="α_φ" val={lab.alphaPhi} min={0} max={1} onChange={(v) => lab.set({ alphaPhi: v })} />
          <Field label="α_A" val={lab.alphaA} min={0} max={1} onChange={(v) => lab.set({ alphaA: v })} />
          <p className="mt-3 text-sm text-muted">
            Test particles obey u^ν ∇_ν u^μ = −c² h^{'{μν}'} ∇_ν ln A. When A = 1 this is geodesic motion.
          </p>
        </div>
        <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Why S_top is gravitationally active</div>
          <p className="mt-3 text-sm leading-relaxed text-muted">
            The topological density B ∧ F_Q contains no metric and no Hodge star, so δS_top / δg_μν = 0. It still
            changes the B and Y equations; the resulting configurations stress spacetime through T^Y and T^B.
          </p>
          <Formula className="mt-4 text-base">
            d * H + λ_Q F_Q = 0
          </Formula>
          <p className="mt-3 text-sm leading-relaxed text-muted">
            Taking d of this equation is consistent because d² = 0 and d F_Q = 0 — the Bianchi identity of the target
            cohomology.
          </p>
        </div>
      </section>
    </div>
  );
}

function Field({
  label,
  val,
  min,
  max,
  onChange,
}: {
  label: string;
  val: number;
  min: number;
  max: number;
  onChange: (v: number) => void;
}) {
  return (
    <div className="mt-3">
      <div className="flex justify-between font-mono text-xs">
        <span className="text-subtle">{label}</span>
        <span className="tabular-nums">{val.toFixed(2)}</span>
      </div>
      <Slider min={min} max={max} step={0.01} value={[val]} onValueChange={(v) => onChange(v[0] ?? val)} />
    </div>
  );
}
