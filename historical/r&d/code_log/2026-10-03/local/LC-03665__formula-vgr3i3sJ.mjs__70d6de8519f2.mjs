import { s as require_jsx_runtime } from "../_libs/@radix-ui/react-collection+[...].mjs";
import { l as cn } from "./store-BJHkQxaW.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/formula-vgr3i3sJ.js
var import_jsx_runtime = require_jsx_runtime();
function Badge({ className, tone = "default", ...props }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		className: cn("inline-flex items-center rounded-sm px-2 py-0.5 font-mono text-[10px] uppercase tracking-[0.14em] tabular-nums", tone === "default" && "bg-elevated text-muted shadow-[var(--shadow-border)]", tone === "steel" && "bg-steel/15 text-steel", tone === "warn" && "bg-warn/15 text-warn", tone === "ok" && "bg-ok/15 text-ok", tone === "danger" && "bg-danger/15 text-danger", className),
		...props
	});
}
function Formula({ boxed, className, children }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: cn("font-display text-center text-lg leading-snug tracking-tight text-fg sm:text-xl", boxed && "rounded-lg bg-elevated px-4 py-3 shadow-[var(--shadow-border)]", className),
		children
	});
}
function Sym({ children, className }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		className: cn("font-display italic", className),
		children
	});
}
function Metric({ label, value, unit, hint }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "min-w-0",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "font-mono text-[10px] uppercase tracking-[0.16em] text-subtle",
				children: label
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mt-1 flex items-baseline gap-1.5",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "font-mono text-lg tabular-nums text-fg sm:text-xl",
					children: value
				}), unit ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "font-mono text-[10px] text-muted",
					children: unit
				}) : null]
			}),
			hint ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "mt-0.5 text-xs text-muted",
				children: hint
			}) : null
		]
	});
}
//#endregion
export { Sym as i, Formula as n, Metric as r, Badge as t };
