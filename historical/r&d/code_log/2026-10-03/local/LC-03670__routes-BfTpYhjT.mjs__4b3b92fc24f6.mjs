import { s as require_jsx_runtime } from "../_libs/@radix-ui/react-collection+[...].mjs";
import { c as catalogStats, d as hEff, g as useLab, i as H0_SHOES, n as FILAMENTS, o as PROJECTED, r as H0_PLANCK, u as getCatalog } from "./store-BJHkQxaW.mjs";
import { v as Link } from "../_libs/@tanstack/react-router+[...].mjs";
import { l as ArrowUpRight } from "../_libs/lucide-react.mjs";
import { i as Sym, n as Formula, r as Metric, t as Badge } from "./formula-vgr3i3sJ.mjs";
import { t as OrbitCloud } from "./orbit-cloud-CutwTzrs.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/routes-BfTpYhjT.js
var import_jsx_runtime = require_jsx_runtime();
var CHAPTERS = [
	{
		to: "/projection",
		kicker: "ACSC",
		title: "Arithmetic projection",
		body: "Elliptic-curve invariants (rank, conductor, regulator, real period) map through Φ onto a cosmological manifold."
	},
	{
		to: "/cohomology",
		kicker: "ECC / RTCH",
		title: "Entropy cohomology",
		body: "A closed target 2-form ω pulls back to F_Q. The charge Q_RTCH is global; the scalar I_Q is not."
	},
	{
		to: "/hubble",
		kicker: "S.T.A.R.",
		title: "Scale-dependent Hubble",
		body: "Local sampling of ⟨Ω_E⟩_z and entropy curvature lift H_eff at low z without touching the CMB."
	}
];
function Home() {
	const beta = useLab((s) => s.beta);
	const gamma = useLab((s) => s.gamma);
	const stats = catalogStats();
	const Hnow = hEff(0, getCatalog(), beta, gamma);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-12",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "grid gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-end",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Badge, {
						tone: "steel",
						children: "Observatory"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
						className: "mt-4 font-display text-4xl leading-[1.05] tracking-tight text-fg sm:text-5xl lg:text-6xl",
						children: "The universe, projected from arithmetic."
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-5 max-w-xl text-base leading-relaxed text-muted",
						children: "STARMAP is a working laboratory for the S.T.A.R. Program — Symbolic–Topological–Arithmetic Relativity — and the fully variational RTCH master action. Drag the manifold. Open a lab."
					})
				] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "grid grid-cols-2 gap-6 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
							label: "H_eff(0)",
							value: Hnow.toFixed(2),
							unit: "km/s/Mpc",
							hint: `SH0ES ${H0_SHOES.toFixed(2)}`
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
							label: "Planck H0",
							value: H0_PLANCK.toFixed(1),
							unit: "km/s/Mpc",
							hint: "CMB anchor"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
							label: "Curves",
							value: String(stats.n),
							hint: `rank 0–4 · ${stats.ranks[1]} of rank 1`
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
							label: "⟨Ω_E⟩",
							value: stats.meanOmega.toFixed(3),
							hint: "catalog mean period"
						})
					]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex items-center justify-between px-5 py-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: "Φ(E) · arithmetic point cloud"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "font-mono text-[10px] text-muted",
						children: "Drag to orbit · click a curve"
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(OrbitCloud, {
					points: PROJECTED,
					links: FILAMENTS,
					className: "h-[min(62vh,540px)] w-full"
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("section", {
				className: "grid gap-4 md:grid-cols-3",
				children: CHAPTERS.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Link, {
					to: c.to,
					className: "group rounded-xl bg-surface p-5 shadow-[var(--shadow-border)] transition-[box-shadow] duration-150 hover:shadow-[var(--shadow-border-hover)]",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "flex items-center justify-between",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "font-mono text-[10px] uppercase tracking-[0.16em] text-steel",
								children: c.kicker
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowUpRight, { className: "size-4 text-subtle transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" })]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
							className: "mt-3 font-display text-2xl tracking-tight",
							children: c.title
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-2 text-sm leading-relaxed text-muted",
							children: c.body
						})
					]
				}, c.to))
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "grid gap-8 lg:grid-cols-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
						className: "font-display text-2xl tracking-tight",
						children: "Effective expansion"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-3 text-sm leading-relaxed text-muted",
						children: "The S.T.A.R. prediction is a scale-dependent Hubble parameter sourced by the weighted real period of curves visible at redshift z, plus entropy-curvature and metric-trace corrections that vanish at last scatter."
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-5",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Formula, {
							boxed: true,
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Sym, { children: "H" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", {
									className: "font-sans text-sm not-italic",
									children: "eff"
								}),
								"(z) = H",
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", {
									className: "font-sans text-sm not-italic",
									children: "0"
								}),
								" · ⟨Ω",
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "E" }),
								"⟩",
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "z" })
							]
						})
					})
				] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
						className: "font-display text-2xl tracking-tight",
						children: "Topological charge"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-3 text-sm leading-relaxed text-muted",
						children: "RTCH does not identify entropy with a local scalar. The observable pairing is cohomological: a closed target form pulled back along the thermodynamic map, integrated on a two-cycle."
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-5",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Formula, {
							boxed: true,
							children: [
								"Q",
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", {
									className: "font-sans text-sm not-italic",
									children: "RTCH"
								}),
								"[Σ",
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "2" }),
								"] = ∫",
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "Σ₂" }),
								" Φ",
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sup", { children: "*" }),
								"ω"
							]
						})
					})
				] })]
			})
		]
	});
}
//#endregion
export { Home as component };
