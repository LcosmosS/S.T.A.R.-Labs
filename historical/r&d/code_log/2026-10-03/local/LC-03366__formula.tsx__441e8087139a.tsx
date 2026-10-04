import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Formula({
  boxed,
  className,
  children,
}: {
  boxed?: boolean;
  className?: string;
  children: ReactNode;
}) {
  return (
    <div
      className={cn(
        "font-display text-center text-lg leading-snug tracking-tight text-fg sm:text-xl",
        boxed && "rounded-lg bg-elevated px-4 py-3 shadow-[var(--shadow-border)]",
        className,
      )}
    >
      {children}
    </div>
  );
}

export function Sym({ children, className }: { children: ReactNode; className?: string }) {
  return <span className={cn("font-display italic", className)}>{children}</span>;
}

export function Metric({
  label,
  value,
  unit,
  hint,
}: {
  label: string;
  value: string;
  unit?: string;
  hint?: string;
}) {
  return (
    <div className="min-w-0">
      <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">{label}</div>
      <div className="mt-1 flex items-baseline gap-1.5">
        <span className="font-mono text-lg tabular-nums text-fg sm:text-xl">{value}</span>
        {unit ? <span className="font-mono text-[10px] text-muted">{unit}</span> : null}
      </div>
      {hint ? <div className="mt-0.5 text-xs text-muted">{hint}</div> : null}
    </div>
  );
}
