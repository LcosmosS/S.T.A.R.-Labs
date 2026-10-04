import { type Curve, getCatalog } from "./catalog";
import { hash32 } from "./rng";

export const H0_PLANCK = 67.4;
export const H0_SHOES = 73.04;
export const OMEGA_M = 0.315;
export const OMEGA_L = 0.685;
export const Z_STAR = 1100;

export type Vec3 = { x: number; y: number; z: number };

export type Projected = Curve & {
  x: number;
  y: number;
  z: number;
  entropy: number;
  cohClass: number;
  theta: number;
  phi: number;
};

function hashUnit(s: string, salt: string) {
  return hash32(s + ":" + salt) / 4294967296;
}

/** ACSC projection Φ(E): (r, log N, Reg) → (x,y,z) with paradox corrections. */
export function projectCurve(c: Curve, bounds: { lnMin: number; lnMax: number }): Projected {
  const lnN = Math.log(c.conductor);
  const v = (lnN - bounds.lnMin) / Math.max(1e-6, bounds.lnMax - bounds.lnMin);
  const theta = hashUnit(c.label, "th") * Math.PI * 2;
  const phi = (0.18 + hashUnit(c.label, "ph") * 0.82) * Math.PI;
  const w = Math.tanh(Math.log1p(c.regulator));
  const s = 1 + 0.12 * Math.sin(3 * theta) + 0.08 * Math.cos(2 * phi);
  const rad = s * (0.35 + 0.95 * v + 0.08 * c.rank);
  const obl = 0.86;
  return {
    ...c,
    x: rad * Math.sin(phi) * Math.cos(theta),
    y: obl * rad * Math.sin(phi) * Math.sin(theta) + 0.16 * c.rank,
    z: rad * Math.cos(phi) + 0.1 * w,
    entropy: Math.log(Math.abs(c.disc) + 1),
    cohClass: (Math.log(Math.abs(c.disc) + 1) * (c.rank + 1)) / Math.sqrt(Math.max(1, c.conductor)),
    theta,
    phi,
  };
}

export function projectCatalog(curves: Curve[] = getCatalog()): Projected[] {
  let lnMin = Infinity;
  let lnMax = -Infinity;
  for (const c of curves) {
    const l = Math.log(c.conductor);
    if (l < lnMin) lnMin = l;
    if (l > lnMax) lnMax = l;
  }
  return curves.map((c) => projectCurve(c, { lnMin, lnMax }));
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

export const PROJECTED = projectCatalog();
export const FILAMENTS = kNearest(PROJECTED, 3);

export function hLcdm(z: number, H0: number) {
  const zp = 1 + z;
  return H0 * Math.sqrt(OMEGA_M * zp * zp * zp + OMEGA_L);
}

/** Local-vs-global sampling weight w_E(z). */
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
 * Calibrated so high-z recovers Planck and low-z approaches SH0ES.
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

/** Closed 2-form on T²: ω = dθ ∧ dφ, [ω] ≠ 0 in H²(T²). */
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
  topologyOn: boolean;
  conformalOn: boolean;
  freezeY: boolean;
  windingU: number;
  windingV: number;
  beta: number;
  gamma: number;
};

export const DEFAULT_RTCH: RtchParams = {
  lambdaQ: 1,
  alphaPhi: 0.22,
  alphaA: 0.12,
  topologyOn: true,
  conformalOn: true,
  freezeY: false,
  windingU: 1,
  windingV: 1,
  beta: 0.48,
  gamma: 0.22,
};

export function conformalA(phi: number, M: number, p: RtchParams) {
  if (!p.conformalOn) return 1;
  return Math.exp(p.alphaPhi * phi + p.alphaA * M);
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


