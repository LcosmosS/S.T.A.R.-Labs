import { createFileRoute } from "@tanstack/react-router";
import { useMemo } from "react";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { CLUSTERS, KAPPA_UCF, getCatalog } from "@/lib/star/catalog";
import { Formula, Metric, Sym } from "@/components/viz/formula";
import { H0_PLANCK, H0_SHOES, Z_STAR, hEff, hLcdm, meanOmega } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";

export const Route = createFileRoute("/hubble")({ component: HubblePage });

function inferredH0(zz: number, curves: ReturnType<typeof getCatalog>, beta: number, gamma: number) {
  const E = hLcdm(zz, 1);
  return hEff(zz, curves, beta, gamma) / E;
}

function HubblePage() {
  const z = useLab((s) => s.z);
  const beta = useLab((s) => s.beta);
  const gamma = useLab((s) => s.gamma);
  const set = useLab((s) => s.set);
  const curves = getCatalog();
  const zPlot = Math.min(z, 2.4);

  const series = useMemo(() => {
    const rows = [];
    for (let i = 0; i <= 48; i++) {
      const zz = (i / 48) * 2.4;
      rows.push({
        z: Number(zz.toFixed(3)),
        star: Number(inferredH0(zz, curves, beta, gamma).toFixed(3)),
        planck: H0_PLANCK,
        shoes: H0_SHOES,
      });
    }
    return rows;
  }, [beta, gamma, curves]);

  const H = inferredH0(zPlot, curves, beta, gamma);
  const om = meanOmega(curves, zPlot);
  const omInf = meanOmega(curves, 1e5);
  const delta = inferredH0(0, curves, beta, gamma) - inferredH0(Z_STAR, curves, beta, gamma);

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="warn">Hubble–Planck tension</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Scale-dependent expansion</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Local distance-ladder measurements sample a biased subset of Φ(E); the CMB averages the global catalog.
          Entropy curvature κ(z) and Tr(δg)(z) add a late-time correction that vanishes at last scatter. The chart
          shows the inferred H0(z) ≡ H_eff(z) / E_ΛCDM(z).
        </p>
      </header>

      <Formula boxed>
        <Sym>H</Sym>
        <sub className="font-sans text-sm not-italic">eff</sub>(z) = H<sub className="font-sans text-sm not-italic">ΛCDM</sub>(z; H<sub>0</sub>⟨Ω⟩)
        + β κ(z) + γ Tr(δg)
      </Formula>

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="H0_eff(z)" value={H.toFixed(2)} unit="km/s/Mpc" />
        <Metric label="SH0ES" value={H0_SHOES.toFixed(2)} unit="km/s/Mpc" />
        <Metric label="Planck" value={H0_PLANCK.toFixed(1)} unit="km/s/Mpc" />
        <Metric label="ΔH0 (local − CMB)" value={delta.toFixed(2)} unit="km/s/Mpc" />
      </div>

      <div className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Inferred H0(z) · km/s/Mpc</div>
          <div className="flex gap-4 font-mono text-[10px] uppercase tracking-[0.12em] text-muted">
            <span className="text-fg">STAR</span>
            <span>Planck</span>
            <span>SH0ES</span>
          </div>
        </div>
        <div className="h-[280px] w-full sm:h-[340px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={series} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
              <CartesianGrid stroke="rgba(255,255,255,0.06)" />
              <XAxis
                dataKey="z"
                type="number"
                domain={[0, 2.4]}
                tick={{ fill: "var(--color-muted)", fontSize: 11, fontFamily: "IBM Plex Mono" }}
                stroke="var(--color-border)"
              />
              <YAxis
                domain={[64, 78]}
                tick={{ fill: "var(--color-muted)", fontSize: 11, fontFamily: "IBM Plex Mono" }}
                stroke="var(--color-border)"
                width={48}
              />
              <Tooltip
                contentStyle={{
                  background: "var(--color-elevated)",
                  border: "1px solid var(--color-border)",
                  borderRadius: 8,
                  fontFamily: "IBM Plex Mono",
                  fontSize: 12,
                }}
              />
              <Line type="monotone" dataKey="star" stroke="var(--color-fg)" dot={false} strokeWidth={2} name="STAR" />
              <Line type="monotone" dataKey="planck" stroke="var(--color-steel)" dot={false} strokeWidth={1.4} name="Planck" />
              <Line type="monotone" dataKey="shoes" stroke="var(--color-muted)" dot={false} strokeDasharray="4 4" strokeWidth={1.2} name="SH0ES" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Control label="Redshift z" value={zPlot.toFixed(2)} min={0} max={2.4} step={0.01} val={zPlot} onChange={(v) => set({ z: v })} />
        <Control label="β · entropy curvature" value={beta.toFixed(2)} min={0} max={1.2} step={0.01} val={beta} onChange={(v) => set({ beta: v })} />
        <Control label="γ · metric trace" value={gamma.toFixed(2)} min={0} max={1} step={0.01} val={gamma} onChange={(v) => set({ gamma: v })} />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Metric label="⟨Ω_E⟩_z" value={om.toFixed(4)} hint="weighted real period" />
        <Metric label="⟨Ω_E⟩_z / ⟨Ω_E⟩_∞" value={(om / omInf).toFixed(4)} hint="local vs global sampling" />
      </div>

      <section>
        <h2 className="font-display text-2xl tracking-tight">Supercluster anchors</h2>
        <p className="mt-2 max-w-2xl text-sm text-muted">
          First-principles UCF scaling uses κ ≈ {KAPPA_UCF} with Virgo as the geometric origin. H_eff factors below
          are the published S.T.A.R. run summary.
        </p>
        <div className="mt-4 overflow-x-auto rounded-xl bg-surface shadow-[var(--shadow-border)]">
          <table className="w-full min-w-[640px] text-left text-sm">
            <thead className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">
              <tr className="border-b border-border">
                {["Cluster", "r (Mly)", "Rank", "H_eff factor", "Entropy", "Coh. class"].map((h) => (
                  <th key={h} className="px-4 py-3 font-medium">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="font-mono tabular-nums">
              {CLUSTERS.map((c) => (
                <tr key={c.name} className="border-b border-border/70 last:border-0">
                  <td className="px-4 py-3 font-sans text-fg">{c.name}</td>
                  <td className="px-4 py-3 text-muted">{c.rMly}</td>
                  <td className="px-4 py-3 text-muted">{c.rank}</td>
                  <td className="px-4 py-3 text-fg">{c.hFactor.toFixed(4)}</td>
                  <td className="px-4 py-3 text-muted">{c.entropy.toFixed(2)}</td>
                  <td className="px-4 py-3 text-muted">{c.cohClass.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function Control({
  label,
  value,
  min,
  max,
  step,
  val,
  onChange,
}: {
  label: string;
  value: string;
  min: number;
  max: number;
  step: number;
  val: number;
  onChange: (v: number) => void;
}) {
  return (
    <div className="rounded-xl bg-surface p-4 shadow-[var(--shadow-border)]">
      <div className="flex items-baseline justify-between">
        <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">{label}</span>
        <span className="font-mono text-sm tabular-nums">{value}</span>
      </div>
      <Slider min={min} max={max} step={step} value={[val]} onValueChange={(v) => onChange(v[0] ?? val)} className="mt-2" />
    </div>
  );
}
