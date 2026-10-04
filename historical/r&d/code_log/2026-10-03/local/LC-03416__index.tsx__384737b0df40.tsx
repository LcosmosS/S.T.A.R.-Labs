import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowUpRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { catalogStats, getCatalog } from "@/lib/star/catalog";
import { OrbitCloud } from "@/components/viz/orbit-cloud";
import { Formula as Eq, Metric, Sym } from "@/components/viz/formula";
import { FILAMENTS, hEff, H0_PLANCK, H0_SHOES, PROJECTED } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";

export const Route = createFileRoute("/")({ component: Home });

const CHAPTERS = [
  {
    to: "/projection",
    kicker: "ACSC",
    title: "Arithmetic projection",
    body: "Elliptic-curve invariants (rank, conductor, regulator, real period) map through Φ onto a cosmological manifold.",
  },
  {
    to: "/cohomology",
    kicker: "ECC / RTCH",
    title: "Entropy cohomology",
    body: "A closed target 2-form ω pulls back to F_Q. The charge Q_RTCH is global; the scalar I_Q is not.",
  },
  {
    to: "/hubble",
    kicker: "S.T.A.R.",
    title: "Scale-dependent Hubble",
    body: "Local sampling of ⟨Ω_E⟩_z and entropy curvature lift H_eff at low z without touching the CMB.",
  },
] as const;

function Home() {
  const beta = useLab((s) => s.beta);
  const gamma = useLab((s) => s.gamma);
  const stats = catalogStats();
  const Hnow = hEff(0, getCatalog(), beta, gamma);

  return (
    <div className="space-y-12">
      <section className="grid gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-end">
        <div>
          <Badge tone="steel">Observatory</Badge>
          <h1 className="mt-4 font-display text-4xl leading-[1.05] tracking-tight text-fg sm:text-5xl lg:text-6xl">
            The universe, projected from arithmetic.
          </h1>
          <p className="mt-5 max-w-xl text-base leading-relaxed text-muted">
            STARMAP is a working laboratory for the S.T.A.R. Program — Symbolic–Topological–Arithmetic Relativity —
            and the fully variational RTCH master action. Drag the manifold. Open a lab.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-6 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <Metric label="H_eff(0)" value={Hnow.toFixed(2)} unit="km/s/Mpc" hint={`SH0ES ${H0_SHOES.toFixed(2)}`} />
          <Metric label="Planck H0" value={H0_PLANCK.toFixed(1)} unit="km/s/Mpc" hint="CMB anchor" />
          <Metric label="Curves" value={String(stats.n)} hint={`rank 0–4 · ${stats.ranks[1]} of rank 1`} />
          <Metric label="⟨Ω_E⟩" value={stats.meanOmega.toFixed(3)} hint="catalog mean period" />
        </div>
      </section>

      <section className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
        <div className="flex items-center justify-between px-5 py-3">
          <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Φ(E) · arithmetic point cloud</div>
          <div className="font-mono text-[10px] text-muted">Drag to orbit · click a curve</div>
        </div>
        <OrbitCloud points={PROJECTED} links={FILAMENTS} className="h-[min(62vh,540px)] w-full" />
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {CHAPTERS.map((c) => (
          <Link
            key={c.to}
            to={c.to}
            className="group rounded-xl bg-surface p-5 shadow-[var(--shadow-border)] transition-[box-shadow] duration-150 hover:shadow-[var(--shadow-border-hover)]"
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-steel">{c.kicker}</span>
              <ArrowUpRight className="size-4 text-subtle transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
            </div>
            <h2 className="mt-3 font-display text-2xl tracking-tight">{c.title}</h2>
            <p className="mt-2 text-sm leading-relaxed text-muted">{c.body}</p>
          </Link>
        ))}
      </section>

      <section className="grid gap-8 lg:grid-cols-2">
        <div>
          <h2 className="font-display text-2xl tracking-tight">Effective expansion</h2>
          <p className="mt-3 text-sm leading-relaxed text-muted">
            The S.T.A.R. prediction is a scale-dependent Hubble parameter sourced by the weighted real period of
            curves visible at redshift z, plus entropy-curvature and metric-trace corrections that vanish at last
            scatter.
          </p>
          <div className="mt-5">
            <Eq boxed>
              <Sym>H</Sym>
              <sub className="font-sans text-sm not-italic">eff</sub>
              (z) = H<sub className="font-sans text-sm not-italic">0</sub> · ⟨Ω<sub>E</sub>⟩<sub>z</sub>
            </Eq>
          </div>
        </div>
        <div>
          <h2 className="font-display text-2xl tracking-tight">Topological charge</h2>
          <p className="mt-3 text-sm leading-relaxed text-muted">
            RTCH does not identify entropy with a local scalar. The observable pairing is cohomological: a closed
            target form pulled back along the thermodynamic map, integrated on a two-cycle.
          </p>
          <div className="mt-5">
            <Eq boxed>
              Q<sub className="font-sans text-sm not-italic">RTCH</sub>[Σ<sub>2</sub>] = ∫<sub>Σ₂</sub> Φ<sup>*</sup>ω
            </Eq>
          </div>
        </div>
      </section>
    </div>
  );
}
