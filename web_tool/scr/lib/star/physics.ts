import { type Curve, getCatalog } from "./catalog";

export const H0_PLANCK = 67.4;
export const H0_SHOES = 73.04;
export const OMEGA_M = 0.315;
export const OMEGA_L = 0.685;
export const Z_STAR = 1100;

export type Vec3 = { x: number; y: number; z: number };

export type MappingFamily = "acsc" | "mcj" | "ptd" | "ft" | "rank-elev";
export type ProvenanceFilter = "all" | "lmfdb" | "synthetic";
export type ColorMode = "rank" | "entropy" | "omega" | "provenance";

export const MAPPING_META: Record<
  MappingFamily,
  { label: string; short: string; note: string; circularRank: boolean }
> = {
  acsc: {
    label: "ACSC Φ",
    short: "ACSC",
    note: "Official 2_STARMAP.md map: (Δ, N, r, Reg) → (θ, φ, ρ, λ)",
    circularRank: false,
  },
  mcj: {
    label: "MCJ",
    short: "MCJ",
    note: "j-invariant angular map — alternative family for locked comparison",
    circularRank: false,
  },
  ptd: {
    label: "PTD",
    short: "PTD",
    note: "Weierstrass a-invariants (a₁…a₆) as algebraic coordinates",
    circularRank: false,
  },
  ft: {
    label: "FT",
    short: "FT",
    note: "Frobenius-like analogue from conductor residue and b-invariants",
    circularRank: false,
  },
  "rank-elev": {
    label: "Rank-elev",
    short: "z ∝ r",
    note: "Historical ACSC-007 elevation z ∝ rank. Rank–web on this family is circular.",
    circularRank: true,
  },
};

export const MAPPING_ORDER: MappingFamily[] = ["acsc", "mcj", "ptd", "ft", "rank-elev"];

export type Projected = Curve & {
  x: number;
  y: number;
  z: number;
  entropy: number;
  cohClass: number;
  theta: number;
  phi: number;
  rho: number;
  lambda: number;
  family: MappingFamily;
};

function acscAngles(c: Curve) {
  const absD = Math.max(1e-12, Math.abs(c.disc));
  const theta = (2 * Math.PI * Math.log(absD)) / (1 + Math.log1p(absD));
  const phi = (Math.PI * Math.log(Math.max(1, c.conductor))) / (1 + Math.log1p(c.conductor));
  const rho = (2 / Math.PI) * Math.atan(c.rank);
  const lambda = Math.log1p(c.regulator) / (1 + Math.log1p(c.regulator));
  return { theta, phi, rho, lambda };
}

function sphere(theta: number, phi: number, rad: number) {
  return {
    x: rad * Math.sin(phi) * Math.cos(theta),
    y: rad * Math.sin(phi) * Math.sin(theta),
    z: rad * Math.cos(phi),
  };
}

/**
 * ACSC Φ from 2_STARMAP.md:
 *   θ = 2π log|Δ| / (1 + log(1+|Δ|))
 *   φ = π log N / (1 + log(1+N))
 *   ρ = (2/π) arctan(r)
 *   λ = log(1+Reg) / (1 + log(1+Reg))
 *   Φ = (sinφ cosθ, sinφ sinθ, cosφ, ρ, λ)
 * The 3-cloud is a 3-embedding of that 5-tuple. Rank is held out of position
 * unless rankLift is on or the family is the historical rank-elev map.
 */
export function projectCurve(c: Curve, family: MappingFamily = "acsc", rankLift = false): Projected {
  const { theta: thA, phi: phA, rho, lambda } = acscAngles(c);
  const entropy = Math.log(Math.abs(c.disc) + 1);
  const cohClass = (entropy * (c.rank + 1)) / Math.sqrt(Math.max(1, c.conductor));
  const logN = Math.log(Math.max(1, c.conductor));
  const nHat = logN / (1 + Math.log1p(c.conductor));
  const [a1, a2, a3, a4, a6] = c.ainvs;

  let theta = thA;
  let phi = phA;
  let rad = 0.55 + 0.75 * lambda;
  let extraZ = 0;

  if (family === "acsc") {
    extraZ = rankLift ? 0.85 * rho : 0;
  } else if (family === "rank-elev") {
    extraZ = 0.95 * c.rank;
  } else if (family === "mcj") {
    const aj = Math.abs(c.jinv);
    theta = Math.PI + Math.atan(c.jinv);
    phi = (Math.PI * Math.log1p(aj)) / (1 + Math.log1p(aj));
    rad = 0.5 + 0.7 * nHat;
    extraZ = rankLift ? 0.85 * rho : 0;
  } else if (family === "ptd") {
    theta = Math.atan2(a6, a4 + 0.01) + Math.PI;
    phi = Math.PI * (0.15 + 0.7 * ((a2 + 2) / 4));
    rad = 0.45 + 0.8 * nHat;
    extraZ = (rankLift ? 0.85 * rho : 0) + 0.08 * a1 + 0.06 * a3;
  } else {
    const ap = a1 * a1 + 4 * a2;
    const bp = a1 * a3 + 2 * a4;
    theta = (2 * Math.PI * ((Math.abs(c.disc) + Math.abs(ap)) % 97)) / 97;
    phi = Math.PI * (0.12 + 0.76 * ((Math.abs(bp) % 53) / 53));
    rad = 0.5 + 0.65 * nHat;
    extraZ = 0.12 * Math.tanh(a6) + (rankLift ? 0.85 * rho : 0);
  }

  const p = sphere(theta, phi, rad);
  return {
    ...c,
    x: p.x,
    y: p.y,
    z: p.z + extraZ,
    entropy,
    cohClass,
    theta,
    phi,
    rho,
    lambda,
    family,
  };
}

