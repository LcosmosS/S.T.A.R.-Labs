import { useEffect, useRef } from "react";
import type { Projected } from "@/lib/star/physics";

type Props = {
  points: Projected[];
  className?: string;
};

export function EntropyField({ points, className }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
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
      const field = new Float32Array(W * H);
      for (let y = 0; y < H; y++) {
        for (let x = 0; x < W; x++) {
          const px = (x / (W - 1)) * 2 - 1;
          const py = (y / (H - 1)) * 2 - 1;
          let v = 0;
          for (const p of points) {
            const dx = px - p.x * 0.55;
            const dy = py - p.y * 0.55;
            const s = 0.08 + 0.02 * p.rank;
            v += p.entropy * Math.exp(-(dx * dx + dy * dy) / (2 * s * s));
          }
          field[y * W + x] = v;
          if (v > max) max = v;
        }
      }
      let k = 0;
      for (let i = 0; i < field.length; i++) {
        const t = field[i]! / (max + 1e-6);
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
        const x = ((p.x * 0.55 + 1) / 2) * w;
        const y = ((p.y * 0.55 + 1) / 2) * h;
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

  return (
    <div ref={wrapRef} className={className}>
      <canvas ref={canvasRef} className="block size-full" />
    </div>
  );
}
