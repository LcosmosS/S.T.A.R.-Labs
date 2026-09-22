import { useEffect, useRef } from "react";
import { evaluateState, gradLnA, matterTrace, type RtchParams } from "@/lib/star/physics";

type Sample = {
  aMean: number;
  residual: number;
  forcePhi: number;
  forceM: number;
  forceQ: number;
  agree: boolean;
};

type Props = {
  params: RtchParams;
  running?: boolean;
  onSample?: (s: Sample) => void;
  className?: string;
};

type Particle = { x: number; y: number; vx: number; vy: number };

export function DynamicsCanvas({ params, running = true, onSample, className }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const paramsRef = useRef(params);
  paramsRef.current = params;
  const runningRef = useRef(running);
  runningRef.current = running;
  const onSampleRef = useRef(onSample);
  onSampleRef.current = onSample;

  useEffect(() => {
    const canvas = canvasRef.current;
    const wrap = wrapRef.current;
    if (!canvas || !wrap) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    let raf = 0;
    let t = 0;
    let alive = true;

    const particles: Particle[] = Array.from({ length: 36 }, (_, i) => ({
      x: 0.12 + (i % 6) * 0.15,
      y: 0.14 + Math.floor(i / 6) * 0.14,
      vx: 0,
      vy: 0,
    }));

    const GW = 28;
    const GH = 18;
    const off = document.createElement("canvas");
    off.width = GW;
    off.height = GH;
    const octx = off.getContext("2d");
    const img = ctx.createImageData(GW, GH);

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
      if (!alive) return;
      const p = paramsRef.current;
      const dt = 0.018;
      if (runningRef.current) t += dt;

      const w = canvas.width;
      const h = canvas.height;
      ctx.fillStyle = "#0c0e12";
      ctx.fillRect(0, 0, w, h);

      let k = 0;
      let aSum = 0;
      let residual = 0;
      let nRes = 0;
      let fPhi = 0;
      let fM = 0;
      let fQ = 0;
      const rho = 1;
      const press = Math.max(0, p.pressure);
      const Tm = matterTrace(rho, press);
      const denom = rho + press;

      for (let j = 0; j < GH; j++) {
        for (let i = 0; i < GW; i++) {
          const x = i / (GW - 1);
          const y = j / (GH - 1);
          const st = evaluateState(x, y, t, p);
          const g = gradLnA(x, y, t, p);
          const px = press * (1 + 0.28 * Math.sin(2 * Math.PI * x) * Math.sin(2 * Math.PI * y));
          const dpx = press * 0.28 * 2 * Math.PI * Math.cos(2 * Math.PI * x) * Math.sin(2 * Math.PI * y);
          const dpy = press * 0.28 * 2 * Math.PI * Math.sin(2 * Math.PI * x) * Math.cos(2 * Math.PI * y);
          const axP = -g.dx;
          const ayP = -g.dy;
          const axF = -dpx / denom + (Tm / denom) * g.dx;
          const ayF = -dpy / denom + (Tm / denom) * g.dy;
          residual += Math.hypot(axP - axF, ayP - ayF);
          nRes += 1;
          aSum += st.A;
          fPhi += Math.abs(p.alphaPhi);
          fM += Math.abs(p.alphaA);
          fQ += Math.abs(st.JQ);
          const lum = Math.min(1, (st.A - 0.7) / 1.4);
          img.data[k++] = Math.floor(14 + 40 * lum);
          img.data[k++] = Math.floor(18 + 55 * lum);
          img.data[k++] = Math.floor(24 + 90 * lum);
          img.data[k++] = 255;
        }
      }

      if (octx) {
        octx.putImageData(img, 0, 0);
        ctx.imageSmoothingEnabled = true;
        ctx.drawImage(off, 0, 0, w, h);
      }

      ctx.strokeStyle = "rgba(138,160,181,0.45)";
      ctx.lineWidth = Math.max(1, 0.8 * dpr);
      const gx = 10;
      const gy = 7;
      for (let j = 0; j < gy; j++) {
        for (let i = 0; i < gx; i++) {
          const x = (i + 0.5) / gx;
          const y = (j + 0.5) / gy;
          const g = gradLnA(x, y, t, p);
          const px = press * 0.28 * 2 * Math.PI * Math.cos(2 * Math.PI * x) * Math.sin(2 * Math.PI * y);
          const py = press * 0.28 * 2 * Math.PI * Math.sin(2 * Math.PI * x) * Math.cos(2 * Math.PI * y);
          const ax = -px / denom + (Tm / denom) * g.dx;
          const ay = -py / denom + (Tm / denom) * g.dy;
          const cx = x * w;
          const cy = y * h;
          const s = 18 * dpr;
          ctx.beginPath();
          ctx.moveTo(cx, cy);
          ctx.lineTo(cx + ax * s, cy + ay * s);
          ctx.stroke();
        }
      }

      if (runningRef.current) {
        for (const part of particles) {
          const g = gradLnA(part.x, part.y, t, p);
          part.vx += -g.dx * dt * 1.8;
          part.vy += -g.dy * dt * 1.8;
          part.vx *= 0.975;
          part.vy *= 0.975;
          part.x += part.vx * dt;
          part.y += part.vy * dt;
          if (part.x < 0.02 || part.x > 0.98) part.vx *= -1;
          if (part.y < 0.02 || part.y > 0.98) part.vy *= -1;
          part.x = Math.min(0.98, Math.max(0.02, part.x));
          part.y = Math.min(0.98, Math.max(0.02, part.y));
        }
      }

      for (const part of particles) {
        ctx.beginPath();
        ctx.arc(part.x * w, part.y * h, 2.4 * dpr, 0, Math.PI * 2);
        ctx.fillStyle = "#d7dee8";
        ctx.fill();
      }

      if (Math.floor(t * 4) !== Math.floor((t - dt) * 4)) {
        onSampleRef.current?.({
          aMean: aSum / (GW * GH),
          residual: residual / Math.max(1, nRes),
          forcePhi: fPhi / (GW * GH),
          forceM: fM / (GW * GH),
          forceQ: fQ / (GW * GH),
          agree: residual / Math.max(1, nRes) < 0.08 + press * 2,
        });
      }

      raf = requestAnimationFrame(draw);
    };
    raf = requestAnimationFrame(draw);

    return () => {
      alive = false;
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
