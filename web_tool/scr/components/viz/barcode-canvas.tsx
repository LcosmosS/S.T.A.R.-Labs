export function RankWebCanvas({
  points,
  className,
}: {
  points: Array<{ density: number; rank: number; env: "void" | "filament" | "cluster" }>;
  className?: string;
}) {
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
      ctx.fillStyle = "#111318";
      ctx.fillRect(0, 0, w, h);
      if (!points.length) return;
      const dens = points.map((p) => p.density);
      const dMin = Math.min(...dens);
      const dMax = Math.max(...dens);
      const pad = 28 * dpr;
      const envColor: Record<string, string> = {
        void: "rgba(138,160,181,0.85)",
        filament: "rgba(196,165,116,0.9)",
        cluster: "rgba(125,154,134,0.95)",
      };
      for (const p of points) {
        const x = pad + ((p.density - dMin) / Math.max(1e-9, dMax - dMin)) * (w - pad * 2);
        const y = h - pad - (p.rank / 4) * (h - pad * 2);
        ctx.beginPath();
        ctx.arc(x, y, (2.4 + p.rank * 0.7) * dpr, 0, Math.PI * 2);
        ctx.fillStyle = envColor[p.env] ?? envColor.void;
        ctx.fill();
      }
      ctx.fillStyle = "#8b919c";
      ctx.font = `${10 * dpr}px "IBM Plex Mono"`;
      ctx.fillText("kNN density →  ·  rank ↑  ·  steel void · brass filament · green cluster", pad, h - 8 * dpr);
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
