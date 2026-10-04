import { create } from "zustand";
import { DEFAULT_RTCH, type RtchParams } from "./physics";

type LabState = RtchParams & {
  z: number;
  selectedLabel: string | null;
  set: (p: Partial<RtchParams & { z: number; selectedLabel: string | null }>) => void;
  applyLimit: (id: LimitId) => void;
  reset: () => void;
};

export type LimitId = "minimal" | "no-topology" | "no-conformal" | "gr" | "frozen-y";

const LIMITS: Record<LimitId, Partial<RtchParams>> = {
  minimal: DEFAULT_RTCH,
  "no-topology": { topologyOn: true, lambdaQ: 0 },
  "no-conformal": { conformalOn: false, alphaPhi: 0, alphaA: 0 },
  gr: { topologyOn: false, conformalOn: false, lambdaQ: 0, alphaPhi: 0, alphaA: 0, freezeY: false },
  "frozen-y": { freezeY: true },
};

export const useLab = create<LabState>()((set) => ({
  ...DEFAULT_RTCH,
  z: 0,
  selectedLabel: "37.a1",
  set: (p) => set(p),
  applyLimit: (id) => set({ ...DEFAULT_RTCH, ...LIMITS[id] }),
  reset: () => set({ ...DEFAULT_RTCH, z: 0 }),
}));
