import { s as require_jsx_runtime } from "../_libs/@radix-ui/react-collection+[...].mjs";
import { g as useLab } from "./store-BJHkQxaW.mjs";
import { n as Button } from "./router-JzY0Ux2j.mjs";
import { n as Formula, r as Metric, t as Badge } from "./formula-vgr3i3sJ.mjs";
import { t as Slider } from "./slider-XbJnmBY9.mjs";
import { t as Switch } from "./switch-X-7IChZi.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/action-xfkUde8i.js
var import_jsx_runtime = require_jsx_runtime();
var TERMS = [
	{
		id: "EH",
		title: "Einstein–Hilbert",
		body: "S_EH = (1/16πG) ∫ R ε_g. Standard GR curvature, plus GHY on ∂M."
	},
	{
		id: "φ",
		title: "Scalar",
		body: "S_φ = −∫ [½ (∇φ)² + V(φ)] ε_g. Sourced by α_φ T_m whenever A depends on φ."
	},
	{
		id: "Y",
		title: "Thermodynamic sigma model",
		body: "S_Y = −∫ [½ G_AB ∂Y^A ∂Y^B + U(Y)] ε_g. Target Christoffel Γ^A_BC enter the EL equation."
	},
	{
		id: "B",
		title: "Two-form kinetic",
		body: "S_B = −½ ∫ H ∧ *H with H = dB. Gauge B → B + dΛ leaves H invariant."
	},
	{
		id: "top",
		title: "Topological coupling",
		body: "S_top = λ_Q ∫ B ∧ F_Q. Metric-independent: T_μν^top = 0, yet it sources B and Y."
	},
	{
		id: "m",
		title: "Matter",
		body: "S_m[Ψ_m, Ã = A²(φ, M) g]. Matter is conserved w.r.t. the physical metric, not the Einstein frame."
	}
];
var LIMITS = [
	{
		id: "minimal",
		label: "Minimal RTCH",
		note: "All couplings on"
	},
	{
		id: "no-topology",
		label: "λ_Q = 0",
		note: "d*H = 0, no J_Q"
	},
	{
		id: "no-conformal",
		label: "A = 1",
		note: "Geodesics recovered"
	},
	{
		id: "gr",
		label: "GR limit",
		note: "A = 1 and λ_Q = 0"
	},
	{
		id: "frozen-y",
		label: "Frozen Y",
		note: "F_Q vanishes locally"
	}
];
var EQUATIONS = [
	{
		title: "Einstein",
		tex: "G_μν = 8πG (T^m + T^φ + T^Y + T^B)_μν"
	},
	{
		title: "Scalar",
		tex: "□φ − V'(φ) + α_φ T_m = 0"
	},
	{
		title: "State fields",
		tex: "□Y^A + Γ^A_BC ∇Y^B ∇Y^C − G^{AB}∂_B U = G^{AB}(J_B^{(Q)} + α_B T_m)"
	},
	{
		title: "Two-form",
		tex: "d*H + λ_Q F_Q = 0"
	},
	{
		title: "Bianchi",
		tex: "dH = 0,   dF_Q = 0"
	}
];
function ActionPage() {
	const lab = useLab();
	const Anote = lab.conformalOn ? "A(φ, M) active" : "A = 1";
	const topNote = lab.topologyOn && lab.lambdaQ !== 0 ? "topological source on" : "topological source off";
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-8",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
				className: "max-w-2xl",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Badge, { children: "RTCH master action" }),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
						className: "mt-3 font-display text-4xl tracking-tight",
						children: "Fully variational field system"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-3 text-sm leading-relaxed text-muted",
						children: "Diffeomorphism-invariant relativistic field theory on (M, g) with scalar φ, thermodynamic map Y^A : M → T, and two-form B. The construction is the rigorous RTCH implementation of ECC: ω is closed and cohomologically nontrivial — it is not d(dM)."
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Formula, {
				boxed: true,
				children: [
					"S",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", {
						className: "font-sans text-sm not-italic",
						children: "RTCH"
					}),
					" = S",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "EH" }),
					" + S",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "φ" }),
					" + S",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "Y" }),
					" + S",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "B" }),
					" + S",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "top" }),
					" + S",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "m" }),
					" + S",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "GHY" })
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-3",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "λ_Q",
						value: lab.lambdaQ.toFixed(2),
						hint: topNote
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "α_φ",
						value: lab.conformalOn ? lab.alphaPhi.toFixed(2) : "0",
						hint: Anote
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "α_A",
						value: lab.conformalOn ? lab.alphaA.toFixed(2) : "0",
						hint: "thermodynamic coupling"
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("section", {
				className: "grid gap-3 sm:grid-cols-2 lg:grid-cols-3",
				children: TERMS.map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("article", {
					className: "rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "font-mono text-[10px] uppercase tracking-[0.16em] text-steel",
							children: t.id
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
							className: "mt-2 font-display text-xl tracking-tight",
							children: t.title
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-2 text-sm leading-relaxed text-muted",
							children: t.body
						})
					]
				}, t.id))
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
				className: "font-display text-2xl tracking-tight",
				children: "Euler–Lagrange system"
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "mt-4 space-y-3",
				children: EQUATIONS.map((e) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-lg bg-elevated px-4 py-3 shadow-[var(--shadow-border)]",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: e.title
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-1 font-display text-lg tracking-tight",
						children: e.tex
					})]
				}, e.title))
			})] }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "font-display text-2xl tracking-tight",
					children: "Standard-physics limits"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "mt-2 max-w-2xl text-sm text-muted",
					children: "Independently testable contractions of the master action. GR geodesics and Einstein-frame conservation are recovered when both novel couplings are off."
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mt-4 flex flex-wrap gap-2",
					children: LIMITS.map((l) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Button, {
						variant: "secondary",
						onClick: () => lab.applyLimit(l.id),
						title: l.note,
						children: l.label
					}, l.id))
				})
			] }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "grid gap-6 lg:grid-cols-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
							children: "Conformal factor A(φ, M)"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", {
							className: "mt-4 flex h-11 items-center justify-between",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								className: "text-sm",
								children: "Matter coupling on"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Switch, {
								checked: lab.conformalOn,
								onCheckedChange: (c) => lab.set({ conformalOn: c })
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Field, {
							label: "α_φ",
							val: lab.alphaPhi,
							min: 0,
							max: 1,
							onChange: (v) => lab.set({ alphaPhi: v })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Field, {
							label: "α_A",
							val: lab.alphaA,
							min: 0,
							max: 1,
							onChange: (v) => lab.set({ alphaA: v })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
							className: "mt-3 text-sm text-muted",
							children: [
								"Test particles obey u^ν ∇_ν u^μ = −c² h^",
								"{μν}",
								" ∇_ν ln A. When A = 1 this is geodesic motion."
							]
						})
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
							children: "Why S_top is gravitationally active"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-3 text-sm leading-relaxed text-muted",
							children: "The topological density B ∧ F_Q contains no metric and no Hodge star, so δS_top / δg_μν = 0. It still changes the B and Y equations; the resulting configurations stress spacetime through T^Y and T^B."
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Formula, {
							className: "mt-4 text-base",
							children: "d * H + λ_Q F_Q = 0"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-3 text-sm leading-relaxed text-muted",
							children: "Taking d of this equation is consistent because d² = 0 and d F_Q = 0 — the Bianchi identity of the target cohomology."
						})
					]
				})]
			})
		]
	});
}
function Field({ label, val, min, max, onChange }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "mt-3",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "flex justify-between font-mono text-xs",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "text-subtle",
				children: label
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "tabular-nums",
				children: val.toFixed(2)
			})]
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Slider, {
			min,
			max,
			step: .01,
			value: [val],
			onValueChange: (v) => onChange(v[0] ?? val)
		})]
	});
}
//#endregion
export { ActionPage as component };