export function projectCatalog(
  curves: Curve[] = getCatalog(),
  family: MappingFamily = "acsc",
  rankLift = false,
): Projected[] {
  return curves.map((c) => projectCurve(c, family, rankLift));
}

export function kNearest(points: Projected[], k = 3): Array<[number, number]> {
  const links: Array<[number, number]> = [];
  const seen = new Set<string>();
  for (let i = 0; i < points.length; i++) {
    const a = points[i]!;
    const dist: Array<{ j: number; d: number }> = [];
    for (let j = 0; j < points.length; j++) {
      if (i === j) continue;
      const b = points[j]!;
      const d = (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2;
      dist.push({ j, d });
    }
    dist.sort((p, q) => p.d - q.d);
    for (let n = 0; n < k && n < dist.length; n++) {
      const j = dist[n]!.j;
      const key = i < j ? `${i}-${j}` : `${j}-${i}`;
      if (seen.has(key)) continue;
      seen.add(key);
      links.push([i, j]);
    }
  }
  return links;
}

type ProjectionKey = `${MappingFamily}:${ProvenanceFilter}:${"0" | "1"}`;

const projCache = new Map<ProjectionKey, { points: Projected[]; links: Array<[number, number]> }>();

export function getProjection(
  family: MappingFamily = "acsc",
  provenance: ProvenanceFilter = "all",
  rankLift = false,
) {
  const key: ProjectionKey = `${family}:${provenance}:${rankLift ? "1" : "0"}`;
  const hit = projCache.get(key);
  if (hit) return hit;
  let curves = getCatalog();
  if (provenance !== "all") curves = curves.filter((c) => c.provenance === provenance);
  const points = projectCatalog(curves, family, family === "rank-elev" ? true : rankLift);
  const out = { points, links: kNearest(points, 3) };
  projCache.set(key, out);
  return out;
}

export const PROJECTED = getProjection("acsc").points;
export const FILAMENTS = getProjection("acsc").links;

export function hLcdm(z: number, H0: number) {
  const zp = 1 + z;
  return H0 * Math.sqrt(OMEGA_M * zp * zp * zp + OMEGA_L);
}

/** Local-vs-global sampling weight w_E(z). Conjectural. */
export function curveWeight(c: Curve, z: number) {
  const t = 1 / (1 + z);
  const local = Math.exp(0.62 * c.rank) / (1 + 0.18 * Math.log(c.conductor));
  return (1 - t) * 1 + t * local;
}

export function meanOmega(curves: Curve[], z: number) {
  let num = 0;
  let den = 0;
  for (const c of curves) {
    const w = curveWeight(c, z);
    num += w * c.omega;
    den += w;
  }
  return den > 0 ? num / den : 1;
}

export function entropyCurvature(z: number) {
  return Math.exp(-z / 1.85);
}

export function metricTrace(z: number) {
  return 1 / Math.pow(1 + z, 0.72);
}

/**
 * H_eff(z) = H_ΛCDM(z; H0 · ⟨Ω⟩_z/⟨Ω⟩_∞) + β κ(z) + γ Tr(δg)(z)
 * Phenomenological S.T.A.R. expansion history. Calibrated so high-z recovers Planck.
 */
export function hEff(z: number, curves: Curve[], beta: number, gamma: number) {
  const omZ = meanOmega(curves, z);
  const omInf = meanOmega(curves, 1e5);
  const scale = Math.pow(omZ / Math.max(1e-9, omInf), 0.28);
  const H0 = H0_PLANCK * scale;
  return hLcdm(z, H0) + beta * entropyCurvature(z) * 5.15 + gamma * metricTrace(z) * 3.4;
}

export function sampleRedshifts(n = 48) {
  const zs: number[] = [];
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1);
    zs.push(Math.expm1(t * Math.log1p(Z_STAR)));
  }
  return zs;
}

