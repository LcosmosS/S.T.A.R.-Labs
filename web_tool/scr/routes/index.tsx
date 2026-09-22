import { createFileRoute, Link } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { ArrowUpRight, Github } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { catalogStats, getCatalog } from "@/lib/star/catalog";
import { OrbitCloud } from "@/components/viz/orbit-cloud";
import { Formula as Eq, Metric, Sym } from "@/components/viz/formula";
import {
  getProjection,
  hEff,
  H0_PLANCK,
  H0_SHOES,
  MAPPING_META,
  MAPPING_ORDER,
  type ColorMode,
  type MappingFamily,
  type ProvenanceFilter,
} from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/")({ component: Home });

const LABS_URL = "https://github.com/LcosmosS/S.T.A.R.-Labs";

const CHAPTERS = [
  {
    to: "/charter",
    kicker: "Charter v1",
    title: "What the program asks",
    body: "Not “elliptic curves determine the universe.” Correspondence is a test: arithmetic maps vs independent structure, with locked nulls and a claim registry.",
  },
  {
    to: "/experiment",
    kicker: "RTCH-E1 · H₁–H₃",
    title: "Falsifiable topology",
    body: "Persistent H0, kNN Betti-1, N1 column-permutation nulls, rank–web, and a locked mapping-family benchmark.",
  },
  {
    to: "/projection",
    kicker: "2_STARMAP.md",
    title: "Official Φ map",
    body: "θ(Δ), φ(N), ρ(r), λ(Reg). Switch ACSC against MCJ, PTD, FT, and the historical rank-elevation family.",
  },
  {
    to: "/hubble",
    kicker: "S.T.A.R.",
    title: "Scale-dependent Hubble",
    body: "Local sampling of ⟨Ω_E⟩_z plus entropy curvature lifts H_eff at low z without touching last scatter.",
  },
  {
    to: "/cohomology",
    kicker: "ECC / RTCH",
    title: "Charge vs scalar",
    body: "Q_RTCH[Σ₂] = ∫ Φ*ω is global. 𝒥_Q = ¼ F_Q² is the local invariant that may enter A. They must not be conflated.",
  },
  {
    to: "/theory",
    kicker: "Status",
    title: "Established vs conjectural",
    body: "Pullbacks and conformal matter coupling are differential geometry. ACSC arithmetic-as-thermodynamics remains a conjecture until independently validated.",
  },
] as const;

const NOTEBOOKS = [
  { id: "00", title: "Registry overview" },
  { id: "01", title: "Preprocessing" },
  { id: "03", title: "Mapping benchmark" },
  { id: "05", title: "Rank topology" },
  { id: "06", title: "Null models" },
  { id: "07", title: "SFR prediction" },
] as const;

const COLOR_MODES: { id: ColorMode; label: string }[] = [
  { id: "rank", label: "Rank" },
  { id: "entropy", label: "Entropy" },
  { id: "omega", label: "Ω_E" },
  { id: "provenance", label: "Source" },
];

const PROVENANCE: { id: ProvenanceFilter; label: string }[] = [
  { id: "all", label: "All" },
  { id: "lmfdb", label: "Named" },
  { id: "synthetic", label: "Synthetic" },
];

