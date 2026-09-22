import type { ReactNode } from "react";
import { Link, useRouterState } from "@tanstack/react-router";
import { BookOpen, Compass, FileText, FlaskConical, Github, Hexagon, Menu, Orbit, Table2, Waves } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { TooltipProvider } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { getCatalog } from "@/lib/star/catalog";
import { hEff } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";

const LABS_URL = "https://github.com/LcosmosS/S.T.A.R.-Labs";

const PRIMARY = [
  { to: "/", label: "Deck", icon: Compass },
  { to: "/dynamics", label: "Dynamics", icon: Waves },
  { to: "/experiment", label: "E1", icon: FlaskConical },
  { to: "/cohomology", label: "Charge", icon: Hexagon },
  { to: "/charter", label: "Charter", icon: FileText },
  { to: "/theory", label: "Status", icon: BookOpen },
] as const;

const SECONDARY = [
  { to: "/hubble", label: "Hubble", icon: Waves },
  { to: "/action", label: "Action", icon: Hexagon },
  { to: "/projection", label: "Projection", icon: Orbit },
  { to: "/catalog", label: "Catalog", icon: Table2 },
] as const;

function NavLinks({ onClick }: { onClick?: () => void }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  return (
    <nav className="flex flex-col gap-1">
      {[...PRIMARY, ...SECONDARY].map((item) => {
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
    <Link to="/" className="flex min-w-0 items-baseline gap-2 whitespace-nowrap">
      <span className="font-display text-2xl leading-none tracking-tight text-fg">STARMAP</span>
      <span className="font-sans text-xs font-medium leading-none tracking-wide text-steel">by S.T.A.R. Labs</span>
    </Link>
  );
}

export function Shell({ children }: { children: ReactNode }) {
  const z = useLab((s) => s.z);
  const beta = useLab((s) => s.beta);
  const gamma = useLab((s) => s.gamma);
  const H = hEff(z, getCatalog(), beta, gamma);
  const n = getCatalog().length;

  return (
    <TooltipProvider delayDuration={200}>
      <div className="min-h-dvh bg-bg text-fg">
        <header className="sticky top-0 z-40 flex h-16 items-center gap-3 border-b border-border bg-bg/90 px-4 backdrop-blur-sm">
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
              <div className="font-mono text-sm tabular-nums text-fg">{n} curves</div>
            </div>
            <a
              href={LABS_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex size-11 items-center justify-center rounded-md text-steel transition-colors hover:bg-elevated hover:text-fg"
              aria-label="S.T.A.R. Labs on GitHub"
            >
              <Github className="size-4" />
            </a>
          </div>
        </header>

        <div className="mx-auto flex max-w-[1400px]">
          <aside className="sticky top-16 hidden h-[calc(100dvh-4rem)] w-52 shrink-0 overflow-y-auto border-r border-border p-4 lg:block">
            <NavLinks />
            <p className="mt-8 font-mono text-[10px] leading-relaxed text-subtle">
              Symbolic–Topological–Arithmetic Relativity
            </p>
            <a
              href={LABS_URL}
              target="_blank"
              rel="noreferrer"
              className="mt-3 inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.14em] text-steel hover:text-fg"
            >
              <Github className="size-3" />
              Labs repo
            </a>
          </aside>
          <main className="min-w-0 flex-1 px-4 py-6 pb-24 lg:px-8 lg:pb-10">{children}</main>
        </div>

        <nav className="fixed inset-x-0 bottom-0 z-40 grid grid-cols-6 border-t border-border bg-bg/95 lg:hidden">
          {PRIMARY.map((item) => (
            <MobileTab key={item.to} {...item} />
          ))}
        </nav>
      </div>
    </TooltipProvider>
  );
}

function MobileTab({ to, label, icon: Icon }: (typeof PRIMARY)[number]) {
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
