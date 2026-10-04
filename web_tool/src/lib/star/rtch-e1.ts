import { getCatalog, intrinsicFeatures, INTRINSIC_NAMES, type Curve } from "./catalog";
import { mulberry32 } from "./rng";

export type Interval = { dim: 0 | 1; birth: number; death: number; persistence: number };

export type GeodesicPair = {
  i: number;
  j: number;
  graph: number;
  chord: number;
  tortuosity: number;
};

export type ExperimentResult = {
  kind: "catalog" | "torus" | "scrambled";
  n: number;
  features: string[];
  seed: number;
  nNulls: number;
  k: number;
  intervals: Interval[];
  h0Max: number;
  h0Mean: number;
  betti1: number;
  cycleBirths: number[];
  geodesic: { meanTort: number; medianTort: number; pairs: GeodesicPair[] };
  pca: Array<{ x: number; y: number; rank: number; label: string }>;
  nullH0: { mean: number; std: number; p: number; samples: number[] };
  nullBetti: { mean: number; std: number; p: number; samples: number[] };
  nullTort: { mean: number; std: number; p: number; samples: number[] };
  verdict: string;
  caveats: string[];
};

function robustScale(X: number[][]): number[][] {
  const d = X[0]?.length ?? 0;
  const n = X.length;
  const med: number[] = [];
  const iqr: number[] = [];
  for (let j = 0; j < d; j++) {
    const col = X.map((r) => r[j]!).sort((a, b) => a - b);
    const q = (p: number) => {
      const i = (n - 1) * p;
      const lo = Math.floor(i);
      const hi = Math.ceil(i);
      return col[lo]! + (col[hi]! - col[lo]!) * (i - lo);
    };
    const m = q(0.5);
    const s = q(0.9) - q(0.1);
    med.push(m);
    iqr.push(s < 1e-9 ? 1 : s);
  }
  return X.map((row) => row.map((v, j) => (v - med[j]!) / iqr[j]!));
}

function dist2(a: number[], b: number[]) {
  let s = 0;
  for (let i = 0; i < a.length; i++) {
    const d = a[i]! - b[i]!;
    s += d * d;
  }
  return s;
}

class UnionFind {
  parent: Int32Array;
  rank: Int32Array;
  constructor(n: number) {
    this.parent = new Int32Array(n);
    this.rank = new Int32Array(n);
    for (let i = 0; i < n; i++) this.parent[i] = i;
  }
  find(i: number): number {
    let p = i;
    while (this.parent[p] !== p) {
      this.parent[p] = this.parent[this.parent[p]!]!;
      p = this.parent[p]!;
    }
    return p;
  }
  union(a: number, b: number) {
    let ra = this.find(a);
    let rb = this.find(b);
    if (ra === rb) return false;
    if (this.rank[ra]! < this.rank[rb]!) [ra, rb] = [rb, ra];
    this.parent[rb] = ra;
    if (this.rank[ra] === this.rank[rb]) this.rank[ra]! += 1;
    return true;
  }
}

function h0FromPoints(X: number[][]): Interval[] {
  const n = X.length;
  const edges: Array<{ i: number; j: number; d: number }> = [];
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      edges.push({ i, j, d: Math.sqrt(dist2(X[i]!, X[j]!)) });
    }
  }
  edges.sort((a, b) => a.d - b.d);
  const uf = new UnionFind(n);
  const intervals: Interval[] = [];
  for (const e of edges) {
    if (uf.union(e.i, e.j)) {
      intervals.push({ dim: 0, birth: 0, death: e.d, persistence: e.d });
      if (intervals.length === n - 1) break;
    }
  }
  return intervals;
}

type Graph = { adj: number[][]; w: number[][]; edges: number; components: number; betti1: number; cycleBirths: number[] };

