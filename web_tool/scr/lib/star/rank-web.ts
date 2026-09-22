import { mulberry32 } from "./rng";
import {
  getProjection,
  MAPPING_META,
  MAPPING_ORDER,
  type MappingFamily,
  type Projected,
} from "./physics";

export type EnvLabel = "void" | "filament" | "cluster";

export type RankWebResult = {
  n: number;
  nPerm: number;
  family: MappingFamily;
  circularRank: boolean;
  counts: Record<EnvLabel, number>;
  meanRank: Record<EnvLabel, number>;
  table: number[][];
  chi2: number;
  p: number;
  permMean: number;
  permStd: number;
  verdict: string;
  environments: Array<{ label: string; rank: number; env: EnvLabel; density: number }>;
};

function knnDensity(points: Projected[], k = 6): number[] {
  const n = points.length;
  const dens = new Array<number>(n);
  for (let i = 0; i < n; i++) {
    const a = points[i]!;
    const ds: number[] = [];
    for (let j = 0; j < n; j++) {
      if (i === j) continue;
      const b = points[j]!;
      ds.push((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2);
    }
    ds.sort((u, v) => u - v);
    let s = 0;
    for (let t = 0; t < k && t < ds.length; t++) s += Math.sqrt(ds[t]!);
    dens[i] = k / Math.max(1e-9, s);
  }
  return dens;
}

function tertile(values: number[]): [(v: number) => EnvLabel, number, number] {
  const sorted = values.slice().sort((a, b) => a - b);
  const q = (p: number) => {
    const i = (sorted.length - 1) * p;
    const lo = Math.floor(i);
    const hi = Math.ceil(i);
    return sorted[lo]! + (sorted[hi]! - sorted[lo]!) * (i - lo);
  };
  const t1 = q(1 / 3);
  const t2 = q(2 / 3);
  return [(v) => (v < t1 ? "void" : v < t2 ? "filament" : "cluster"), t1, t2];
}

function chiSquare(table: number[][]): number {
  const rows = table.length;
  const cols = table[0]?.length ?? 0;
  const rowSum = table.map((r) => r.reduce((a, b) => a + b, 0));
  const colSum = Array.from({ length: cols }, (_, j) => table.reduce((a, r) => a + (r[j] ?? 0), 0));
  const n = rowSum.reduce((a, b) => a + b, 0);
  let chi = 0;
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const e = (rowSum[i]! * colSum[j]!) / Math.max(1, n);
      if (e <= 0) continue;
      const o = table[i]![j]!;
      chi += (o - e) ** 2 / e;
    }
  }
  return chi;
}

function tableFrom(ranks: number[], envs: EnvLabel[]): number[][] {
  const rankBucket = (r: number) => (r <= 0 ? 0 : r === 1 ? 1 : 2);
  const envIdx = (e: EnvLabel) => (e === "void" ? 0 : e === "filament" ? 1 : 2);
  const table = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
  ];
  for (let i = 0; i < ranks.length; i++) {
    table[rankBucket(ranks[i]!)]![envIdx(envs[i]!)]! += 1;
  }
  return table;
}

/** H₁–H₃: rank vs local-density environment on Φ(E). Null: shuffle ranks. */
export function runRankWeb(nPerm = 240, seed = 20260919, family: MappingFamily = "acsc"): RankWebResult {
  const points = getProjection(family, "all", false).points;
  const dens = knnDensity(points, 6);
  const [classify] = tertile(dens);
  const envs = dens.map(classify);
  const ranks = points.map((p) => p.rank);
  const obsTable = tableFrom(ranks, envs);
  const chi2 = chiSquare(obsTable);
  const circularRank = MAPPING_META[family].circularRank;

  const rng = mulberry32(seed);
  const samples: number[] = [];
  const work = ranks.slice();
  for (let p = 0; p < nPerm; p++) {
    for (let i = work.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      const t = work[i]!;
      work[i] = work[j]!;
      work[j] = t;
    }
    samples.push(chiSquare(tableFrom(work, envs)));
  }
  const more = samples.filter((s) => s >= chi2).length;
  const p = (more + 1) / (nPerm + 1);
  const mean = samples.reduce((a, b) => a + b, 0) / nPerm;
  const std = Math.sqrt(samples.reduce((a, b) => a + (b - mean) ** 2, 0) / Math.max(1, nPerm - 1));

  const meanRank: Record<EnvLabel, number> = { void: 0, filament: 0, cluster: 0 };
  const counts: Record<EnvLabel, number> = { void: 0, filament: 0, cluster: 0 };
  for (let i = 0; i < points.length; i++) {
    const e = envs[i]!;
    counts[e] += 1;
    meanRank[e] += ranks[i]!;
  }
  (Object.keys(meanRank) as EnvLabel[]).forEach((k) => {
    meanRank[k] = counts[k] ? meanRank[k] / counts[k] : 0;
  });

  const verdict = circularRank
    ? "This family puts rank on an axis. Association with local density is expected and is not evidence for ACSC."
    : p < 0.05
      ? "Rank and local-density environment on this map are associated beyond shuffled-rank nulls. Geometric correspondence in the chosen projection — not a physical identification of rank with clusters."
      : "Rank is statistically indistinguishable from a shuffled assignment at this sample size. A null result is the scientifically useful outcome for H₁–H₃.";

  return {
    n: points.length,
    nPerm,
    family,
    circularRank,
    counts,
    meanRank,
    table: obsTable,
    chi2,
    p,
    permMean: mean,
    permStd: std,
    verdict,
    environments: points.map((pt, i) => ({
      label: pt.label,
      rank: pt.rank,
      env: envs[i]!,
      density: dens[i]!,
    })),
  };
}

export type FamilyBenchmark = {
  family: MappingFamily;
  label: string;
  chi2: number;
  p: number;
  circularRank: boolean;
  signal: boolean;
};

/** Notebook 03 analogue: locked rank–web across mapping families. */
export function compareMappingFamilies(nPerm = 96, seed = 20260921): FamilyBenchmark[] {
  return MAPPING_ORDER.map((family) => {
    const r = runRankWeb(nPerm, seed, family);
    return {
      family,
      label: MAPPING_META[family].label,
      chi2: r.chi2,
      p: r.p,
      circularRank: r.circularRank,
      signal: !r.circularRank && r.p < 0.05,
    };
  });
}
