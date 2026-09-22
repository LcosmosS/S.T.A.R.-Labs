import { create } from "zustand";
import { DEFAULT_RTCH, type ColorMode, type MappingFamily, type ProvenanceFilter, type RtchParams } from "./physics";

type LabState = RtchParams & {
  z: number;
  selectedLabel: string | null;
  mappingFamily: MappingFamily;
  provenance: ProvenanceFilter;
  showFilaments: boolean;
  colorMode: ColorMode;
  rankLift: boolean;
  set: (
    p: Partial<
      RtchParams & {
        z: number;
        selectedLabel: string | null;
        mappingFamily: MappingFamily;
        provenance: ProvenanceFilter;
        showFilaments: boolean;
        colorMode: ColorMode;
        rankLift: boolean;
      }
    >,
  ) => void;
  applyLimit: (id: LimitId) => void;
  reset: () => void;
};

export type LimitId = "minimal" | "gr" | "local-only" | "topo-only" | "no-conformal" | "frozen-y";

const LIMITS: Record<LimitId, Partial<RtchParams>> = {
  minimal: DEFAULT_RTCH,
  gr: {
    topologyOn: false,
    conformalOn: false,
    lambdaQ: 0,
    alphaPhi: 0,
    alphaA: 0,
    betaQ: 0,
    freezeY: false,
  },
  "local-only": { topologyOn: false, lambdaQ: 0, conformalOn: true, betaQ: 0.35 },
  "topo-only": { topologyOn: true, lambdaQ: 1, conformalOn: true, betaQ: 0 },
  "no-conformal": { conformalOn: false, alphaPhi: 0, alphaA: 0, betaQ: 0 },
  "frozen-y": { freezeY: true },
};

export const LIMIT_META: Record<LimitId, { label: string; note: string; pair: string }> = {
  minimal: { label: "Full RTCH", note: "λ_Q ≠ 0 and β_Q ≠ 0", pair: "(≠0, ≠0)" },
  gr: { label: "GR limit", note: "no cohomological interaction", pair: "(0, 0)" },
  "local-only": { label: "Local only", note: "A(J_Q) without B ∧ F_Q", pair: "(0, ≠0)" },
  "topo-only": { label: "Topological only", note: "B ∧ F_Q, β_Q = 0", pair: "(≠0, 0)" },
  "no-conformal": { label: "A = 1", note: "geodesics recovered", pair: "A ≡ 1" },
  "frozen-y": { label: "Frozen Y", note: "F_Q vanishes locally", pair: "dY = 0" },
};

const INITIAL = {
  ...DEFAULT_RTCH,
  z: 0,
  selectedLabel: "37.a1",
  mappingFamily: "acsc" as MappingFamily,
  provenance: "all" as ProvenanceFilter,
  showFilaments: true,
  colorMode: "rank" as ColorMode,
  rankLift: false,
};

export const useLab = create<LabState>()((set) => ({
  ...INITIAL,
  set: (p) => set(p),
  applyLimit: (id) => set({ ...DEFAULT_RTCH, ...LIMITS[id] }),
  reset: () => set({ ...INITIAL }),
}));
