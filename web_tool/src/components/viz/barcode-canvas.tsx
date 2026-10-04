import { useEffect, useRef } from "react";
import type { ExperimentResult, Interval } from "@/lib/star/rtch-e1";
import type { RankWebResult } from "@/lib/star/rank-web";

type Size = { width: number; height: number };
type Plot = { left: number; top: number; width: number; height: number };
type Paint = (ctx: CanvasRenderingContext2D, size: Size) => void;
const MUTED = "#9aa5b4";
const GRID = "#29303a";
const RANK_COLORS = ["#91a9c0", "#d6b77e", "#93b8a0", "#be9fd3"];
const ENV_COLORS = { void: "#91a9c0", filament: "#d6b77e", cluster: "#93b8a0" };

function CanvasSurface({ paint, description, className }: { paint: Paint; description: string; className?: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    const wrap = wrapRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !wrap || !ctx) return;
    const draw = () => {
      const { width, height } = wrap.getBoundingClientRect();
      if (width <= 0 || height <= 0) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.max(1, Math.round(width * dpr));
      canvas.height = Math.max(1, Math.round(height * dpr));
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = "#111318";
      ctx.fillRect(0, 0, width, height);
      ctx.font = '10px "IBM Plex Mono", monospace';
      paint(ctx, { width, height });
    };
    draw();
    const observer = typeof ResizeObserver === "undefined" ? null : new ResizeObserver(draw);
    observer?.observe(wrap);
    window.addEventListener("resize", draw);
    return () => {
      observer?.disconnect();
      window.removeEventListener("resize", draw);
    };
  }, [paint]);
  return (
    <div ref={wrapRef} className={className ?? "h-56 w-full"}>
      <canvas ref={canvasRef} className="block size-full" role="img" aria-label={description}>{description}</canvas>
    </div>
  );
}

function numberLabel(value: number) {
  const magnitude = Math.abs(value);
  return magnitude > 0 && (magnitude < 0.01 || magnitude >= 10000)
    ? value.toExponential(1) : Number(value.toFixed(2)).toString();
}

function extent(values: number[]): [number, number] {
  const lo = Math.min(...values), hi = Math.max(...values);
  // Constant coordinates stay centered; only the displayed axis range expands.
  const margin = lo === hi ? Math.max(0.5, Math.abs(lo) * 0.05) : (hi - lo) * 0.06;
  return [lo - margin, hi + margin];
}

function empty(ctx: CanvasRenderingContext2D, size: Size, message: string) {
  ctx.fillStyle = MUTED;
  ctx.textAlign = "center";
  ctx.fillText(message, size.width / 2, size.height / 2);
}

function plotArea(size: Size): Plot {
  return { left: 44, top: 16, width: Math.max(1, size.width - 62), height: Math.max(1, size.height - 76) };
}

function axes(ctx: CanvasRenderingContext2D, plot: Plot, xMin: number, xMax: number, yMin: number, yMax: number, xLabel: string, yLabel: string, yTicks?: number[]) {
  ctx.lineWidth = 1;
  ctx.fillStyle = MUTED;
  const ys = yTicks ?? Array.from({ length: 5 }, (_, i) => yMin + (yMax - yMin) * i / 4);
  ctx.textAlign = "right";
  for (const value of ys) {
    const y = plot.top + plot.height - (value - yMin) / (yMax - yMin) * plot.height;
    ctx.strokeStyle = GRID;
    ctx.beginPath();
    ctx.moveTo(plot.left, y);
    ctx.lineTo(plot.left + plot.width, y);
    ctx.stroke();
    ctx.fillText(numberLabel(value), plot.left - 7, y + 3);
  }
  ctx.textAlign = "center";
  for (let i = 0; i <= 4; i++) ctx.fillText(numberLabel(xMin + (xMax - xMin) * i / 4), plot.left + plot.width * i / 4, plot.top + plot.height + 16);
  ctx.strokeStyle = MUTED;
  ctx.beginPath();
  ctx.moveTo(plot.left, plot.top);
  ctx.lineTo(plot.left, plot.top + plot.height);
  ctx.lineTo(plot.left + plot.width, plot.top + plot.height);
  ctx.stroke();
  ctx.fillText(xLabel, plot.left + plot.width / 2, plot.top + plot.height + 32);
  ctx.save();
  ctx.translate(12, plot.top + plot.height / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText(yLabel, 0, 0);
  ctx.restore();
}

function legend(ctx: CanvasRenderingContext2D, size: Size, items: Array<[string, string]>) {
  let x = 44;
  ctx.textAlign = "left";
  for (const [label, color] of items) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x + 3, size.height - 12, 3, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = MUTED;
    ctx.fillText(label, x + 11, size.height - 9);
    x += ctx.measureText(label).width + 25;
  }
}