function Home() {
  const beta = useLab((s) => s.beta);
  const gamma = useLab((s) => s.gamma);
  const z = useLab((s) => s.z);
  const set = useLab((s) => s.set);
  const selected = useLab((s) => s.selectedLabel);
  const family = useLab((s) => s.mappingFamily);
  const provenance = useLab((s) => s.provenance);
  const showFilaments = useLab((s) => s.showFilaments);
  const colorMode = useLab((s) => s.colorMode);
  const rankLift = useLab((s) => s.rankLift);
  const [query, setQuery] = useState("");
  const stats = catalogStats();
  const catalog = getCatalog();
  const Hnow = hEff(z, catalog, beta, gamma);
  const meta = MAPPING_META[family];
  const { points, links } = getProjection(family, provenance, rankLift);
  const curve = points.find((c) => c.label === selected) ?? points[0];

  const hits = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return catalog
      .filter((c) => c.label.toLowerCase().includes(q) || String(c.conductor).includes(q))
      .slice(0, 6);
  }, [catalog, query]);

  return (
    <div className="space-y-12">
      <section className="grid gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-end">
        <div>
          <Badge tone="steel">Observatory</Badge>
          <h1 className="mt-4 font-display text-4xl leading-[1.05] tracking-tight text-fg sm:text-5xl lg:text-6xl">
            Correspondence first. Physics later.
          </h1>
          <p className="mt-5 max-w-xl text-base leading-relaxed text-muted">
            STARMAP is the in-browser mapping engine for{" "}
            <a href={LABS_URL} target="_blank" rel="noreferrer" className="text-steel underline-offset-4 hover:underline">
              S.T.A.R. Labs
            </a>
            . It does not assume elliptic curves determine the universe. It tests whether a locked arithmetic map
            produces structure that was not used to construct it.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-6 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <Metric label="H_eff(z)" value={Hnow.toFixed(2)} unit="km/s/Mpc" hint={`z = ${z.toFixed(2)} · SH0ES ${H0_SHOES.toFixed(2)}`} />
          <Metric label="Planck H0" value={H0_PLANCK.toFixed(1)} unit="km/s/Mpc" hint="CMB anchor" />
          <Metric label="Curves" value={String(points.length)} hint={`${stats.famous} named · ${stats.ranks[1]} rank 1`} />
          <Metric label="⟨Ω_E⟩" value={stats.meanOmega.toFixed(3)} hint="catalog mean period" />
        </div>
      </section>

      <section className="overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]">
        <div className="flex flex-col gap-3 border-b border-border px-4 py-3 sm:px-5">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Φ(E) · {meta.label}</div>
              <p className="mt-1 max-w-xl text-xs leading-relaxed text-muted">{meta.note}</p>
            </div>
            <div className="font-mono text-[10px] text-muted">Drag to orbit · click a curve · scroll to zoom</div>
          </div>
          <div className="flex flex-wrap gap-1">
            {MAPPING_ORDER.map((id) => (
              <FamilyChip key={id} id={id} active={family === id} onClick={() => set({ mappingFamily: id })} />
            ))}
          </div>
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex flex-wrap items-center gap-1">
              {PROVENANCE.map((p) => (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => set({ provenance: p.id })}
                  className={chipClass(provenance === p.id)}
                >
                  {p.label}
                </button>
              ))}
              <span className="mx-1 h-4 w-px bg-border" />
              {COLOR_MODES.map((m) => (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => set({ colorMode: m.id })}
                  className={chipClass(colorMode === m.id)}
                >
                  {m.label}
                </button>
              ))}
            </div>
            <div className="flex flex-wrap items-center gap-4">
              <label className="flex h-11 items-center gap-2 text-xs text-muted">
                <Switch checked={showFilaments} onCheckedChange={(v) => set({ showFilaments: v })} />
                Filaments
              </label>
              <label className="flex h-11 items-center gap-2 text-xs text-muted">
                <Switch
                  checked={family === "rank-elev" ? true : rankLift}
                  disabled={family === "rank-elev"}
                  onCheckedChange={(v) => set({ rankLift: v })}
                />
                Rank lift
              </label>
            </div>
          </div>
        </div>

        <OrbitCloud
          points={points}
          links={links}
          selected={selected}
          onSelect={(label) => set({ selectedLabel: label })}
          colorMode={colorMode}
          showLinks={showFilaments}
          className="h-[min(62vh,540px)] w-full"
        />

        <div className="grid gap-4 border-t border-border px-4 py-4 sm:px-5 lg:grid-cols-[1.15fr_0.85fr]">
          {curve ? (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <Metric label="Label" value={curve.label} hint={curve.provenance} />
              <Metric label="Rank" value={String(curve.rank)} hint={`N = ${curve.conductor}`} />
              <Metric label="ρ_E" value={curve.rho.toFixed(3)} hint="(2/π) arctan(r)" />
              <Metric label="λ_E" value={curve.lambda.toFixed(3)} hint="regulator scale" />
              <Metric label="θ_E" value={curve.theta.toFixed(3)} hint="from |Δ|" />
              <Metric label="φ_E" value={curve.phi.toFixed(3)} hint="from N" />
              <Metric label="Ω_E" value={curve.omega.toFixed(4)} hint="real period" />
              <Metric label="Reg" value={curve.regulator.toFixed(4)} />
            </div>
          ) : (
            <p className="text-sm text-muted">Click a point in the cloud.</p>
          )}
          <div className="space-y-3">
            <div className="relative">
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Jump to label or conductor"
                aria-label="Search curves"
              />
              {hits.length > 0 ? (
                <ul className="absolute z-10 mt-1 w-full overflow-hidden rounded-md bg-elevated shadow-[var(--shadow-border)]">
                  {hits.map((c) => (
                    <li key={c.label}>
                      <button
                        type="button"
                        className="flex h-11 w-full items-center justify-between px-3 text-left text-sm hover:bg-surface"
                        onClick={() => {
                          set({ selectedLabel: c.label });
                          setQuery("");
                        }}
                      >
                        <span className="font-mono">{c.label}</span>
                        <span className="font-mono text-xs text-muted">r = {c.rank}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              ) : null}
            </div>
            <div>
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Redshift z</span>
                <span className="font-mono text-xs tabular-nums text-fg">{z.toFixed(2)}</span>
              </div>
              <Slider min={0} max={2.4} step={0.01} value={[z]} onValueChange={(v) => set({ z: v[0] ?? 0 })} />
            </div>
          </div>
        </div>
        {meta.circularRank ? (
          <p className="border-t border-border px-5 py-3 text-xs text-warn">
            Rank-elev puts rank on an axis. Do not read filament structure here as support for ACSC.
          </p>
        ) : null}
      </section>

      <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
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
          <h2 className="font-display text-2xl tracking-tight">Null hypothesis</h2>
          <p className="mt-3 text-sm leading-relaxed text-muted">
            Appendix B of the variational paper isolates a single extra parameter. The extended model is supported only
            insofar as β_Q improves prediction while surviving independent nulls.
          </p>
          <div className="mt-5">
            <Eq boxed>
              H<sub className="font-sans text-sm not-italic">0</sub> : β<sub>Q</sub> = 0
            </Eq>
          </div>
        </div>
        <div>
          <h2 className="font-display text-2xl tracking-tight">Official ACSC map</h2>
          <p className="mt-3 text-sm leading-relaxed text-muted">
            The 5-tuple from 2_STARMAP.md. The cloud is a 3-embedding; rank is held out of position unless Rank lift is
            on.
          </p>
          <div className="mt-5">
            <Eq boxed>
              <Sym>Φ</Sym>(E) = (sin φ cos θ, sin φ sin θ, cos φ, ρ, λ)
            </Eq>
          </div>
        </div>
      </section>

      <section className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
        <div className="flex items-center justify-between gap-3">
          <h2 className="font-display text-xl tracking-tight">Controlled notebooks</h2>
          <a
            href={`${LABS_URL}/tree/main/notebooks`}
            target="_blank"
            rel="noreferrer"
            className="inline-flex h-11 items-center gap-2 text-sm text-steel hover:text-fg"
          >
            <Github className="size-4" />
            Open in Labs
          </a>
        </div>
        <ul className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {NOTEBOOKS.map((nb) => (
            <li key={nb.id} className="flex items-baseline gap-3 text-sm">
              <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">{nb.id}</span>
              <span className="text-muted">{nb.title}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

function FamilyChip({ id, active, onClick }: { id: MappingFamily; active: boolean; onClick: () => void }) {
  return (
    <button type="button" onClick={onClick} className={chipClass(active)}>
      {MAPPING_META[id].short}
    </button>
  );
}

function chipClass(active: boolean) {
  return cn(
    "h-11 rounded-md px-3 text-sm",
    active ? "bg-primary text-primary-fg" : "bg-elevated text-muted shadow-[var(--shadow-border)]",
  );
}
