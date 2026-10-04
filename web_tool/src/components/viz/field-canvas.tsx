import { useEffect, useRef } from "react";
import { conformalA, localIq, pullbackDensity, type FieldSample, type RtchParams } from "@/lib/star/physics";

type Props = {
  params: RtchParams;
  onSample?: (s: FieldSample) => void;
  className?: string;
};

const N = 48;

export function FieldCanvas({ params, onSample, className }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const paramsRef = useRef(params);
  paramsRef.current = params;
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
      t += 0.016;
      const p = paramsRef.current;
      const wu = p.windingU;
      const wv = p.windingV;
      const jitter = p.freezeY ? 0 : 0.18;
      let q = 0;
      let iqSum = 0;
      let iqMax = 0;
      let hNorm = 0;
      let phi2 = 0;
      let jSum = 0;
      let aSum = 0;

      const F: number[][] = Array.from({ length: N }, () => Array(N).fill(0));
      const Y1 = (i: number, j: number) => {
        const u = i / N;
        const v = j / N;
        return wu * 2 * Math.PI * u + jitter * Math.sin(2 * Math.PI * (3 * u + t * 0.35) + v);
      };
      const Y2 = (i: number, j: number) => {
        const u = i / N;
        const v = j / N;
        return wv * 2 * Math.PI * v + jitter * Math.cos(2 * Math.PI * (2 * v - t * 0.28) + u);
      };

      for (let i = 0; i < N; i++) {
        for (let j = 0; j < N; j++) {
          const d1x = Y1(i + 1, j) - Y1(i, j);
          const d1y = Y1(i, j + 1) - Y1(i, j);
          const d2x = Y2(i + 1, j) - Y2(i, j);
          const d2y = Y2(i, j + 1) - Y2(i, j);
          const Fxy = pullbackDensity(d1x, d1y, d2x, d2y);
          F[i]![j] = Fxy;
          q += Fxy;
          const iq = localIq(Fxy);
          iqSum += iq;
          if (iq > iqMax) iqMax = iq;
          const lam = p.topologyOn ? p.lambdaQ : 0;
          const H = lam * Fxy;
          hNorm += H * H;
          const phi = 0.25 * Math.sin(Y1(i, j)) * Math.cos(Y2(i, j));
          phi2 += phi * phi;
          const JA = (lam / 6) * H * Math.sin(Y2(i, j));
          jSum += JA * JA;
          const M = 0.4 + 0.2 * Math.sin(Y1(i, j) + Y2(i, j));
          const A = conformalA(phi, M, iq, p);
          aSum += A;
        }
      }

      const cell = 1 / (N * N);
      const qDegree = q / (4 * Math.PI * Math.PI);
      if (Math.floor(t * 4) !== Math.floor((t - 0.016) * 4)) {
        onSampleRef.current?.({
          q: qDegree,
          iqMean: iqSum * cell,
          iqMax,
          hNorm: Math.sqrt(hNorm * cell),
          phiRms: Math.sqrt(phi2 * cell),
          sourceJ: Math.sqrt(jSum * cell),
          aMean: aSum * cell,
        });
      }

      let k = 0;
      for (let j = 0; j < N; j++) {
        for (let i = 0; i < N; i++) {
          const Fxy = F[i]![j]!;
          const iq = localIq(Fxy);
          const tq = 0.5 + 0.5 * Math.tanh(Fxy * 1.8);
          const ti = Math.min(1, iq / (iqMax + 1e-6));
          const r = Math.floor(18 + 40 * ti + 90 * tq);
          const g = Math.floor(22 + 55 * ti + 70 * (1 - tq));
          const b = Math.floor(28 + 90 * ti + 110 * (1 - tq));
          img.data[k++] = r;
          img.data[k++] = g;
          img.data[k++] = b;
          img.data[k++] = 255;
        }
      }

      if (octx) {
        octx.putImageData(img, 0, 0);
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(off, 0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = "rgba(215,222,232,0.35)";
        ctx.lineWidth = Math.max(1, dpr);
        const m = Math.min(canvas.width, canvas.height) * 0.32;
        ctx.beginPath();
        ctx.arc(canvas.width * 0.5, canvas.height * 0.5, m, 0, Math.PI * 2);
        ctx.stroke();
        ctx.font = `${11 * dpr}px "IBM Plex Mono"`;
        ctx.fillStyle = "rgba(236,238,242,0.7)";
        ctx.fillText("Σ₂", canvas.width * 0.5 + m * 0.72, canvas.height * 0.5 - m * 0.72);
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

  return (
    <div ref={wrapRef} className={className}>
      <canvas ref={canvasRef} className="block size-full" />
    </div>
  );
}