export function BarcodeCanvas({ intervals, className }: { intervals: Interval[]; className?: string }) {
  const paint: Paint = (ctx, size) => {
    const valid = intervals.filter((iv) => Number.isFinite(iv.birth) && (Number.isFinite(iv.death) || iv.death === Infinity) && iv.death >= iv.birth);
    if (!valid.length) return empty(ctx, size, "No persistence intervals supplied");
    const xMin = Math.min(0, ...valid.map((iv) => iv.birth));
    const xMax = Math.max(xMin + 1e-9, ...valid.map((iv) => Number.isFinite(iv.death) ? iv.death : iv.birth));
    const left = 44, right = Math.max(left + 1, size.width - 20);
    const top = 14, bottom = Math.max(top + 1, size.height - 42);
    const xAt = (value: number) => left + (value - xMin) / (xMax - xMin) * (right - left);
    const rowHeight = (bottom - top) / valid.length;
    ctx.textAlign = "left";
    for (let i = 0; i < valid.length; i++) {
      const iv = valid[i]!;
      const y = top + rowHeight * (i + 0.5);
      const start = xAt(iv.birth), end = iv.death === Infinity ? right : xAt(iv.death);
      ctx.fillStyle = MUTED;
      if (rowHeight >= 8) ctx.fillText(`H${iv.dim}`, 13, y + 3);
      ctx.strokeStyle = iv.dim === 0 ? RANK_COLORS[0]! : RANK_COLORS[1]!;
      ctx.lineWidth = Math.max(1, Math.min(3, rowHeight * 0.55));
      ctx.beginPath();
      ctx.moveTo(start, y);
      ctx.lineTo(end, y);
      ctx.stroke();
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(start, y - 2);
      ctx.lineTo(start, y + 2);
      if (iv.death === Infinity) {
        ctx.moveTo(end - 4, y - 3);
        ctx.lineTo(end, y);
        ctx.lineTo(end - 4, y + 3);
      } else {
        ctx.moveTo(end, y - 2);
        ctx.lineTo(end, y + 2);
      }
      ctx.stroke();
    }
    ctx.fillStyle = MUTED;
    ctx.textAlign = "center";
    ctx.lineWidth = 1;
    ctx.strokeStyle = GRID;
    ctx.beginPath();
    ctx.moveTo(left, bottom + 3);
    ctx.lineTo(right, bottom + 3);
    ctx.stroke();
    for (let i = 0; i <= 4; i++) ctx.fillText(numberLabel(xMin + (xMax - xMin) * i / 4), left + (right - left) * i / 4, bottom + 18);
    ctx.fillText(`${valid.length} supplied intervals · filtration distance`, size.width / 2, size.height - 8);
  };
  return <CanvasSurface paint={paint} className={className} description={`Persistence barcode of ${intervals.length} supplied intervals, plotted from birth to death.`} />;
}

export function PcaCanvas({ points, className }: { points: ExperimentResult["pca"]; className?: string }) {
  const paint: Paint = (ctx, size) => {
    const valid = points.filter((p) => Number.isFinite(p.x) && Number.isFinite(p.y) && Number.isFinite(p.rank));
    if (!valid.length) return empty(ctx, size, "No embedding points supplied");
    const plot = plotArea(size);
    const [xLo, xHi] = extent(valid.map((p) => p.x));
    const [yLo, yHi] = extent(valid.map((p) => p.y));
    // Equal units preserve the geometry of the supplied PCA coordinates.
    const scale = Math.min(plot.width / (xHi - xLo), plot.height / (yHi - yLo));
    const xMid = (xLo + xHi) / 2, yMid = (yLo + yHi) / 2;
    const xMin = xMid - plot.width / scale / 2, xMax = xMid + plot.width / scale / 2;
    const yMin = yMid - plot.height / scale / 2, yMax = yMid + plot.height / scale / 2;
    axes(ctx, plot, xMin, xMax, yMin, yMax, "PC 1 score", "PC 2 score");
    ctx.globalAlpha = 0.8;
    for (const point of valid) {
      ctx.fillStyle = RANK_COLORS[Math.min(3, Math.max(0, Math.floor(point.rank)))]!;
      ctx.beginPath();
      ctx.arc(plot.left + (point.x - xMin) * scale, plot.top + (yMax - point.y) * scale, 2.7, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    legend(ctx, size, RANK_COLORS.map((color, i): [string, string] => [`r ${i === 3 ? "3+" : i}`, color]));
  };
  return <CanvasSurface paint={paint} className={className} description={`Principal component scatterplot of ${points.length} supplied points, colored by rank. Both axes use equal distance units.`} />;
}

export function RankWebCanvas({ points, className }: { points: RankWebResult["environments"]; className?: string }) {
  const paint: Paint = (ctx, size) => {
    const valid = points.filter((p) => Number.isFinite(p.density) && Number.isFinite(p.rank));
    if (!valid.length) return empty(ctx, size, "No rank-density points supplied");
    const plot = plotArea(size);
    const [xMin, xMax] = extent(valid.map((p) => p.density));
    const yMin = Math.min(0, Math.floor(Math.min(...valid.map((p) => p.rank))));
    const yMax = Math.max(yMin + 1, Math.ceil(Math.max(...valid.map((p) => p.rank))));
    const step = Math.max(1, Math.ceil((yMax - yMin) / 4));
    const yTicks = Array.from({ length: Math.floor((yMax - yMin) / step) + 1 }, (_, i) => yMin + i * step);
    axes(ctx, plot, xMin, xMax, yMin, yMax, "kNN density", "Rank", yTicks);
    ctx.globalAlpha = 0.8;
    for (const point of valid) {
      const x = plot.left + (point.density - xMin) / (xMax - xMin) * plot.width;
      const y = plot.top + (yMax - point.rank) / (yMax - yMin) * plot.height;
      ctx.fillStyle = ENV_COLORS[point.env];
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    legend(ctx, size, [["low", ENV_COLORS.void], ["middle", ENV_COLORS.filament], ["high", ENV_COLORS.cluster]]);
  };
  return <CanvasSurface paint={paint} className={className} description={`Rank versus local density for ${points.length} supplied points. Steel, brass, and green identify low, middle, and high density tertiles.`} />;
}
