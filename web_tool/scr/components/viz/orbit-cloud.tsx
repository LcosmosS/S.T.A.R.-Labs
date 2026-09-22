import { useEffect, useRef } from "react";
import type { ColorMode, Projected } from "@/lib/star/physics";

type Props = {
  points: Projected[];
  links?: Array<[number, number]>;
  selected?: string | null;
  onSelect?: (label: string) => void;
  autoRotate?: boolean;
  colorMode?: ColorMode;
  showLinks?: boolean;
  className?: string;
};

export function OrbitCloud({
  points,
  links = [],
  selected,
  onSelect,
  autoRotate = true,
  colorMode = "rank",
  showLinks = true,
  className,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const onSelectRef = useRef(onSelect);
  onSelectRef.current = onSelect;
  const selectedRef = useRef(selected);
  selectedRef.current = selected;
  const colorRef = useRef(colorMode);
  colorRef.current = colorMode;
  const linksOnRef = useRef(showLinks);
  linksOnRef.current = showLinks;
  const state = useRef({
    ax: 0.42,
    ay: 0.7,
    dist: 4.6,
    dragging: false,
    lx: 0,
    ly: 0,
    downX: 0,
    downY: 0,
    moved: 0,
    hover: -1,
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    const wrap = wrapRef.current;
    if (!canvas || !wrap) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let raf = 0;
    let running = true;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    let eMin = Infinity;
    let eMax = -Infinity;
    let oMin = Infinity;
    let oMax = -Infinity;
    for (const p of points) {
      if (p.entropy < eMin) eMin = p.entropy;
      if (p.entropy > eMax) eMax = p.entropy;
      if (p.omega < oMin) oMin = p.omega;
      if (p.omega > oMax) oMax = p.omega;
    }

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

    const project = (p: { x: number; y: number; z: number }) => {
      const { ax, ay, dist } = state.current;
      const cosx = Math.cos(ax);
      const sinx = Math.sin(ax);
      const cosy = Math.cos(ay);
      const siny = Math.sin(ay);
      const y1 = p.y * cosx - p.z * sinx;
      const z1 = p.y * sinx + p.z * cosx;
      const x2 = p.x * cosy + z1 * siny;
      const z2 = -p.x * siny + z1 * cosy;
      const f = 2.2 / (dist + z2);
      return { X: x2 * f, Y: y1 * f, z: z2, f };
    };

    const hit = (mx: number, my: number) => {
      const w = canvas.width;
      const h = canvas.height;
      let best = -1;
      let bestD = 18 * dpr;
      for (let i = 0; i < points.length; i++) {
        const q = project(points[i]!);
        const px = w * 0.5 + q.X * Math.min(w, h) * 0.38;
        const py = h * 0.5 + q.Y * Math.min(w, h) * 0.38;
        const d = Math.hypot(px - mx * dpr, py - my * dpr);
        if (d < bestD) {
          bestD = d;
          best = i;
        }
      }
      return best;
    };

    const fillFor = (p: Projected, lit: boolean, hover: boolean) => {
      if (lit || hover) return "rgb(215, 222, 232)";
      const mode = colorRef.current;
      if (mode === "provenance") {
        return p.provenance === "lmfdb" ? "rgba(196, 165, 116, 0.95)" : "rgba(110, 128, 148, 0.82)";
      }
      if (mode === "entropy") {
        const t = (p.entropy - eMin) / Math.max(1e-6, eMax - eMin);
        const r = Math.round(90 + t * 110);
        const g = Math.round(110 + t * 40);
        const b = Math.round(130 - t * 40);
        return `rgba(${r}, ${g}, ${b}, 0.92)`;
      }
      if (mode === "omega") {
        const t = (p.omega - oMin) / Math.max(1e-6, oMax - oMin);
        const r = Math.round(120 - t * 40);
        const g = Math.round(140 + t * 30);
        const b = Math.round(160 + t * 40);
        return `rgba(${r}, ${g}, ${b}, 0.92)`;
      }
      const lum = 140 + p.rank * 22;
      return `rgba(${lum - 30}, ${lum}, ${lum + 20}, 0.92)`;
    };

    const draw = () => {
      if (!running) return;
      if (autoRotate && !state.current.dragging) state.current.ay += 0.0032;
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      const g = ctx.createRadialGradient(w * 0.5, h * 0.52, 0, w * 0.5, h * 0.5, Math.max(w, h) * 0.55);
      g.addColorStop(0, "rgba(24, 28, 36, 0.9)");
      g.addColorStop(1, "rgba(8, 9, 11, 0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);

      const scale = Math.min(w, h) * 0.38;
      const cx = w * 0.5;
      const cy = h * 0.5;

      if (linksOnRef.current) {
        ctx.lineWidth = Math.max(1, 0.7 * dpr);
        for (const [i, j] of links) {
          const a = points[i];
          const b = points[j];
          if (!a || !b) continue;
          const pa = project(a);
          const pb = project(b);
          const alpha = 0.08 + 0.12 * ((pa.f + pb.f) * 0.5);
          ctx.strokeStyle = `rgba(138, 160, 181, ${alpha})`;
          ctx.beginPath();
          ctx.moveTo(cx + pa.X * scale, cy + pa.Y * scale);
          ctx.lineTo(cx + pb.X * scale, cy + pb.Y * scale);
          ctx.stroke();
        }
      }

      const order = points.map((_, i) => i).sort((i, j) => project(points[i]!).z - project(points[j]!).z);
      for (const i of order) {
        const p = points[i]!;
        const q = project(p);
        const px = cx + q.X * scale;
        const py = cy + q.Y * scale;
        const r = (2.1 + p.rank * 0.85) * dpr * (0.75 + 0.4 * q.f);
        const lit = selectedRef.current === p.label;
        const hover = state.current.hover === i;
        ctx.beginPath();
        ctx.arc(px, py, r, 0, Math.PI * 2);
        ctx.fillStyle = fillFor(p, lit, hover);
        ctx.fill();
        if (lit) {
          ctx.strokeStyle = "rgba(215,222,232,0.7)";
          ctx.lineWidth = 1.2 * dpr;
          ctx.beginPath();
          ctx.arc(px, py, r + 4 * dpr, 0, Math.PI * 2);
          ctx.stroke();
        }
      }

      raf = requestAnimationFrame(draw);
    };
    raf = requestAnimationFrame(draw);

    const onDown = (e: PointerEvent) => {
      state.current.dragging = true;
      state.current.lx = e.clientX;
      state.current.ly = e.clientY;
      state.current.downX = e.clientX;
      state.current.downY = e.clientY;
      state.current.moved = 0;
      canvas.setPointerCapture(e.pointerId);
    };
    const onMove = (e: PointerEvent) => {
      const rect = canvas.getBoundingClientRect();
      state.current.hover = hit(e.clientX - rect.left, e.clientY - rect.top);
      if (!state.current.dragging) return;
      const dx = e.clientX - state.current.lx;
      const dy = e.clientY - state.current.ly;
      state.current.lx = e.clientX;
      state.current.ly = e.clientY;
      state.current.moved += Math.hypot(dx, dy);
      state.current.ay += dx * 0.008;
      state.current.ax += dy * 0.008;
      state.current.ax = Math.max(-1.2, Math.min(1.2, state.current.ax));
    };
    const onUp = (e: PointerEvent) => {
      const was = state.current.dragging;
      const moved = state.current.moved;
      state.current.dragging = false;
      if (!was) return;
      if (moved > 6) return;
      const rect = canvas.getBoundingClientRect();
      const i = hit(e.clientX - rect.left, e.clientY - rect.top);
      if (i >= 0) onSelectRef.current?.(points[i]!.label);
    };
    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      state.current.dist = Math.max(2.4, Math.min(8, state.current.dist + e.deltaY * 0.004));
    };

    canvas.addEventListener("pointerdown", onDown);
    canvas.addEventListener("pointermove", onMove);
    canvas.addEventListener("pointerup", onUp);
    canvas.addEventListener("wheel", onWheel, { passive: false });

    return () => {
      running = false;
      cancelAnimationFrame(raf);
      ro.disconnect();
      canvas.removeEventListener("pointerdown", onDown);
      canvas.removeEventListener("pointermove", onMove);
      canvas.removeEventListener("pointerup", onUp);
      canvas.removeEventListener("wheel", onWheel);
    };
  }, [points, links, autoRotate]);

  return (
    <div ref={wrapRef} className={className}>
      <canvas ref={canvasRef} className="block size-full touch-none" />
    </div>
  );
}
