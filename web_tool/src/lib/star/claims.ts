import snapshot from "./registry-snapshot.json";

/** Current website claims come only from the canonical, hashed repository snapshot. */
export type ClaimStatus = string;
export type Claim = {
  id: string;
  qualifiedId: string;
  statement: string;
  module: string;
  category: string;
  status: ClaimStatus;
  support: string;
  next: string;
  controlledSupportEligible: boolean;
  physicalSupportEligible: boolean;
};

export const CLAIMS: Claim[] = snapshot.claims.map((claim) => ({
  id: claim.Claim_ID,
  qualifiedId: claim.Qualified_Claim_ID,
  statement: claim.Statement,
  module: claim.Claim_ID.split("-")[1] ?? claim.Claim_Type,
  category: claim.Claim_Type,
  status: claim.Status,
  support: claim.Current_Audit_Assessment,
  next: claim.Evidence_Requirement,
  controlledSupportEligible: claim.Controlled_Support_Eligible === "true",
  physicalSupportEligible: claim.Physical_Support_Eligible === "true",
}));

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
