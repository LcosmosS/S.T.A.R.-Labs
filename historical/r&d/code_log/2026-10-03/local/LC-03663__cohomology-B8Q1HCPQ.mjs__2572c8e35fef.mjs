import { i as __toESM } from "../_runtime.mjs";
import { c as require_react, s as require_jsx_runtime } from "../_libs/@radix-ui/react-collection+[...].mjs";
import { g as useLab, h as pullbackDensity, p as localIq } from "./store-BJHkQxaW.mjs";
import { n as Formula, r as Metric, t as Badge } from "./formula-vgr3i3sJ.mjs";
import { t as Slider } from "./slider-XbJnmBY9.mjs";
import { t as Switch } from "./switch-X-7IChZi.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/cohomology-B8Q1HCPQ.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function TorusMap({ params, className }) {
	const canvasRef = (0, import_react.useRef)(null);
	const wrapRef = (0, import_react.useRef)(null);
	const paramsRef = (0, import_react.useRef)(params);
	paramsRef.current = params;
	(0, import_react.useEffect)(() => {
		const canvas = canvasRef.current;
		const wrap = wrapRef.current;
		if (!canvas || !wrap) return;
		const ctx = canvas.getContext("2d");
		if (!ctx) return;
		const dpr = Math.min(window.devicePixelRatio || 1, 2);
		let raf = 0;
		let t = 0;
		let running = true;
		const resize = () => {
			const r = wrap.getBoundingClientRect();
			canvas.width = Math.max(1, Math.floor(r.width * dpr));
			canvas.height = Math.max(1, Math.floor(r.height * dpr));
			canvas.style.width = `${r.width}px`;
			canvas.style.height = `${r.height}px`;
		};
		resize();
		const ro = new ResizeObserver(resize);
		ro.observe(wrap);
		const draw = () => {
			if (!running) return;
			t += .016;
			const p = paramsRef.current;
			const w = canvas.width;
			const h = canvas.height;
			ctx.fillStyle = "#111318";
			ctx.fillRect(0, 0, w, h);
			const pad = 28 * dpr;
			const bw = w - pad * 2;
			const bh = h - pad * 2;
			ctx.strokeStyle = "rgba(255,255,255,0.1)";
			ctx.strokeRect(pad, pad, bw, bh);
			ctx.font = `${10 * dpr}px "IBM Plex Mono"`;
			ctx.fillStyle = "#8b919c";
			ctx.fillText("θ ~ θ+2π", pad, pad - 8 * dpr);
			ctx.fillText("φ", pad - 18 * dpr, pad + 12 * dpr);
			const n = 18;
			ctx.strokeStyle = "rgba(138,160,181,0.55)";
			ctx.lineWidth = Math.max(1, 1.1 * dpr);
			for (let i = 0; i <= n; i++) {
				ctx.beginPath();
				for (let j = 0; j <= 40; j++) {
					const u = i / n;
					const v = j / 40;
					const jit = p.freezeY ? 0 : .02 * Math.sin(t + 8 * u);
					const x = pad + u * p.windingU % 1 * bw + jit * bw;
					const y = pad + (v * p.windingV + .04 * Math.sin(2 * Math.PI * u + t * .4)) % 1 * bh;
					if (j === 0) ctx.moveTo(x, y);
					else ctx.lineTo(x, y);
				}
				ctx.stroke();
			}
			ctx.strokeStyle = "rgba(215,222,232,0.45)";
			for (let j = 0; j <= n; j++) {
				ctx.beginPath();
				for (let i = 0; i <= 40; i++) {
					const u = i / 40;
					const v = j / n;
					const x = pad + (u * p.windingU + .03 * Math.cos(2 * Math.PI * v - t * .3)) % 1 * bw;
					const y = pad + v * p.windingV % 1 * bh;
					if (i === 0) ctx.moveTo(x, y);
					else ctx.lineTo(x, y);
				}
				ctx.stroke();
			}
			ctx.fillStyle = "#d7dee8";
			ctx.font = `${12 * dpr}px "IBM Plex Mono"`;
			ctx.fillText(`deg (n,m) = (${p.windingU}, ${p.windingV})`, pad, h - 10 * dpr);
			raf = requestAnimationFrame(draw);
		};
		raf = requestAnimationFrame(draw);
		return () => {
			running = false;
			cancelAnimationFrame(raf);
			ro.disconnect();
		};
	}, []);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		ref: wrapRef,
		className,
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("canvas", {
			ref: canvasRef,
			className: "block size-full"
		})
	});
}
var N = 48;
function FieldCanvas({ params, onSample, className }) {
	const canvasRef = (0, import_react.useRef)(null);
	const wrapRef = (0, import_react.useRef)(null);
	const paramsRef = (0, import_react.useRef)(params);
	paramsRef.current = params;
	const onSampleRef = (0, import_react.useRef)(onSample);
	onSampleRef.current = onSample;
	(0, import_react.useEffect)(() => {
		const canvas = canvasRef.current;
		const wrap = wrapRef.current;
		if (!canvas || !wrap) return;
		const ctx = canvas.getContext("2d");
		if (!ctx) return;
		const dpr = Math.min(window.devicePixelRatio || 1, 2);
		let raf = 0;
		let t = 0;
		let running = true;
		const resize = () => {
			const r = wrap.getBoundingClientRect();
			canvas.width = Math.max(1, Math.floor(r.width * dpr));
			canvas.height = Math.max(1, Math.floor(r.height * dpr));
			canvas.style.width = `${r.width}px`;
			canvas.style.height = `${r.height}px`;
		};
		resize();
		const ro = new ResizeObserver(resize);
		ro.observe(wrap);
		const off = document.createElement("canvas");
		off.width = N;
		off.height = N;
		const octx = off.getContext("2d");
		const img = ctx.createImageData(N, N);
		const draw = () => {
			if (!running) return;
			t += .016;
			const p = paramsRef.current;
			const wu = p.windingU;
			const wv = p.windingV;
			const jitter = p.freezeY ? 0 : .18;
			let q = 0;
			let iqSum = 0;
			let iqMax = 0;
			let hNorm = 0;
			let phi2 = 0;
			let jSum = 0;
			let aSum = 0;
			const F = Array.from({ length: N }, () => Array(N).fill(0));
			const Y1 = (i, j) => {
				const u = i / N;
				const v = j / N;
				return wu * 2 * Math.PI * u + jitter * Math.sin(2 * Math.PI * (3 * u + t * .35) + v);
			};
			const Y2 = (i, j) => {
				const u = i / N;
				const v = j / N;
				return wv * 2 * Math.PI * v + jitter * Math.cos(2 * Math.PI * (2 * v - t * .28) + u);
			};
			for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
				const d1x = Y1(i + 1, j) - Y1(i, j);
				const d1y = Y1(i, j + 1) - Y1(i, j);
				const d2x = Y2(i + 1, j) - Y2(i, j);
				const d2y = Y2(i, j + 1) - Y2(i, j);
				const Fxy = pullbackDensity(d1x, d1y, d2x, d2y);
				F[i][j] = Fxy;
				q += Fxy;
				const iq = localIq(Fxy);
				iqSum += iq;
				if (iq > iqMax) iqMax = iq;
				const lam = p.topologyOn ? p.lambdaQ : 0;
				const H = lam * Fxy;
				hNorm += H * H;
				const phi = .25 * Math.sin(Y1(i, j)) * Math.cos(Y2(i, j));
				phi2 += phi * phi;
				const JA = lam / 6 * H * Math.sin(Y2(i, j));
				jSum += JA * JA;
				const M = .4 + .2 * Math.sin(Y1(i, j) + Y2(i, j));
				const A = p.conformalOn ? Math.exp(p.alphaPhi * phi + p.alphaA * M) : 1;
				aSum += A;
			}
			const cell = 1 / 2304;
			const qDegree = q / (4 * Math.PI * Math.PI);
			if (Math.floor(t * 4) !== Math.floor((t - .016) * 4)) onSampleRef.current?.({
				q: qDegree,
				iqMean: iqSum * cell,
				iqMax,
				hNorm: Math.sqrt(hNorm * cell),
				phiRms: Math.sqrt(phi2 * cell),
				sourceJ: Math.sqrt(jSum * cell),
				aMean: aSum * cell
			});
			let k = 0;
			for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
				const Fxy = F[i][j];
				const iq = localIq(Fxy);
				const tq = .5 + .5 * Math.tanh(Fxy * 1.8);
				const ti = Math.min(1, iq / (iqMax + 1e-6));
				const r = Math.floor(18 + 40 * ti + 90 * tq);
				const g = Math.floor(22 + 55 * ti + 70 * (1 - tq));
				const b = Math.floor(28 + 90 * ti + 110 * (1 - tq));
				img.data[k++] = r;
				img.data[k++] = g;
				img.data[k++] = b;
				img.data[k++] = 255;
			}
			if (octx) {
				octx.putImageData(img, 0, 0);
				ctx.imageSmoothingEnabled = false;
				ctx.drawImage(off, 0, 0, canvas.width, canvas.height);
				ctx.strokeStyle = "rgba(215,222,232,0.35)";
				ctx.lineWidth = Math.max(1, dpr);
				const m = Math.min(canvas.width, canvas.height) * .32;
				ctx.beginPath();
				ctx.arc(canvas.width * .5, canvas.height * .5, m, 0, Math.PI * 2);
				ctx.stroke();
				ctx.font = `${11 * dpr}px "IBM Plex Mono"`;
				ctx.fillStyle = "rgba(236,238,242,0.7)";
				ctx.fillText("Σ₂", canvas.width * .5 + m * .72, canvas.height * .5 - m * .72);
			}
			raf = requestAnimationFrame(draw);
		};
		raf = requestAnimationFrame(draw);
		return () => {
			running = false;
			cancelAnimationFrame(raf);
			ro.disconnect();
		};
	}, []);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		ref: wrapRef,
		className,
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("canvas", {
			ref: canvasRef,
			className: "block size-full"
		})
	});
}
function CohomologyPage() {
	const lab = useLab();
	const [sample, setSample] = (0, import_react.useState)({
		q: 0,
		iqMean: 0,
		iqMax: 0,
		hNorm: 0,
		phiRms: 0,
		sourceJ: 0,
		aMean: 1
	});
	const onSample = (0, import_react.useCallback)((s) => setSample(s), []);
	const params = {
		lambdaQ: lab.lambdaQ,
		alphaPhi: lab.alphaPhi,
		alphaA: lab.alphaA,
		topologyOn: lab.topologyOn,
		conformalOn: lab.conformalOn,
		freezeY: lab.freezeY,
		windingU: lab.windingU,
		windingV: lab.windingV,
		beta: lab.beta,
		gamma: lab.gamma
	};
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "space-y-8",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
				className: "max-w-2xl",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Badge, {
						tone: "steel",
						children: "ECC · RTCH"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", {
						className: "mt-3 font-display text-4xl tracking-tight",
						children: "Entropy cohomology"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
						className: "mt-3 text-sm leading-relaxed text-muted",
						children: "Target manifold T² carries a closed 2-form ω with [ω] ≠ 0 in de Rham cohomology. The spacetime pullback F_Q = Φ*ω is closed because d_T ω = 0. The charge on a two-cycle is topological; I_Q is a local dynamical scalar and must not be substituted for Q."
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 md:grid-cols-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Formula, {
					boxed: true,
					children: [
						"Q",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", {
							className: "font-sans text-sm not-italic",
							children: "RTCH"
						}),
						"[Σ",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "2" }),
						"] = ∫ Φ",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sup", { children: "*" }),
						"ω"
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Formula, {
					boxed: true,
					children: [
						"I",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", {
							className: "font-sans text-sm not-italic",
							children: "Q"
						}),
						" = ¼ F",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "Q μν" }),
						" F",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sub", { children: "Q" }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("sup", { children: "μν" })
					]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-4 sm:grid-cols-4",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "Q_RTCH",
						value: sample.q.toFixed(2),
						hint: "normalized degree"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "deg (n,m)",
						value: `${lab.windingU} × ${lab.windingV}`,
						hint: "covering degree"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "⟨I_Q⟩",
						value: sample.iqMean.toExponential(2),
						hint: "local scalar"
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Metric, {
						label: "max I_Q",
						value: sample.iqMax.toExponential(2),
						hint: "not quantized"
					})
				]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-6 lg:grid-cols-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("figure", {
					className: "overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("figcaption", {
						className: "px-4 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: "Pullback F_Q on a spatial slice · Σ₂ marked"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(FieldCanvas, {
						params,
						onSample,
						className: "h-[320px] w-full"
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("figure", {
					className: "overflow-hidden rounded-xl bg-surface shadow-[var(--shadow-border)]",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("figcaption", {
						className: "px-4 py-3 font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: "Target T² with periodic identifications"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(TorusMap, {
						params,
						className: "h-[320px] w-full"
					})]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid gap-6 lg:grid-cols-2",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
							children: "Winding of Φ"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "mt-2 text-sm text-muted",
							children: "Changing covering degree (n, m) jumps Q by integers. Stretching the map changes I_Q continuously without altering the cohomology class."
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mt-4 space-y-4",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "flex justify-between font-mono text-xs",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "text-subtle",
									children: "n · θ winding"
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "tabular-nums",
									children: lab.windingU
								})]
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Slider, {
								min: 0,
								max: 4,
								step: 1,
								value: [lab.windingU],
								onValueChange: (v) => lab.set({ windingU: v[0] ?? 1 })
							})] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "flex justify-between font-mono text-xs",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "text-subtle",
									children: "m · φ winding"
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "tabular-nums",
									children: lab.windingV
								})]
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Slider, {
								min: 0,
								max: 4,
								step: 1,
								value: [lab.windingV],
								onValueChange: (v) => lab.set({ windingV: v[0] ?? 1 })
							})] })]
						})
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
						children: "Dynamical couplings"
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mt-4 space-y-4",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Row, {
								label: "Topological λ_Q",
								checked: lab.topologyOn,
								onChecked: (c) => lab.set({ topologyOn: c })
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "flex justify-between font-mono text-xs",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "text-subtle",
									children: "λ_Q"
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "tabular-nums",
									children: lab.lambdaQ.toFixed(2)
								})]
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Slider, {
								min: 0,
								max: 3,
								step: .05,
								value: [lab.lambdaQ],
								onValueChange: (v) => lab.set({ lambdaQ: v[0] ?? 1 })
							})] }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Row, {
								label: "Freeze Y^A",
								checked: lab.freezeY,
								onChecked: (c) => lab.set({ freezeY: c })
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
								className: "text-sm text-muted",
								children: [
									"Frozen thermodynamic fields set F_Q → 0 locally and remove the cohomological source from the B equation. |H| = ",
									sample.hNorm.toExponential(2),
									", |J_Q| = ",
									sample.sourceJ.toExponential(2),
									"."
								]
							})
						]
					})]
				})]
			})
		]
	});
}
function Row({ label, checked, onChecked }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", {
		className: "flex h-11 items-center justify-between gap-4",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
			className: "text-sm",
			children: label
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Switch, {
			checked,
			onCheckedChange: onChecked
		})]
	});
}
//#endregion
export { CohomologyPage as component };
