import { createFileRoute } from "@tanstack/react-router";
import { useMemo } from "react";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { CLUSTERS, KAPPA_UCF, getCatalog } from "@/lib/star/catalog";
import { Formula, Metric } from "@/components/viz/formula";
import { H0_PLANCK, H0_SHOES, hEff, hLcdm, meanOmega } from "@/lib/star/physics";
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
  const highZ = inferredH0(1100, curves, beta, gamma);

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="warn">Conjectural expansion</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Scale-dependent Hubble</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          S.T.A.R. treats the local expansion rate as a weighted real-period average plus entropy-curvature and
          metric-trace terms that decay toward last scatter. This is a phenomenological layer on ACSC, not a derivation
          from the RTCH action.
        </p>
      </header>

      <Formula boxed>
        H<sub className="font-sans text-sm not-italic">eff</sub>(z) = H<sub className="font-sans text-sm not-italic">ΛCDM</sub>(z; H₀ ⟨Ω⟩_z) + β κ(z) + γ Tr(δg)
      </Formula>

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="H0_eff(z)" value={H.toFixed(2)} unit="km/s/Mpc" hint={`z = ${zPlot.toFixed(2)}`} />
        <Metric label="SH0ES" value={H0_SHOES.toFixed(2)} unit="km/s/Mpc" hint="local ladder" />
        <Metric label="Planck" value={H0_PLANCK.toFixed(1)} unit="km/s/Mpc" hint="CMB" />
        <Metric label="H_eff(z*)" value={highZ.toFixed(2)} hint="last scatter" />
      </div>

      <section className="rounded-xl bg-surface p-4 shadow-[var(--shadow-border)] sm:p-5">
        <div className="mb-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Inferred H0 versus redshift</div>
        <div className="h-64 w-full sm:h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={series} margin={{ top: 8, right: 12, left: 0, bottom: 0 }}>
              <CartesianGrid stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="z" tick={{ fill: "#8b919c", fontSize: 11 }} />
              <YAxis domain={[64, 78]} tick={{ fill: "#8b919c", fontSize: 11 }} />
              <Tooltip
                contentStyle={{ background: "#181c24", border: "1px solid #232831", borderRadius: 8 }}
                labelStyle={{ color: "#8b919c" }}
              />
              <Line type="monotone" dataKey="star" stroke="#d7dee8" strokeWidth={2} dot={false} name="STARMAP" />
              <Line type="monotone" dataKey="shoes" stroke="#c4a574" strokeWidth={1} dot={false} name="SH0ES" />
              <Line type="monotone" dataKey="planck" stroke="#8aa0b5" strokeWidth={1} dot={false} name="Planck" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <h2 className="font-display text-xl tracking-tight">Controls</h2>
          <div>
            <div className="mb-1 flex justify-between font-mono text-[11px] text-muted">
              <span>redshift z</span>
              <span className="tabular-nums text-fg">{zPlot.toFixed(2)}</span>
            </div>
            <Slider min={0} max={2.4} step={0.01} value={[z]} onValueChange={(v) => set({ z: v[0] ?? 0 })} />
          </div>
          <div>
            <div className="mb-1 flex justify-between font-mono text-[11px] text-muted">
              <span>entropy curvature β</span>
              <span className="tabular-nums text-fg">{beta.toFixed(2)}</span>
            </div>
            <Slider min={0} max={1.2} step={0.01} value={[beta]} onValueChange={(v) => set({ beta: v[0] ?? 0 })} />
          </div>
          <div>
            <div className="mb-1 flex justify-between font-mono text-[11px] text-muted">
              <span>metric trace γ</span>
              <span className="tabular-nums text-fg">{gamma.toFixed(2)}</span>
            </div>
            <Slider min={0} max={1} step={0.01} value={[gamma]} onValueChange={(v) => set({ gamma: v[0] ?? 0 })} />
          </div>
          <Metric label="⟨Ω_E⟩_z" value={om.toFixed(4)} hint={`κ_UCF = ${KAPPA_UCF}`} />
        </div>
        <div>
          <h2 className="font-display text-xl tracking-tight">Cluster probe</h2>
          <p className="mt-2 text-sm text-muted">Illustrative nearby overdensities used as a local sampling check, not a survey catalog.</p>
          <div className="mt-4 divide-y divide-border rounded-xl bg-surface shadow-[var(--shadow-border)]">
            {CLUSTERS.map((c) => (
              <div key={c.name} className="flex items-baseline justify-between px-4 py-3">
                <div>
                  <div className="text-sm text-fg">{c.name}</div>
                  <div className="font-mono text-[10px] text-subtle">{c.rMly} Mly · rank {c.rank}</div>
                </div>
                <div className="font-mono text-sm tabular-nums text-fg">{c.hFactor.toFixed(4)}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
