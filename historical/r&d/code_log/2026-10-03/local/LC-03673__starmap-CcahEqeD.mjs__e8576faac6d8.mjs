import { i as __toESM } from "../_runtime.mjs";
import { c as require_react, s as require_jsx_runtime } from "../_libs/@radix-ui/react-collection+[...].mjs";
import { a as KAPPA_UCF, g as useLab, n as FILAMENTS, o as PROJECTED, t as CLUSTERS } from "./store-BJHkQxaW.mjs";
import { r as Metric, t as Badge } from "./formula-vgr3i3sJ.mjs";
import { t as OrbitCloud } from "./orbit-cloud-CutwTzrs.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/starmap-CcahEqeD.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function EntropyField({ points, className }) {
	const canvasRef = (0, import_react.useRef)(null);
	const wrapRef = (0, import_react.useRef)(null);
	(0, import_react.useEffect)(() => {
		const canvas = canvasRef.current;
		const wrap = wrapRef.current;
		if (!canvas || !wrap) return;
		const ctx = canvas.getContext("2d");
		if (!ctx) return;
		const dpr = Math.min(window.devicePixelRatio || 1, 2);
		const draw = () => {
			const r = wrap.getBoundingClientRect();
			canvas.width = Math.max(1, Math.floor(r.width * dpr));
			canvas.height = Math.max(1, Math.floor(r.height * dpr));
			canvas.style.width = `${r.width}px`;
			canvas.style.height = `${r.height}px`;
			const w = canvas.width;
			const h = canvas.height;
			const W = 90;
			const H = 70;
			const img = ctx.createImageData(W, H);
			let max = 0;
			const field = /* @__PURE__ */ new Float32Array(6300);
			for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
				const px = x / 89 * 2 - 1;
				const py = y / 69 * 2 - 1;
				let v = 0;
				for (const p of points) {
					const dx = px - p.x * .55;
					const dy = py - p.y * .55;
					const s = .08 + .02 * p.rank;
					v += p.entropy * Math.exp(-(dx * dx + dy * dy) / (2 * s * s));
				}
				field[y * W + x] = v;
				if (v > max) max = v;
			}
			let k = 0;
			for (let i = 0; i < field.length; i++) {
				const t = field[i] / (max + 1e-6);
				img.data[k++] = Math.floor(12 + 30 * t);
				img.data[k++] = Math.floor(16 + 70 * t);
				img.data[k++] = Math.floor(22 + 140 * t);
				img.data[k++] = 255;
			}
			const off = document.createElement("canvas");
			off.width = W;
			off.height = H;
			off.getContext("2d")?.putImageData(img, 0, 0);
			ctx.imageSmoothingEnabled = true;
			ctx.drawImage(off, 0, 0, w, h);
			ctx.fillStyle = "rgba(236,238,242,0.8)";
			for (const p of points) {
				if (p.rank < 2) continue;
				const x = (p.x * .55 + 1) / 2 * w;
				const y = (p.y * .55 + 1) / 2 * h;
				ctx.beginPath();
				ctx.arc(x, y, 2.2 * dpr, 0, Math.PI * 2);
				ctx.fill();
			}
		};
		draw();
		const ro = new ResizeObserver(draw);
		ro.observe(wrap);
		return () => ro.disconnect();
	}, [points]);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		ref: wrapRef,
		className,
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("canvas", {
			ref: canvasRef,
			className: "block size-full"
		})
	});
}
function StarMapPage() {
	const selectedLabel = useLab((s) => s.selectedLabel);
	const set = useLab((s) => s.set);
	const selected = PROJECTED.find((p) => p.label === selectedLabel);
	const highRank = PROJECTED.filter((p) => p.rank >= 2).length;
	const meanEnt = PROJECTED.reduce((s, p) => s + p.entropy, 0) / PROJECTED.length;
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-8",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
				className: "max-w-2xl",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Badge, {
						tone: "steel",
						children: "S.T.A.R.M.A.P."
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
						className: "mt-3 font-display text-4xl tracking-tight",
						children: "Cosmic cartography"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-3 text-sm leading-relaxed text-muted",
						children: "High-fidelity topography of the arithmetic sky: filaments from nearest-neighbour persistence on Φ(E), entropy field M(x) as a kernel density of log|Δ|, and supercluster anchors from the UCF scaling a ≈ −κ r."
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-3",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "Filaments",
						value: String(FILAMENTS.length),
						hint: "k = 3 persistence edges"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "Rank ≥ 2",
						value: String(highRank),
						hint: "local structure bias"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "⟨log|Δ|⟩",
						value: meanEnt.toFixed(2),
						hint: "entropy proxy"
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-6 lg:grid-cols-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("figure", {
					className: "overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("figcaption", {
						className: "px-4 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: "Arithmetic cosmic web"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(OrbitCloud, {
						points: PROJECTED,
						links: FILAMENTS,
						selected: selectedLabel,
						onSelect: (label) => set({ selectedLabel: label }),
						className: "h-[360px] w-full"
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("figure", {
					className: "overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("figcaption", {
						className: "px-4 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: "Entropy field M(x) · rank ≥ 2 marked"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(EntropyField, {
						points: PROJECTED,
						className: "h-[360px] w-full"
					})]
				})]
			}),
			selected ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: "Focused curve"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-1 font-display text-2xl",
						children: selected.label
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
						className: "mt-2 text-sm text-muted",
						children: [
							"Rank ",
							selected.rank,
							", conductor ",
							selected.conductor.toLocaleString(),
							", Ω = ",
							selected.omega.toFixed(4),
							". Entropy proxy log|Δ| = ",
							selected.entropy.toFixed(2),
							"."
						]
					})
				]
			}) : null,
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "font-display text-2xl tracking-tight",
					children: "UCF cluster lattice"
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
					className: "mt-2 max-w-2xl text-sm text-muted",
					children: [
						"Virgo is the geometric origin (r = 54 Mly, a = −1706) with data-driven κ = ",
						KAPPA_UCF,
						". Comoving volumes and cohomology classes follow entropy × (rank + 1) / √r."
					]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5",
					children: CLUSTERS.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("article", {
						className: "rounded-xl bg-surface p-4 shadow-[var(--shadow-border)]",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "font-display text-xl tracking-tight",
							children: c.name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mt-3 space-y-2 font-mono text-xs tabular-nums text-muted",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "flex justify-between",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "r" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
										className: "text-fg",
										children: [c.rMly, " Mly"]
									})]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "flex justify-between",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "a" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
										className: "text-fg",
										children: c.derivedA
									})]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "flex justify-between",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "H factor" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
										className: "text-fg",
										children: c.hFactor.toFixed(4)
									})]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "flex justify-between",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "rank" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
										className: "text-fg",
										children: c.rank
									})]
								})
							]
						})]
					}, c.name))
				})
			] })
		]
	});
}
//#endregion
export { StarMapPage as component };