function knnGraph(X: number[][], k: number): Graph {
  const n = X.length;
  const adj: number[][] = Array.from({ length: n }, () => []);
  const w: number[][] = Array.from({ length: n }, () => []);
  const seen = new Set<string>();
  for (let i = 0; i < n; i++) {
    const ds: Array<{ j: number; d: number }> = [];
    for (let j = 0; j < n; j++) {
      if (i === j) continue;
      ds.push({ j, d: Math.sqrt(dist2(X[i]!, X[j]!)) });
    }
    ds.sort((a, b) => a.d - b.d);
    for (let t = 0; t < k && t < ds.length; t++) {
      const j = ds[t]!.j;
      const key = i < j ? `${i}-${j}` : `${j}-${i}`;
      if (seen.has(key)) continue;
      seen.add(key);
      adj[i]!.push(j);
      adj[j]!.push(i);
      w[i]!.push(ds[t]!.d);
      w[j]!.push(ds[t]!.d);
    }
  }
  const uf = new UnionFind(n);
  const cycleBirths: number[] = [];
  const edgeList: Array<{ i: number; j: number; d: number }> = [];
  for (let i = 0; i < n; i++) {
    for (let t = 0; t < adj[i]!.length; t++) {
      const j = adj[i]![t]!;
      if (i < j) edgeList.push({ i, j, d: w[i]![t]! });
    }
  }
  edgeList.sort((a, b) => a.d - b.d);
  let tree = 0;
  for (const e of edgeList) {
    if (uf.union(e.i, e.j)) tree += 1;
    else cycleBirths.push(e.d);
  }
  const roots = new Set<number>();
  for (let i = 0; i < n; i++) roots.add(uf.find(i));
  const components = roots.size;
  const edges = edgeList.length;
  const betti1 = Math.max(0, edges - n + components);
  return { adj, w, edges, components, betti1, cycleBirths };
}

function dijkstra(graph: Graph, src: number): Float64Array {
  const n = graph.adj.length;
  const dist = new Float64Array(n);
  dist.fill(Infinity);
  dist[src] = 0;
  const used = new Uint8Array(n);
  for (let iter = 0; iter < n; iter++) {
    let u = -1;
    let best = Infinity;
    for (let i = 0; i < n; i++) {
      if (!used[i] && dist[i]! < best) {
        best = dist[i]!;
        u = i;
      }
    }
    if (u < 0) break;
    used[u] = 1;
    const nbr = graph.adj[u]!;
    for (let t = 0; t < nbr.length; t++) {
      const v = nbr[t]!;
      const nd = dist[u]! + graph.w[u]![t]!;
      if (nd < dist[v]!) dist[v] = nd;
    }
  }
  return dist;
}

function geodesicSample(X: number[][], graph: Graph, nPairs: number, rng: () => number): GeodesicPair[] {
  const n = X.length;
  const pairs: GeodesicPair[] = [];
  const neighbor = new Set<string>();
  for (let i = 0; i < n; i++) {
    for (const j of graph.adj[i]!) neighbor.add(i < j ? `${i}-${j}` : `${j}-${i}`);
  }
  let tries = 0;
  while (pairs.length < nPairs && tries < nPairs * 40) {
    tries += 1;
    const i = Math.floor(rng() * n);
    const j = Math.floor(rng() * n);
    if (i === j) continue;
    const key = i < j ? `${i}-${j}` : `${j}-${i}`;
    if (neighbor.has(key)) continue;
    const dist = dijkstra(graph, i);
    const g = dist[j]!;
    if (!Number.isFinite(g) || g <= 0) continue;
    const chord = Math.sqrt(dist2(X[i]!, X[j]!));
    if (chord < 1e-9) continue;
    pairs.push({ i, j, graph: g, chord, tortuosity: g / chord });
  }
  return pairs;
}