/** Closed 2-form on T²: ω = dθ ∧ dφ, [ω] ≠ 0 in H²(T²). Established pullback. */
export function pullbackDensity(dY1dx: number, dY1dy: number, dY2dx: number, dY2dy: number) {
  return dY1dx * dY2dy - dY1dy * dY2dx;
}

export function topologicalCharge(Fq: number[][], cellArea: number) {
  let q = 0;
  for (let i = 0; i < Fq.length; i++) {
    const row = Fq[i]!;
    for (let j = 0; j < row.length; j++) q += row[j]!;
  }
  return q * cellArea;
}

export function localIq(Fxy: number) {
  return 0.25 * Fxy * Fxy;
}

export type RtchParams = {
  lambdaQ: number;
  alphaPhi: number;
  alphaA: number;
  betaQ: number;
  lambdaScale: number;
  topologyOn: boolean;
  conformalOn: boolean;
  freezeY: boolean;
  windingU: number;
  windingV: number;
  beta: number;
  gamma: number;
  pressure: number;
};

export const DEFAULT_RTCH: RtchParams = {
  lambdaQ: 1,
  alphaPhi: 0.22,
  alphaA: 0.12,
  betaQ: 0.35,
  lambdaScale: 1,
  topologyOn: true,
  conformalOn: true,
  freezeY: false,
  windingU: 1,
  windingV: 1,
  beta: 0.48,
  gamma: 0.22,
  pressure: 0,
};

/** α_Q = β_Q / Λ_Q^4  — Appendix B minimal falsifiable model. */
export function alphaQ(p: RtchParams) {
  if (!p.conformalOn) return 0;
  const L4 = Math.pow(Math.max(0.25, p.lambdaScale), 4);
  return p.betaQ / L4;
}

export function conformalA(phi: number, M: number, JQ: number, p: RtchParams) {
  if (!p.conformalOn) return 1;
  return Math.exp(p.alphaPhi * phi + p.alphaA * M + alphaQ(p) * JQ);
}

export function matterTrace(rho: number, pressure: number) {
  return -rho + 3 * pressure;
}

export type FieldSample = {
  q: number;
  iqMean: number;
  iqMax: number;
  hNorm: number;
  phiRms: number;
  sourceJ: number;
  aMean: number;
};

export type StatePoint = {
  Y1: number;
  Y2: number;
  Fxy: number;
  JQ: number;
  phi: number;
  M: number;
  A: number;
  lnA: number;
};

/** Thermodynamic map Φ: (x,y) → T² with optional local deformation. Established pullback. */
export function evaluateState(x: number, y: number, t: number, p: RtchParams): StatePoint {
  const jitter = p.freezeY ? 0 : 0.18;
  const Y1 = p.windingU * 2 * Math.PI * x + jitter * Math.sin(2 * Math.PI * (3 * x + t * 0.35) + y);
  const Y2 = p.windingV * 2 * Math.PI * y + jitter * Math.cos(2 * Math.PI * (2 * y - t * 0.28) + x);
  const eps = 1e-3;
  const Y1x = p.windingU * 2 * Math.PI + jitter * 2 * Math.PI * 3 * Math.cos(2 * Math.PI * (3 * x + t * 0.35) + y);
  const Y1y = jitter * Math.cos(2 * Math.PI * (3 * x + t * 0.35) + y);
  const Y2x = jitter * (-Math.sin(2 * Math.PI * (2 * y - t * 0.28) + x));
  const Y2y = p.windingV * 2 * Math.PI + jitter * 2 * Math.PI * 2 * (-Math.sin(2 * Math.PI * (2 * y - t * 0.28) + x));
  void eps;
  const Fxy = p.freezeY ? 0 : pullbackDensity(Y1x, Y1y, Y2x, Y2y);
  const JQ = localIq(Fxy);
  const phi = 0.25 * Math.sin(Y1) * Math.cos(Y2);
  const M = 0.4 + 0.2 * Math.sin(Y1 + Y2);
  const A = conformalA(phi, M, JQ, p);
  return { Y1, Y2, Fxy, JQ, phi, M, A, lnA: Math.log(Math.max(1e-9, A)) };
}

export function gradLnA(x: number, y: number, t: number, p: RtchParams) {
  const h = 0.008;
  const c = evaluateState(x, y, t, p).lnA;
  const dx = (evaluateState(Math.min(1 - h, x + h), y, t, p).lnA - c) / h;
  const dy = (evaluateState(x, Math.min(1 - h, y + h), t, p).lnA - c) / h;
  return { dx, dy, lnA: c };
}
