import { hash32, mulberry32 } from "./rng";

export type Curve = {
  label: string;
  conductor: number;
  rank: number;
  regulator: number;
  omega: number;
  disc: number;
  ainvs: [number, number, number, number, number];
  torsion: string;
  isogeny: string;
};

export type Cluster = {
  name: string;
  rMly: number;
  rank: number;
  conductor: number;
  hFactor: number;
  entropy: number;
  cohClass: number;
  volume: number;
  derivedA: number;
};

/** Illustrative LMFDB/Cremona-style catalog for the ACSC projection. */
const FAMOUS: Curve[] = [
  { label: "11.a3", conductor: 11, rank: 0, regulator: 1, omega: 6.34605, disc: -11, ainvs: [0, -1, 1, 0, 0], torsion: "Z/5", isogeny: "11.a" },
  { label: "11.a2", conductor: 11, rank: 0, regulator: 1, omega: 1.26921, disc: -161051, ainvs: [0, -1, 1, -10, -20], torsion: "Z/5", isogeny: "11.a" },
  { label: "11.a1", conductor: 11, rank: 0, regulator: 1, omega: 0.25384, disc: 11, ainvs: [0, -1, 1, -7820, -263580], torsion: "Z/5", isogeny: "11.a" },
  { label: "37.a1", conductor: 37, rank: 1, regulator: 0.05111, omega: 5.98692, disc: -37, ainvs: [0, 0, 1, -1, 0], torsion: "1", isogeny: "37.a" },
  { label: "43.a1", conductor: 43, rank: 1, regulator: 0.03248, omega: 5.47113, disc: -43, ainvs: [0, 1, 1, 0, 0], torsion: "1", isogeny: "43.a" },
  { label: "53.a1", conductor: 53, rank: 1, regulator: 0.14298, omega: 4.87201, disc: -53, ainvs: [1, -1, 1, 0, 0], torsion: "1", isogeny: "53.a" },
  { label: "61.a1", conductor: 61, rank: 1, regulator: 0.04865, omega: 4.9812, disc: -61, ainvs: [1, 0, 0, -2, 1], torsion: "1", isogeny: "61.a" },
  { label: "89.a1", conductor: 89, rank: 1, regulator: 0.1723, omega: 4.2104, disc: -89, ainvs: [1, 1, 0, -2, 0], torsion: "1", isogeny: "89.a" },
  { label: "389.a1", conductor: 389, rank: 2, regulator: 0.15246, omega: 2.49014, disc: -389, ainvs: [0, 1, 1, -2, 0], torsion: "1", isogeny: "389.a" },
  { label: "433.a1", conductor: 433, rank: 2, regulator: 0.2341, omega: 2.3188, disc: -433, ainvs: [1, -1, 0, -3, 2], torsion: "1", isogeny: "433.a" },
  { label: "5077.a1", conductor: 5077, rank: 3, regulator: 0.4172, omega: 1.1024, disc: -5077, ainvs: [0, 0, 1, -7, 6], torsion: "1", isogeny: "5077.a" },
  { label: "234446.a1", conductor: 234446, rank: 4, regulator: 1.528, omega: 0.4122, disc: -234446, ainvs: [1, 0, 1, -36, -70], torsion: "1", isogeny: "234446.a" },
];

function syntheticCurve(i: number, rng: () => number): Curve {
  const roll = rng();
  const rank = roll < 0.38 ? 0 : roll < 0.86 ? 1 : roll < 0.97 ? 2 : roll < 0.995 ? 3 : 4;
  const conductor = Math.round(14 + rng() * rng() * 180000);
  const letter = String.fromCharCode(97 + Math.floor(rng() * 6));
  const label = `${conductor}.${letter}1`;
  const regulator = rank === 0 ? 1 : Math.exp(0.35 * rank * rng()) * rank * (0.04 + 0.18 * rng()) * Math.log(conductor + 3);
  const omega = (6.8 / Math.pow(conductor, 0.22)) * (0.55 + 0.9 * rng()) / (1 + 0.18 * rank);
  const sign = rng() < 0.55 ? -1 : 1;
  const disc = sign * Math.round(conductor * (1 + rng() * 40) * Math.pow(10, Math.floor(rng() * 3)));
  const torsionPool = ["1", "Z/2", "Z/2×Z/2", "Z/4", "Z/3", "Z/5", "Z/6"];
  return {
    label,
    conductor,
    rank,
    regulator: Number(regulator.toFixed(5)),
    omega: Number(omega.toFixed(5)),
    disc,
    ainvs: [
      Math.floor(rng() * 3) - 1,
      Math.floor(rng() * 5) - 2,
      Math.floor(rng() * 2),
      Math.floor(rng() * 21) - 10,
      Math.floor(rng() * 41) - 20,
    ],
    torsion: torsionPool[Math.floor(rng() * torsionPool.length)] ?? "1",
    isogeny: `${conductor}.${letter}`,
  };
}

let cached: Curve[] | null = null;

export function getCatalog(): Curve[] {
  if (cached) return cached;
  const rng = mulberry32(0x53544152);
  const extra: Curve[] = [];
  const used = new Set(FAMOUS.map((c) => c.label));
  let i = 0;
  while (extra.length < 148) {
    const c = syntheticCurve(i++, rng);
    if (used.has(c.label)) continue;
    used.add(c.label);
    extra.push(c);
  }
  cached = [...FAMOUS, ...extra].sort((a, b) => a.conductor - b.conductor || a.label.localeCompare(b.label));
  return cached;
}

export const CLUSTERS: Cluster[] = [
  { name: "Virgo", rMly: 54, rank: 2, conductor: 1.82e10, hFactor: 1.0174, entropy: 35.15, cohClass: 12.63, volume: 3.235e8, derivedA: -1706 },
  { name: "Perseus", rMly: 236, rank: 1, conductor: 2.56e10, hFactor: 1.0237, entropy: 39.31, cohClass: 4.8, volume: 1.313e9, derivedA: -7456 },
  { name: "Coma", rMly: 321, rank: 0, conductor: 4.1e12, hFactor: 1.0251, entropy: 39.64, cohClass: 2.1, volume: 5.12e7, derivedA: -10141 },
  { name: "Hercules", rMly: 500, rank: 1, conductor: 8.4e11, hFactor: 1.027, entropy: 40.12, cohClass: 3.41, volume: 2.08e8, derivedA: -15796 },
  { name: "Shapley", rMly: 650, rank: 1, conductor: 1.1e12, hFactor: 1.0281, entropy: 40.55, cohClass: 3.02, volume: 4.41e8, derivedA: -20535 },
];

export const KAPPA_UCF = 31.5926;

export function catalogStats(curves: Curve[] = getCatalog()) {
  const n = curves.length;
  const ranks = [0, 0, 0, 0, 0];
  let om = 0;
  let ent = 0;
  for (const c of curves) {
    ranks[Math.min(c.rank, 4)] += 1;
    om += c.omega;
    ent += Math.log(Math.abs(c.disc) + 1);
  }
  return {
    n,
    ranks,
    meanOmega: om / n,
    meanEntropy: ent / n,
    maxConductor: curves[curves.length - 1]?.conductor ?? 0,
  };
}

export function curveHue(rank: number) {
  const t = Math.min(rank, 4) / 4;
  return 210 - t * 18;
}

export function idColor(label: string) {
  return hash32(label);
}
