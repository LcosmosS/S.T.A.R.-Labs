import type { ReactNode } from "react";
import { Link, useRouterState } from "@tanstack/react-router";
import { Activity, Atom, Compass, Globe2, Hexagon, Menu, Orbit } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { TooltipProvider } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { getCatalog } from "@/lib/star/catalog";
import { hEff, hLcdm, PROJECTED } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";

const NAV = [
  { to: "/", label: "Deck", icon: Compass },
  { to: "/projection", label: "Projection", icon: Orbit },
  { to: "/hubble", label: "Hubble", icon: Activity },
  { to: "/cohomology", label: "Charge", icon: Hexagon },
  { to: "/action", label: "Action", icon: Atom },
  { to: "/starmap", label: "Map", icon: Globe2 },
] as const;

function NavLinks({ onClick }: { onClick?: () => void }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  return (
    <nav className="flex flex-col gap-1">
      {NAV.map((item) => {
        const active = pathname === item.to;
        const Icon = item.icon;
        return (
          <Link
            key={item.to}
            to={item.to}
            onClick={onClick}
            className={cn(
              "flex h-11 items-center gap-3 rounded-md px-3 text-sm font-medium transition-colors",
              active ? "bg-elevated text-fg shadow-[var(--shadow-border)]" : "text-muted hover:bg-elevated/70 hover:text-fg",
            )}
          >
            <Icon className="size-4" />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}

function Wordmark() {
  return (
    <Link to="/" className="flex items-baseline gap-2">
      <span className="font-display text-xl tracking-tight text-fg">STARMAP</span>
      <span className="hidden font-mono text-[10px] uppercase tracking-[0.18em] text-subtle sm:inline">S.T.A.R.</span>
    </Link>
  );
}

export function Shell({ children }: { children: ReactNode }) {
  const z = useLab((s) => s.z);
  const beta = useLab((s) => s.beta);
  const gamma = useLab((s) => s.gamma);
  const H = hEff(z, getCatalog(), beta, gamma) / hLcdm(z, 1);

  return (
    <TooltipProvider delayDuration={200}>
      <div className="min-h-dvh bg-bg text-fg">
        <header className="sticky top-0 z-40 flex h-14 items-center gap-3 border-b border-border bg-bg/90 px-4 backdrop-blur-sm">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="lg:hidden" aria-label="Open navigation">
                <Menu className="size-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left">
              <div className="mb-6 mt-2">
                <Wordmark />
              </div>
              <NavLinks />
            </SheetContent>
          </Sheet>
          <Wordmark />
          <div className="ml-auto flex items-center gap-4">
            <div className="hidden text-right sm:block">
              <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">H0_eff</div>
              <div className="font-mono text-sm tabular-nums text-fg">
                {H.toFixed(2)} <span className="text-muted">km/s/Mpc</span>
              </div>
            </div>
            <div className="hidden text-right md:block">
              <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-subtle">Catalog</div>
              <div className="font-mono text-sm tabular-nums text-fg">{PROJECTED.length} curves</div>
            </div>
          </div>
        </header>

        <div className="mx-auto flex max-w-[1400px]">
          <aside className="sticky top-14 hidden h-[calc(100dvh-3.5rem)] w-52 shrink-0 border-r border-border p-4 lg:block">
            <NavLinks />
            <p className="mt-8 font-mono text-[10px] leading-relaxed text-subtle">
              Symbolic–Topological–Arithmetic Relativity
            </p>
          </aside>
          <main className="min-w-0 flex-1 px-4 py-6 pb-24 lg:px-8 lg:pb-10">{children}</main>
        </div>

        <nav className="fixed inset-x-0 bottom-0 z-40 grid grid-cols-6 border-t border-border bg-bg/95 lg:hidden">
          {NAV.map((item) => (
            <MobileTab key={item.to} {...item} />
          ))}
        </nav>
      </div>
    </TooltipProvider>
  );
}

function MobileTab({ to, label, icon: Icon }: (typeof NAV)[number]) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const active = pathname === to;
  return (
    <Link
      to={to}
      className={cn(
        "flex min-h-14 flex-col items-center justify-center gap-1 text-[10px] tracking-wide",
        active ? "text-fg" : "text-muted",
      )}
    >
      <Icon className="size-4" />
      {label}
    </Link>
  );
}
