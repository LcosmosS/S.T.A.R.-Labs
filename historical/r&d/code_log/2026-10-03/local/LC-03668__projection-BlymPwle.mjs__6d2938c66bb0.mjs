import { s as require_jsx_runtime } from "../_libs/@radix-ui/react-collection+[...].mjs";
import { g as useLab, n as FILAMENTS, o as PROJECTED, u as getCatalog } from "./store-BJHkQxaW.mjs";
import { i as Sym, n as Formula, r as Metric, t as Badge } from "./formula-vgr3i3sJ.mjs";
import { t as OrbitCloud } from "./orbit-cloud-CutwTzrs.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/projection-BlymPwle.js
var import_jsx_runtime = require_jsx_runtime();
function ProjectionPage() {
	const selectedLabel = useLab((s) => s.selectedLabel);
	const set = useLab((s) => s.set);
	const curve = PROJECTED.find((c) => c.label === selectedLabel) ?? PROJECTED[0];
	const catalog = getCatalog();
	const ranks = [
		0,
		1,
		2,
		3,
		4
	].map((r) => catalog.filter((c) => c.rank === r).length);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-8",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
				className: "max-w-2xl",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Badge, {
						tone: "steel",
						children: "ACSC"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
						className: "mt-3 font-display text-4xl tracking-tight",
						children: "Arithmetic–cosmic projection"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-3 text-sm leading-relaxed text-muted",
						children: "The Arithmetic–Cosmic Structure Conjecture maps elliptic-curve invariants into a cosmological manifold. Rank, log-conductor and regulator become coordinates; sinusoidal and oblate corrections implement the global-to-local mapping paradox."
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Formula, {
				boxed: true,
				children: [
					"Φ(E): (",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Sym, { children: "r" }),
					", log ",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Sym, { children: "N" }),
					", Reg) → (",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Sym, { children: "x" }),
					", ",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Sym, { children: "y" }),
					", ",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Sym, { children: "z" }),
					")"
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-6 lg:grid-cols-[1.4fr_0.8fr]",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(OrbitCloud, {
						points: PROJECTED,
						links: FILAMENTS,
						selected: curve.label,
						onSelect: (label) => set({ selectedLabel: label }),
						autoRotate: false,
						className: "h-[min(56vh,520px)] w-full"
					})
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("aside", {
					className: "space-y-5 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
							children: "Selected curve"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "font-display text-3xl tracking-tight",
							children: curve.label
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "grid grid-cols-2 gap-4",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
									label: "Conductor N",
									value: curve.conductor.toLocaleString()
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
									label: "Rank r",
									value: String(curve.rank)
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
									label: "Regulator",
									value: curve.regulator.toFixed(4)
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
									label: "Real period Ω",
									value: curve.omega.toFixed(4)
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
									label: "Discriminant Δ",
									value: curve.disc.toExponential(2)
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
									label: "Torsion",
									value: curve.torsion
								})
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "font-mono text-xs text-muted",
							children: [
								"a-invariants [",
								curve.ainvs.join(", "),
								"]"
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "font-mono text-xs text-muted",
							children: ["Isogeny class ", curve.isogeny]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "grid grid-cols-2 gap-4 pt-2",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
								label: "Entropy log|Δ|",
								value: curve.entropy.toFixed(2)
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
								label: "Coh. class",
								value: curve.cohClass.toExponential(2)
							})]
						})
					]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "font-display text-2xl tracking-tight",
					children: "Rank spectrum"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mt-2 max-w-2xl text-sm text-muted",
					children: "Higher rank is locally over-sampled at low redshift in the Hubble lab, matching the S.T.A.R. claim that structure-rich patches of Φ(E) drive the late-time H_eff enhancement."
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mt-5 grid grid-cols-5 gap-3",
					children: ranks.map((n, r) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "rounded-lg bg-surface p-4 shadow-[var(--shadow-border)]",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
								children: ["Rank ", r]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mt-2 font-mono text-2xl tabular-nums",
								children: n
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mt-3 h-1.5 overflow-hidden rounded-full bg-elevated",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
									className: "h-full bg-primary",
									style: { width: `${n / catalog.length * 100}%` }
								})
							})
						]
					}, r))
				})
			] })
		]
	});
}
//#endregion
export { ProjectionPage as component };
