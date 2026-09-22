import { createFileRoute, Link } from "@tanstack/react-router";
import { Badge } from "@/components/ui/badge";
import { Formula } from "@/components/viz/formula";

export const Route = createFileRoute("/theory")({ component: TheoryPage });

const CHAIN = [
  { title: "State map", body: "Φ : M → 𝒯, x ↦ Y^A(x)" },
  { title: "Pullback", body: "F_Q = Φ* ω,  d F_Q = 0" },
  { title: "Local scalar", body: "𝒥_Q = ¼ F_Q²  (not Q_RTCH)" },
  { title: "Conformal factor", body: "A = A(φ, ℳ, 𝒥_Q) > 0" },
  { title: "Physical metric", body: "g̃_μν = A² g_μν" },
  { title: "Matter action", body: "S_m[Ψ_m, g̃]" },
  { title: "Both regimes", body: "particles, fluids, T_m, exchange" },
];

const LIMITS = [
  { title: "Candidate action", body: "The master action is a variational realization, not a uniqueness theorem." },
  { title: "Nontrivial class", body: "Existence of closed non-exact ω is an assumption on 𝒯." },
  { title: "Choice of 𝒥_Q", body: "¼ F² is a chosen local invariant among several possible scalars." },
  { title: "A(φ, ℳ, 𝒥_Q)", body: "The conformal coupling is additional model structure." },
  { title: "Two-form B", body: "Introduces extra dynamical degrees of freedom." },
  { title: "No entropy production", body: "A conservative action does not automatically describe irreversible processes." },
  { title: "Arithmetic ≠ thermodynamic", body: "Y^A(E) does not by itself identify rank with mass or conductor with energy." },
  { title: "Open empirics", body: "Local coupling remains untested until a map from observables to (φ, ℳ, F_Q) is specified." },
];

function TheoryPage() {
  return (
    <div className="space-y-10">
      <header className="max-w-2xl">
        <Badge>Status of claims</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Established geometry, conjectural physics</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          The RTCH paper is explicit: conformal matter coupling and closed-form pullbacks are differential geometry.
          Identifying elliptic-curve invariants with thermodynamic fields, and asserting that A depends on 𝒥_Q, are
          conjectural until constrained against nested nulls. Historical wording lives in the{" "}
          <Link to="/charter" className="text-fg underline-offset-4 hover:underline">
            claim registry
          </Link>
          ; its status is set by the Charter.
        </p>
      </header>

      <section>
        <h2 className="font-display text-2xl tracking-tight">Structural chain</h2>
        <ol className="mt-4 grid gap-3 sm:grid-cols-2">
          {CHAIN.map((c, i) => (
            <li key={c.title} className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
              <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-steel">{String(i + 1).padStart(2, "0")}</div>
              <h3 className="mt-2 font-display text-xl tracking-tight">{c.title}</h3>
              <p className="mt-1 font-display text-fg">{c.body}</p>
            </li>
          ))}
        </ol>
      </section>

      <Formula boxed>H₀ : β_Q = 0</Formula>

      <section className="grid gap-4 md:grid-cols-2">
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <Badge tone="ok">Established</Badge>
          <ul className="mt-3 space-y-2 text-sm leading-relaxed text-muted">
            <li>Pullback of a closed form is closed.</li>
            <li>Matter coupled to g̃ = A² g has diffeomorphism-invariant conservation in the physical frame.</li>
            <li>Worldline variation of −m ∫ A ds yields a^ν = −c² h^νμ ∇_μ ln A.</li>
            <li>The dust limit of the Euler equation reproduces that worldline force.</li>
            <li>u_μ f^μ = 0, so four-velocity normalization is preserved.</li>
          </ul>
        </article>
        <article className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
          <Badge tone="warn">Conjectural / ECC / ACSC</Badge>
          <ul className="mt-3 space-y-2 text-sm leading-relaxed text-muted">
            <li>Nontrivial [ω] ∈ H²(𝒯) with thermodynamic interpretation.</li>
            <li>A depends on 𝒥_Q rather than another invariant of F_Q.</li>
            <li>Y^A built from (log N, log |Δ|, r, log R, log |Ω|, …).</li>
            <li>Scale-dependent H_eff from period weighting.</li>
            <li>Arithmetic projection as a source of large-scale structure.</li>
          </ul>
        </article>
      </section>

      <section>
        <h2 className="font-display text-2xl tracking-tight">Limitations (paper §53)</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          {LIMITS.map((l) => (
            <article key={l.title} className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)]">
              <h3 className="font-display text-lg tracking-tight">{l.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">{l.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="max-w-2xl">
        <h2 className="font-display text-2xl tracking-tight">What would count</h2>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          A meaningful RTCH-E1 result is a stable H1/H2 signature longer than matched nulls, surviving seeds, feature
          subsets, and isogeny-class controls, with geodesic or scalar coordinates that predict a held-out invariant.
          Even then it is structure in a chosen metric representation — not a physical law. Falsification is equally
          useful: persistence indistinguishable from N1, or topology explained by a single marginal.
        </p>
      </section>
    </div>
  );
}
