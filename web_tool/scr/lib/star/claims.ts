export type ClaimStatus =
  | "ACTIVE TEST"
  | "EXPLORATORY"
  | "PRELIMINARY"
  | "OPEN"
  | "SUPPORTED"
  | "SPECULATIVE"
  | "RECLASSIFIED"
  | "FALSIFIED"
  | "DERIVED";

export type Claim = {
  id: string;
  statement: string;
  module: "ACSC" | "GLMPCT" | "ECC" | "RTCH" | "CROSS" | "MAP" | "NEG";
  category: "D" | "E" | "M" | "H" | "C" | "T" | "S" | "P";
  status: ClaimStatus;
  support: string;
  next: string;
};

export const CLAIMS: Claim[] = [
  {
    id: "ACSC-001",
    statement: "Arithmetic invariants of elliptic curves can be projected into a geometric representation that may be compared with cosmic structure.",
    module: "ACSC",
    category: "H",
    status: "ACTIVE TEST",
    support: "S1 — candidate map Φ exists in STARMAP.",
    next: "Compare Φ against null and alternative mappings with locked parameters.",
  },
  {
    id: "ACSC-002",
    statement: "The arithmetic projection Φ(E) corresponds to the topology of large-scale cosmic matter distribution.",
    module: "ACSC",
    category: "H",
    status: "EXPLORATORY",
    support: "S2 pending independent reconstruction. Historical W₂ < 0.01 is model-dependent.",
    next: "H₀: D_arith is no more similar to D_cosmic than randomized or alternative mappings.",
  },
  {
    id: "ACSC-007",
    statement: "Rank determines the vertical/elevation coordinate of the projection (z = 200 r).",
    module: "ACSC",
    category: "M",
    status: "EXPLORATORY",
    support: "S1 — phenomenological scaling, not a constant of nature.",
    next: "Compare against alternative scalings on held-out samples.",
  },
  {
    id: "ACSC-008",
    statement: "Rank corresponds to cosmic dimensionality (0 void, 1 filament, 2 cluster, 3 supercluster).",
    module: "ACSC",
    category: "H",
    status: "ACTIVE TEST",
    support: "S0/S1 — STARMAP tests this as H₁–H₃ on Φ(E) density tertiles.",
    next: "Rank–web permutation test vs shuffled ranks.",
  },
  {
    id: "ACSC-011",
    statement: "Rank growth produces an analogue of dark-energy-driven expansion.",
    module: "ACSC",
    category: "S",
    status: "SPECULATIVE",
    support: "S0",
    next: "Requires a dynamical theory before any expansion test.",
  },
  {
    id: "ACSC-012",
    statement: "Arithmetic invariants can replace the energy-momentum tensor or Einstein tensor.",
    module: "ACSC",
    category: "S",
    status: "SPECULATIVE",
    support: "S0",
    next: "Needs a consistent action, conservation, known limits, and novel predictions.",
  },
  {
    id: "GLMPCT-008",
    statement: "A modified Strong BSD formula involving Fibonacci, π, and φ is supported by the cosmological mapping.",
    module: "GLMPCT",
    category: "H",
    status: "FALSIFIED",
    support: "Documented failure on the tested curves.",
    next: "Preserve as evidence against arbitrary numerical insertions into BSD.",
  },
  {
    id: "MAP-001",
    statement: "The primary projection should not be required to be a strict bijection.",
    module: "MAP",
    category: "M",
    status: "SUPPORTED",
    support: "S1 — design principle: Φ is a projection, many-to-one allowed.",
    next: "Quantify fibers and test whether they carry predictive meaning.",
  },
  {
    id: "MAP-005",
    statement: "BSD is not required for the projection framework.",
    module: "MAP",
    category: "M",
    status: "SUPPORTED",
    support: "S1 — mappings use computable invariants only.",
    next: "Keep alternative maps MCJ / PTD / FT as controls.",
  },
  {
    id: "ECC-003",
    statement: "Entropy curvature can be represented by a closed non-exact 2-form ω with dω = 0 and [ω] ≠ 0.",
    module: "ECC",
    category: "M",
    status: "ACTIVE TEST",
    support: "S1 — T² pullback in STARMAP is a mathematical construction.",
    next: "Specify the target and exhibit an explicit nontrivial class.",
  },
  {
    id: "ECC-008",
    statement: "ECC has been empirically validated as a computational theorem.",
    module: "ECC",
    category: "H",
    status: "RECLASSIFIED",
    support: "Computational performance is not a theorem.",
    next: "Controlled ablation vs unconstrained models.",
  },
  {
    id: "RTCH-003",
    statement: "The pullback satisfies d F_Q = 0 whenever dω = 0.",
    module: "RTCH",
    category: "D",
    status: "DERIVED",
    support: "Standard: pullback commutes with exterior derivative.",
    next: "Keep as a Level D identity, not as physical evidence.",
  },
  {
    id: "RTCH-006",
    statement: "Matter may couple through Ã = A²(φ, ℳ, 𝒥_Q) g.",
    module: "RTCH",
    category: "M",
    status: "ACTIVE TEST",
    support: "S1 — candidate conformal coupling.",
    next: "Equivalence-principle, Solar-System, pulsar, lensing, cosmology.",
  },
  {
    id: "RTCH-007",
    statement: "The conformal coupling produces a fifth-force-like acceleration a^ν = −c² h^νμ ∇_μ ln A.",
    module: "RTCH",
    category: "D",
    status: "DERIVED",
    support: "Worldline variation of −m ∫ A ds, conditional on the action.",
    next: "Dust limit of the Euler equation must agree — STARMAP Dynamics page.",
  },
  {
    id: "CROSS-001",
    statement: "Arithmetic rank may be related to cosmic-web morphology.",
    module: "CROSS",
    category: "H",
    status: "ACTIVE TEST",
    support: "Primary active hypothesis.",
    next: "P(r | cluster, filament, void) with survey controls.",
  },
  {
    id: "CROSS-008",
    statement: "The Hubble–Planck tension can be explained by the S.T.A.R. framework.",
    module: "CROSS",
    category: "S",
    status: "OPEN",
    support: "Downstream hypothesis only.",
    next: "Requires a consistent dynamical cosmological model first.",
  },
  {
    id: "NEG-001",
    statement: "Modified Strong BSD expressions involving Fibonacci, π, and φ fail on tested curves.",
    module: "NEG",
    category: "E",
    status: "FALSIFIED",
    support: "Negative result retained as a scientific result.",
    next: "Do not reintroduce the same perturbation.",
  },
];

export const CORE_QUESTIONS = [
  {
    id: "Q1",
    title: "Arithmetic → cosmic structure",
    body: "Can arithmetic invariants be mapped into geometric or topological structures that correspond nontrivially to independently observed cosmic structure?",
  },
  {
    id: "Q2",
    title: "Arithmetic topography",
    body: "Can those invariants become scalar or vector fields whose geometry can be compared with matter, lensing, or radiation — without assuming they are gravity?",
  },
  {
    id: "Q3",
    title: "Rank and the cosmic web",
    body: "Does rank, alone or with other invariants, predict clusters, filaments, voids, or web complexity better than shuffled and alternative controls?",
  },
  {
    id: "Q4",
    title: "Evolution",
    body: "Can an arithmetic family indexed by τ reproduce features of cosmic topology as a function of redshift, without identifying τ with z or rank with time?",
  },
  {
    id: "Q5",
    title: "Symbolic fields",
    body: "If robust correspondence exists, can it be expressed as a consistent variational theory that recovers known limits? RTCH is a candidate, not a replacement for Einstein gravity.",
  },
];
