import { i as __toESM } from "../_runtime.mjs";
import { c as require_react, s as require_jsx_runtime } from "../_libs/@radix-ui/react-collection+[...].mjs";
import { a as KAPPA_UCF, d as hEff, f as hLcdm, g as useLab, i as H0_SHOES, m as meanOmega, r as H0_PLANCK, s as Z_STAR, t as CLUSTERS, u as getCatalog } from "./store-BJHkQxaW.mjs";
import { i as Sym, n as Formula, r as Metric, t as Badge } from "./formula-vgr3i3sJ.mjs";
import { t as Slider } from "./slider-XbJnmBY9.mjs";
import { a as CartesianGrid, i as Line, n as YAxis, o as ResponsiveContainer, r as XAxis, s as Tooltip, t as LineChart } from "../_libs/recharts+[...].mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/hubble-3TPmuDbO.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function inferredH0(zz, curves, beta, gamma) {
	const E = hLcdm(zz, 1);
	return hEff(zz, curves, beta, gamma) / E;
}
function HubblePage() {
	const z = useLab((s) => s.z);
	const beta = useLab((s) => s.beta);
	const gamma = useLab((s) => s.gamma);
	const set = useLab((s) => s.set);
	const curves = getCatalog();
	const zPlot = Math.min(z, 2.4);
	const series = (0, import_react.useMemo)(() => {
		const rows = [];
		for (let i = 0; i <= 48; i++) {
			const zz = i / 48 * 2.4;
			rows.push({
				z: Number(zz.toFixed(3)),
				star: Number(inferredH0(zz, curves, beta, gamma).toFixed(3)),
				planck: H0_PLANCK,
				shoes: H0_SHOES
			});
		}
		return rows;
	}, [
		beta,
		gamma,
		curves
	]);
	const H = inferredH0(zPlot, curves, beta, gamma);
	const om = meanOmega(curves, zPlot);
	const omInf = meanOmega(curves, 1e5);
	const delta = inferredH0(0, curves, beta, gamma) - inferredH0(Z_STAR, curves, beta, gamma);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-8",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
				className: "max-w-2xl",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Badge, {
						tone: "warn",
						children: "Hubble–Planck tension"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
						className: "mt-3 font-display text-4xl tracking-tight",
						children: "Scale-dependent expansion"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-3 text-sm leading-relaxed text-muted",
						children: "Local distance-ladder measurements sample a biased subset of Φ(E); the CMB averages the global catalog. Entropy curvature κ(z) and Tr(δg)(z) add a late-time correction that vanishes at last scatter. The chart shows the inferred H0(z) ≡ H_eff(z) / E_ΛCDM(z)."
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Formula, {
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
						children: "ΛCDM"
					}),
					"(z; H",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "0" }),
					"⟨Ω⟩) + β κ(z) + γ Tr(δg)"
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "H0_eff(z)",
						value: H.toFixed(2),
						unit: "km/s/Mpc"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "SH0ES",
						value: H0_SHOES.toFixed(2),
						unit: "km/s/Mpc"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "Planck",
						value: H0_PLANCK.toFixed(1),
						unit: "km/s/Mpc"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "ΔH0 (local − CMB)",
						value: delta.toFixed(2),
						unit: "km/s/Mpc"
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mb-4 flex flex-wrap items-end justify-between gap-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: "Inferred H0(z) · km/s/Mpc"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex gap-4 font-mono text-[10px] uppercase tracking-[0.12em] text-muted",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-fg",
								children: "STAR"
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Planck" }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "SH0ES" })
						]
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "h-[280px] w-full sm:h-[340px]",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ResponsiveContainer, {
						width: "100%",
						height: "100%",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(LineChart, {
							data: series,
							margin: {
								top: 8,
								right: 8,
								left: 0,
								bottom: 0
							},
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CartesianGrid, { stroke: "rgba(255,255,255,0.06)" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(XAxis, {
									dataKey: "z",
									type: "number",
									domain: [0, 2.4],
									tick: {
										fill: "var(--color-muted)",
										fontSize: 11,
										fontFamily: "IBM Plex Mono"
									},
									stroke: "var(--color-border)"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(YAxis, {
									domain: [64, 78],
									tick: {
										fill: "var(--color-muted)",
										fontSize: 11,
										fontFamily: "IBM Plex Mono"
									},
									stroke: "var(--color-border)",
									width: 48
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Tooltip, { contentStyle: {
									background: "var(--color-elevated)",
									border: "1px solid var(--color-border)",
									borderRadius: 8,
									fontFamily: "IBM Plex Mono",
									fontSize: 12
								} }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Line, {
									type: "monotone",
									dataKey: "star",
									stroke: "var(--color-fg)",
									dot: false,
									strokeWidth: 2,
									name: "STAR"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Line, {
									type: "monotone",
									dataKey: "planck",
									stroke: "var(--color-steel)",
									dot: false,
									strokeWidth: 1.4,
									name: "Planck"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Line, {
									type: "monotone",
									dataKey: "shoes",
									stroke: "var(--color-muted)",
									dot: false,
									strokeDasharray: "4 4",
									strokeWidth: 1.2,
									name: "SH0ES"
								})
							]
						})
					})
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-6 lg:grid-cols-3",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Control, {
						label: "Redshift z",
						value: zPlot.toFixed(2),
						min: 0,
						max: 2.4,
						step: .01,
						val: zPlot,
						onChange: (v) => set({ z: v })
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Control, {
						label: "β · entropy curvature",
						value: beta.toFixed(2),
						min: 0,
						max: 1.2,
						step: .01,
						val: beta,
						onChange: (v) => set({ beta: v })
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Control, {
						label: "γ · metric trace",
						value: gamma.toFixed(2),
						min: 0,
						max: 1,
						step: .01,
						val: gamma,
						onChange: (v) => set({ gamma: v })
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
					label: "⟨Ω_E⟩_z",
					value: om.toFixed(4),
					hint: "weighted real period"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
					label: "⟨Ω_E⟩_z / ⟨Ω_E⟩_∞",
					value: (om / omInf).toFixed(4),
					hint: "local vs global sampling"
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "font-display text-2xl tracking-tight",
					children: "Supercluster anchors"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
					className: "mt-2 max-w-2xl text-sm text-muted",
					children: [
						"First-principles UCF scaling uses κ ≈ ",
						KAPPA_UCF,
						" with Virgo as the geometric origin. H_eff factors below are the published S.T.A.R. run summary."
					]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mt-4 overflow-x-auto rounded-xl bg-surface shadow-[var(--shadow-border)]",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("table", {
						className: "w-full min-w-[640px] text-left text-sm",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("thead", {
							className: "font-mono text-[10px] uppercase tracking-[0.14em] text-subtle",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tr", {
								className: "border-b border-border",
								children: [
									"Cluster",
									"r (Mly)",
									"Rank",
									"H_eff factor",
									"Entropy",
									"Coh. class"
								].map((h) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("th", {
									className: "px-4 py-3 font-medium",
									children: h
								}, h))
							})
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("tbody", {
							className: "font-mono tabular-nums",
							children: CLUSTERS.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("tr", {
								className: "border-b border-border/70 last:border-0",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
										className: "px-4 py-3 font-sans text-fg",
										children: c.name
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
										className: "px-4 py-3 text-muted",
										children: c.rMly
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
										className: "px-4 py-3 text-muted",
										children: c.rank
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
										className: "px-4 py-3 text-fg",
										children: c.hFactor.toFixed(4)
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
										className: "px-4 py-3 text-muted",
										children: c.entropy.toFixed(2)
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("td", {
										className: "px-4 py-3 text-muted",
										children: c.cohClass.toFixed(2)
									})
								]
							}, c.name))
						})]
					})
				})
			] })
		]
	});
}
function Control({ label, value, min, max, step, val, onChange }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "rounded-xl bg-surface p-4 shadow-[var(--shadow-border)]",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "flex items-baseline justify-between",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "font-mono text-[10px] uppercase tracking-[0.14em] text-subtle",
				children: label
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "font-mono text-sm tabular-nums",
				children: value
			})]
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Slider, {
			min,
			max,
			step,
			value: [val],
			onValueChange: (v) => onChange(v[0] ?? val),
			className: "mt-2"
		})]
	});
}
//#endregion
export { HubblePage as component };
