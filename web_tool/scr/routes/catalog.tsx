import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Metric } from "@/components/viz/formula";
import { catalogStats, getCatalog } from "@/lib/star/catalog";
import { useLab } from "@/lib/star/store";

export const Route = createFileRoute("/catalog")({ component: CatalogPage });

function CatalogPage() {
  const [q, setQ] = useState("");
  const [rank, setRank] = useState<number | "all">("all");
  const selected = useLab((s) => s.selectedLabel);
  const set = useLab((s) => s.set);
  const curves = getCatalog();
  const stats = catalogStats();

  const rows = useMemo(() => {
    const query = q.trim().toLowerCase();
    return curves.filter((c) => {
      if (rank !== "all" && c.rank !== rank) return false;
      if (!query) return true;
      return c.label.toLowerCase().includes(query) || String(c.conductor).includes(query) || c.torsion.toLowerCase().includes(query);
    });
  }, [curves, q, rank]);

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge>LMFDB-style seed</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Elliptic-curve catalog</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Named curves keep their LMFDB labels. The remainder is a synthetic, seeded draw used so the projection and
          RTCH-E1 pipeline can run entirely in the browser. Rank is a response variable — never part of the primary
          topology metric.
        </p>
      </header>

      <div className="grid gap-4 sm:grid-cols-4">
        <Metric label="Curves" value={String(stats.n)} hint={`${stats.famous} named`} />
        <Metric label="Rank 0 / 1" value={`${stats.ranks[0]} / ${stats.ranks[1]}`} />
        <Metric label="Rank 2+" value={String(stats.ranks[2] + stats.ranks[3] + stats.ranks[4])} />
        <Metric label="⟨Ω_E⟩" value={stats.meanOmega.toFixed(3)} />
      </div>

      <div className="flex flex-col gap-3 sm:flex-row">
        <Input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search label, conductor, torsion"
          aria-label="Search catalog"
        />
        <div className="flex flex-wrap gap-1">
          {(["all", 0, 1, 2, 3, 4] as const).map((r) => (
            <button
              key={String(r)}
              type="button"
              onClick={() => setRank(r)}
              className={`h-11 rounded-md px-3 text-sm ${rank === r ? "bg-primary text-primary-fg" : "bg-elevated text-muted shadow-[var(--shadow-border)]"}`}
            >
              {r === "all" ? "All ranks" : `r = ${r}`}
            </button>
          ))}
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl bg-surface shadow-[var(--shadow-border)]">
        <table className="w-full min-w-[720px] text-left text-sm">
          <thead className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">
            <tr>
              <th className="px-4 py-3">Label</th>
              <th className="px-3 py-3">N</th>
              <th className="px-3 py-3">r</th>
              <th className="px-3 py-3">R</th>
              <th className="px-3 py-3">Ω</th>
              <th className="px-3 py-3">Δ</th>
              <th className="px-3 py-3">Tors</th>
              <th className="px-3 py-3">Src</th>
            </tr>
          </thead>
          <tbody>
            {rows.slice(0, 80).map((c) => {
              const on = c.label === selected;
              return (
                <tr
                  key={c.label}
                  className={`cursor-pointer border-t border-border ${on ? "bg-elevated" : "hover:bg-elevated/60"}`}
                  onClick={() => set({ selectedLabel: c.label })}
                >
                  <td className="px-4 py-2 font-mono text-fg">{c.label}</td>
                  <td className="px-3 py-2 font-mono tabular-nums text-muted">{c.conductor}</td>
                  <td className="px-3 py-2 font-mono tabular-nums">{c.rank}</td>
                  <td className="px-3 py-2 font-mono tabular-nums text-muted">{c.regulator.toFixed(4)}</td>
                  <td className="px-3 py-2 font-mono tabular-nums">{c.omega.toFixed(4)}</td>
                  <td className="px-3 py-2 font-mono tabular-nums text-muted">{c.disc}</td>
                  <td className="px-3 py-2 font-mono text-muted">{c.torsion}</td>
                  <td className="px-3 py-2">
                    <Badge tone={c.provenance === "lmfdb" ? "ok" : "default"}>{c.provenance}</Badge>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {rows.length > 80 ? (
          <div className="border-t border-border px-4 py-3 font-mono text-[11px] text-subtle">
            Showing 80 of {rows.length} matches
          </div>
        ) : null}
      </div>
    </div>
  );
}
