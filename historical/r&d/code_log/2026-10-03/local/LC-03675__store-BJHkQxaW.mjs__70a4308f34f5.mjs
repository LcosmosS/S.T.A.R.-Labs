import { n as clsx } from "../_libs/class-variance-authority+clsx.mjs";
import { t as twMerge } from "../_libs/tailwind-merge.mjs";
import { t as create } from "../_libs/zustand.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/store-BJHkQxaW.js
function cn(...inputs) {
	return twMerge(clsx(inputs));
}
function mulberry32(seed) {
	let a = seed >>> 0;
	return function next() {
		a += 1831565813;
		let t = a;
		t = Math.imul(t ^ t >>> 15, t | 1);
		t ^= t + Math.imul(t ^ t >>> 7, t | 61);
		return ((t ^ t >>> 14) >>> 0) / 4294967296;
	};
}
function hash32(s) {
	let h = 2166136261;
	for (let i = 0; i < s.length; i++) {
		h ^= s.charCodeAt(i);
		h = Math.imul(h, 16777619);
	}
	return h >>> 0;
}
/** Illustrative LMFDB/Cremona-style catalog for the ACSC projection. */
var FAMOUS = [
	{
		label: "11.a3",
		conductor: 11,
		rank: 0,
		regulator: 1,
		omega: 6.34605,
		disc: -11,
		ainvs: [
			0,
			-1,
			1,
			0,
			0
		],
		torsion: "Z/5",
		isogeny: "11.a"
	},
	{
		label: "11.a2",
		conductor: 11,
		rank: 0,
		regulator: 1,
		omega: 1.26921,
		disc: -161051,
		ainvs: [
			0,
			-1,
			1,
			-10,
			-20
		],
		torsion: "Z/5",
		isogeny: "11.a"
	},
	{
		label: "11.a1",
		conductor: 11,
		rank: 0,
		regulator: 1,
		omega: .25384,
		disc: 11,
		ainvs: [
			0,
			-1,
			1,
			-7820,
			-263580
		],
		torsion: "Z/5",
		isogeny: "11.a"
	},
	{
		label: "37.a1",
		conductor: 37,
		rank: 1,
		regulator: .05111,
		omega: 5.98692,
		disc: -37,
		ainvs: [
			0,
			0,
			1,
			-1,
			0
		],
		torsion: "1",
		isogeny: "37.a"
	},
	{
		label: "43.a1",
		conductor: 43,
		rank: 1,
		regulator: .03248,
		omega: 5.47113,
		disc: -43,
		ainvs: [
			0,
			1,
			1,
			0,
			0
		],
		torsion: "1",
		isogeny: "43.a"
	},
	{
		label: "53.a1",
		conductor: 53,
		rank: 1,
		regulator: .14298,
		omega: 4.87201,
		disc: -53,
		ainvs: [
			1,
			-1,
			1,
			0,
			0
		],
		torsion: "1",
		isogeny: "53.a"
	},
	{
		label: "61.a1",
		conductor: 61,
		rank: 1,
		regulator: .04865,
		omega: 4.9812,
		disc: -61,
		ainvs: [
			1,
			0,
			0,
			-2,
			1
		],
		torsion: "1",
		isogeny: "61.a"
	},
	{
		label: "89.a1",
		conductor: 89,
		rank: 1,
		regulator: .1723,
		omega: 4.2104,
		disc: -89,
		ainvs: [
			1,
			1,
			0,
			-2,
			0
		],
		torsion: "1",
		isogeny: "89.a"
	},
	{
		label: "389.a1",
		conductor: 389,
		rank: 2,
		regulator: .15246,
		omega: 2.49014,
		disc: -389,
		ainvs: [
			0,
			1,
			1,
			-2,
			0
		],
		torsion: "1",
		isogeny: "389.a"
	},
	{
		label: "433.a1",
		conductor: 433,
		rank: 2,
		regulator: .2341,
		omega: 2.3188,
		disc: -433,
		ainvs: [
			1,
			-1,
			0,
			-3,
			2
		],
		torsion: "1",
		isogeny: "433.a"
	},
	{
		label: "5077.a1",
		conductor: 5077,
		rank: 3,
		regulator: .4172,
		omega: 1.1024,
		disc: -5077,
		ainvs: [
			0,
			0,
			1,
			-7,
			6
		],
		torsion: "1",
		isogeny: "5077.a"
	},
	{
		label: "234446.a1",
		conductor: 234446,
		rank: 4,
		regulator: 1.528,
		omega: .4122,
		disc: -234446,
		ainvs: [
			1,
			0,
			1,
			-36,
			-70
		],
		torsion: "1",
		isogeny: "234446.a"
	}
];
function syntheticCurve(i, rng) {
	const roll = rng();
	const rank = roll < .38 ? 0 : roll < .86 ? 1 : roll < .97 ? 2 : roll < .995 ? 3 : 4;
	const conductor = Math.round(14 + rng() * rng() * 18e4);
	const letter = String.fromCharCode(97 + Math.floor(rng() * 6));
	const label = `${conductor}.${letter}1`;
	const regulator = rank === 0 ? 1 : Math.exp(.35 * rank * rng()) * rank * (.04 + .18 * rng()) * Math.log(conductor + 3);
	const omega = 6.8 / Math.pow(conductor, .22) * (.55 + .9 * rng()) / (1 + .18 * rank);
	const disc = (rng() < .55 ? -1 : 1) * Math.round(conductor * (1 + rng() * 40) * Math.pow(10, Math.floor(rng() * 3)));
	const torsionPool = [
		"1",
		"Z/2",
		"Z/2×Z/2",
		"Z/4",
		"Z/3",
		"Z/5",
		"Z/6"
	];
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
			Math.floor(rng() * 41) - 20
		],
		torsion: torsionPool[Math.floor(rng() * torsionPool.length)] ?? "1",
		isogeny: `${conductor}.${letter}`
	};
}
var cached = null;
function getCatalog() {
	if (cached) return cached;
	const rng = mulberry32(1398030674);
	const extra = [];
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
var CLUSTERS = [
	{
		name: "Virgo",
		rMly: 54,
		rank: 2,
		conductor: 182e8,
		hFactor: 1.0174,
		entropy: 35.15,
		cohClass: 12.63,
		volume: 3235e5,
		derivedA: -1706
	},
	{
		name: "Perseus",
		rMly: 236,
		rank: 1,
		conductor: 256e8,
		hFactor: 1.0237,
		entropy: 39.31,
		cohClass: 4.8,
		volume: 1313e6,
		derivedA: -7456
	},
	{
		name: "Coma",
		rMly: 321,
		rank: 0,
		conductor: 41e11,
		hFactor: 1.0251,
		entropy: 39.64,
		cohClass: 2.1,
		volume: 512e5,
		derivedA: -10141
	},
	{
		name: "Hercules",
		rMly: 500,
		rank: 1,
		conductor: 84e10,
		hFactor: 1.027,
		entropy: 40.12,
		cohClass: 3.41,
		volume: 208e6,
		derivedA: -15796
	},
	{
		name: "Shapley",
		rMly: 650,
		rank: 1,
		conductor: 11e11,
		hFactor: 1.0281,
		entropy: 40.55,
		cohClass: 3.02,
		volume: 441e6,
		derivedA: -20535
	}
];
var KAPPA_UCF = 31.5926;
function catalogStats(curves = getCatalog()) {
	const n = curves.length;
	const ranks = [
		0,
		0,
		0,
		0,
		0
	];
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
		maxConductor: curves[curves.length - 1]?.conductor ?? 0
	};
}
var H0_PLANCK = 67.4;
var H0_SHOES = 73.04;
var OMEGA_M = .315;
var OMEGA_L = .685;
var Z_STAR = 1100;
function hashUnit(s, salt) {
	return hash32(s + ":" + salt) / 4294967296;
}
/** ACSC projection Φ(E): (r, log N, Reg) → (x,y,z) with paradox corrections. */
function projectCurve(c, bounds) {
	const v = (Math.log(c.conductor) - bounds.lnMin) / Math.max(1e-6, bounds.lnMax - bounds.lnMin);
	const theta = hashUnit(c.label, "th") * Math.PI * 2;
	const phi = (.18 + hashUnit(c.label, "ph") * .82) * Math.PI;
	const w = Math.tanh(Math.log1p(c.regulator));
	const rad = (1 + .12 * Math.sin(3 * theta) + .08 * Math.cos(2 * phi)) * (.35 + .95 * v + .08 * c.rank);
	const obl = .86;
	return {
		...c,
		x: rad * Math.sin(phi) * Math.cos(theta),
		y: obl * rad * Math.sin(phi) * Math.sin(theta) + .16 * c.rank,
		z: rad * Math.cos(phi) + .1 * w,
		entropy: Math.log(Math.abs(c.disc) + 1),
		cohClass: Math.log(Math.abs(c.disc) + 1) * (c.rank + 1) / Math.sqrt(Math.max(1, c.conductor)),
		theta,
		phi
	};
}
function projectCatalog(curves = getCatalog()) {
	let lnMin = Infinity;
	let lnMax = -Infinity;
	for (const c of curves) {
		const l = Math.log(c.conductor);
		if (l < lnMin) lnMin = l;
		if (l > lnMax) lnMax = l;
	}
	return curves.map((c) => projectCurve(c, {
		lnMin,
		lnMax
	}));
}
function kNearest(points, k = 3) {
	const links = [];
	const seen = /* @__PURE__ */ new Set();
	for (let i = 0; i < points.length; i++) {
		const a = points[i];
		const dist = [];
		for (let j = 0; j < points.length; j++) {
			if (i === j) continue;
			const b = points[j];
			const d = (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2;
			dist.push({
				j,
				d
			});
		}
		dist.sort((p, q) => p.d - q.d);
		for (let n = 0; n < k && n < dist.length; n++) {
			const j = dist[n].j;
			const key = i < j ? `${i}-${j}` : `${j}-${i}`;
			if (seen.has(key)) continue;
			seen.add(key);
			links.push([i, j]);
		}
	}
	return links;
}
var PROJECTED = projectCatalog();
var FILAMENTS = kNearest(PROJECTED, 3);
function hLcdm(z, H0) {
	const zp = 1 + z;
	return H0 * Math.sqrt(OMEGA_M * zp * zp * zp + OMEGA_L);
}
/** Local-vs-global sampling weight w_E(z). */
function curveWeight(c, z) {
	const t = 1 / (1 + z);
	const local = Math.exp(.62 * c.rank) / (1 + .18 * Math.log(c.conductor));
	return (1 - t) * 1 + t * local;
}
function meanOmega(curves, z) {
	let num = 0;
	let den = 0;
	for (const c of curves) {
		const w = curveWeight(c, z);
		num += w * c.omega;
		den += w;
	}
	return den > 0 ? num / den : 1;
}
function entropyCurvature(z) {
	return Math.exp(-z / 1.85);
}
function metricTrace(z) {
	return 1 / Math.pow(1 + z, .72);
}
/**
* H_eff(z) = H_ΛCDM(z; H0 · ⟨Ω⟩_z/⟨Ω⟩_∞) + β κ(z) + γ Tr(δg)(z)
* Calibrated so high-z recovers Planck and low-z approaches SH0ES.
*/
function hEff(z, curves, beta, gamma) {
	const omZ = meanOmega(curves, z);
	const omInf = meanOmega(curves, 1e5);
	return hLcdm(z, H0_PLANCK * Math.pow(omZ / Math.max(1e-9, omInf), .28)) + beta * entropyCurvature(z) * 5.15 + gamma * metricTrace(z) * 3.4;
}
/** Closed 2-form on T²: ω = dθ ∧ dφ, [ω] ≠ 0 in H²(T²). */
function pullbackDensity(dY1dx, dY1dy, dY2dx, dY2dy) {
	return dY1dx * dY2dy - dY1dy * dY2dx;
}
function localIq(Fxy) {
	return .25 * Fxy * Fxy;
}
var DEFAULT_RTCH = {
	lambdaQ: 1,
	alphaPhi: .22,
	alphaA: .12,
	topologyOn: true,
	conformalOn: true,
	freezeY: false,
	windingU: 1,
	windingV: 1,
	beta: .48,
	gamma: .22
};
var LIMITS = {
	minimal: DEFAULT_RTCH,
	"no-topology": {
		topologyOn: true,
		lambdaQ: 0
	},
	"no-conformal": {
		conformalOn: false,
		alphaPhi: 0,
		alphaA: 0
	},
	gr: {
		topologyOn: false,
		conformalOn: false,
		lambdaQ: 0,
		alphaPhi: 0,
		alphaA: 0,
		freezeY: false
	},
	"frozen-y": { freezeY: true }
};
var useLab = create()((set) => ({
	...DEFAULT_RTCH,
	z: 0,
	selectedLabel: "37.a1",
	set: (p) => set(p),
	applyLimit: (id) => set({
		...DEFAULT_RTCH,
		...LIMITS[id]
	}),
	reset: () => set({
		...DEFAULT_RTCH,
		z: 0
	})
}));
//#endregion
export { KAPPA_UCF as a, catalogStats as c, hEff as d, hLcdm as f, useLab as g, pullbackDensity as h, H0_SHOES as i, cn as l, meanOmega as m, FILAMENTS as n, PROJECTED as o, localIq as p, H0_PLANCK as r, Z_STAR as s, CLUSTERS as t, getCatalog as u };