function pca2(X: number[][]): Array<{ x: number; y: number }> {
  const n = X.length;
  const d = X[0]?.length ?? 0;
  const mean = new Array(d).fill(0);
  for (const row of X) for (let j = 0; j < d; j++) mean[j] += row[j]!;
  for (let j = 0; j < d; j++) mean[j] /= n;
  const C = Array.from({ length: d }, () => new Array(d).fill(0));
  for (const row of X) {
    for (let a = 0; a < d; a++) {
      for (let b = 0; b < d; b++) {
        C[a]![b] += (row[a]! - mean[a]!) * (row[b]! - mean[b]!);
      }
    }
  }
  for (let a = 0; a < d; a++) for (let b = 0; b < d; b++) C[a]![b]! /= Math.max(1, n - 1);

  function power(mat: number[][], iters = 40) {
    let v = new Array(d).fill(0).map((_, i) => (i === 0 ? 1 : 0.07 * i));
    let norm = Math.hypot(...v) || 1;
    v = v.map((x) => x / norm);
    for (let t = 0; t < iters; t++) {
      const nv = new Array(d).fill(0);
      for (let i = 0; i < d; i++) for (let j = 0; j < d; j++) nv[i] += mat[i]![j]! * v[j]!;
      norm = Math.hypot(...nv) || 1;
      v = nv.map((x) => x / norm);
    }
    return v;
  }
  const v1 = power(C);
  const C2 = C.map((row, i) =>
    row.map((c, j) => {
      let dot = 0;
      for (let k = 0; k < d; k++) for (let l = 0; l < d; l++) dot += v1[k]! * C[k]![l]! * v1[l]!;
      return c - dot * v1[i]! * v1[j]!;
    }),
  );
  const v2 = power(C2);
  return X.map((row) => {
    let x = 0;
    let y = 0;
    for (let j = 0; j < d; j++) {
      const z = row[j]! - mean[j]!;
      x += z * v1[j]!;
      y += z * v2[j]!;
    }
    return { x, y };
  });
}

function permuteColumns(X: number[][], rng: () => number): number[][] {
  const n = X.length;
  const d = X[0]?.length ?? 0;
  const out = X.map((r) => r.slice());
  for (let j = 0; j < d; j++) {
    for (let i = n - 1; i > 0; i--) {
      const k = Math.floor(rng() * (i + 1));
      const tmp = out[i]![j]!;
      out[i]![j] = out[k]![j]!;
      out[k]![j] = tmp;
    }
  }
  return out;
}

function stats(samples: number[], observed: number) {
  const n = samples.length;
  const mean = samples.reduce((a, b) => a + b, 0) / Math.max(1, n);
  const var_ = samples.reduce((a, b) => a + (b - mean) ** 2, 0) / Math.max(1, n - 1);
  const std = Math.sqrt(var_);
  const more = samples.filter((s) => s >= observed).length;
  const p = (more + 1) / (n + 1);
  return { mean, std, p, samples };
}

function torusSample(n: number, rng: () => number): number[][] {
  const R = 2;
  const r = 1;
  const pts: number[][] = [];
  for (let i = 0; i < n; i++) {
    const u = rng() * Math.PI * 2;
    const v = rng() * Math.PI * 2;
    pts.push([
      (R + r * Math.cos(v)) * Math.cos(u),
      (R + r * Math.cos(v)) * Math.sin(u),
      r * Math.sin(v),
      0.15 * Math.sin(2 * u),
      0.15 * Math.cos(3 * v),
    ]);
  }
  return pts;
}

function matrixFromCurves(curves: Curve[]): { X: number[][]; labels: string[]; ranks: number[] } {
  const raw = curves.map(intrinsicFeatures);
  return {
    X: robustScale(raw),
    labels: curves.map((c) => c.label),
    ranks: curves.map((c) => c.rank),
  };
}

function summarize(X: number[][], k: number, nPairs: number, rng: () => number) {
  const intervals = h0FromPoints(X);
  const graph = knnGraph(X, k);
  const pairs = geodesicSample(X, graph, nPairs, rng);
  const torts = pairs.map((p) => p.tortuosity);
  const meanTort = torts.length ? torts.reduce((a, b) => a + b, 0) / torts.length : 1;
  const sorted = torts.slice().sort((a, b) => a - b);
  const medianTort = sorted.length ? sorted[Math.floor(sorted.length / 2)]! : 1;
  const h0Max = intervals.reduce((m, iv) => Math.max(m, iv.persistence), 0);
  const h0Mean = intervals.length ? intervals.reduce((s, iv) => s + iv.persistence, 0) / intervals.length : 0;
  return {
    intervals,
    graph,
    pairs,
    meanTort,
    medianTort,
    h0Max,
    h0Mean,
  };
}

