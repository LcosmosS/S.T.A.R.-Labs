import { useEffect, useRef } from "react";
import type { RtchParams } from "@/lib/star/physics";

type Props = {
  params: RtchParams;
  className?: string;
};

export function TorusMap({ params, className }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const paramsRef = useRef(params);
  paramsRef.current = params;

  useEffect(() => {
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
      t += 0.016;
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
          const jit = p.freezeY ? 0 : 0.02 * Math.sin(t + 8 * u);
          const x = pad + ((u * p.windingU) % 1) * bw + jit * bw;
          const y = pad + ((v * p.windingV + 0.04 * Math.sin(2 * Math.PI * u + t * 0.4)) % 1) * bh;
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
          const x = pad + ((u * p.windingU + 0.03 * Math.cos(2 * Math.PI * v - t * 0.3)) % 1) * bw;
          const y = pad + ((v * p.windingV) % 1) * bh;
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

  return (
    <div ref={wrapRef} className={className}>
      <canvas ref={canvasRef} className="block size-full" />
    </div>
  );
}