export function runExperiment(opts: {
  kind: "catalog" | "torus" | "scrambled";
  nNulls?: number;
  k?: number;
  seed?: number;
  nPairs?: number;
}): ExperimentResult {
  const nNulls = opts.nNulls ?? 24;
  const k = opts.k ?? 8;
  const seed = opts.seed ?? 20260917;
  const nPairs = opts.nPairs ?? 40;
  const rng = mulberry32(seed);

  const curves = getCatalog();
  let X: number[][];
  let labels: string[];
  let ranks: number[];
  if (opts.kind === "torus") {
    X = robustScale(torusSample(Math.min(220, curves.length), rng));
    labels = X.map((_, i) => `T${i}`);
    ranks = X.map(() => 0);
  } else {
    const m = matrixFromCurves(curves);
    X = m.X;
    labels = m.labels;
    ranks = m.ranks;
    if (opts.kind === "scrambled") X = permuteColumns(X, rng);
  }

  const obs = summarize(X, k, nPairs, rng);
  const pcaCoords = pca2(X);

  const nullH0s: number[] = [];
  const nullB1: number[] = [];
  const nullT: number[] = [];
  for (let n = 0; n < nNulls; n++) {
    const Xp = permuteColumns(X, rng);
    const s = summarize(Xp, k, Math.min(16, nPairs), rng);
    nullH0s.push(s.h0Max);
    nullB1.push(s.graph.betti1);
    nullT.push(s.meanTort);
  }

  const nullH0 = stats(nullH0s, obs.h0Max);
  const nullBetti = stats(nullB1, obs.graph.betti1);
  const nullTort = stats(nullT, obs.meanTort);

  const survive =
    opts.kind === "torus"
      ? obs.graph.betti1 >= 2
      : nullH0.p < 0.05 || nullBetti.p < 0.05;

  const verdict =
    opts.kind === "torus"
      ? obs.graph.betti1 >= 2
        ? "Positive control: the sampled torus retains extra 1-cycles in its kNN graph, as required."
        : "Positive control failed — increase sample size or k. A sparse kNN graph is not a VR complex."
      : opts.kind === "scrambled"
        ? "Scrambled columns destroy joint structure. This is the N1 null geometry itself."
        : survive
          ? "Observed topology exceeds the N1 column-permutation null at α = 0.05 on at least one statistic. This is evidence of structure in the sampled metric, not a proof that T is a manifold with H^k ≠ 0."
          : "Observed topology is statistically indistinguishable from the N1 null at this sample size. A null result is scientifically useful.";

  return {
    kind: opts.kind,
    n: X.length,
    features: INTRINSIC_NAMES,
    seed,
    nNulls,
    k,
    intervals: obs.intervals.slice().sort((a, b) => b.persistence - a.persistence).slice(0, 24),
    h0Max: obs.h0Max,
    h0Mean: obs.h0Mean,
    betti1: obs.graph.betti1,
    cycleBirths: obs.graph.cycleBirths.slice(0, 24),
    geodesic: { meanTort: obs.meanTort, medianTort: obs.medianTort, pairs: obs.pairs.slice(0, 8) },
    pca: pcaCoords.map((p, i) => ({ ...p, rank: ranks[i] ?? 0, label: labels[i] ?? String(i) })),
    nullH0,
    nullBetti,
    nullTort,
    verdict,
    caveats: [
      "Persistent H_k of a finite point cloud is not a proof that the arithmetic state space is a smooth manifold.",
      "Rank is excluded from the primary feature metric (RTCH-E1 protocol).",
      "Graph Betti-1 is computed on a kNN graph, not a complete Vietoris–Rips complex.",
      "N1 independently permutes each feature column, preserving every marginal.",
    ],
  };
}
