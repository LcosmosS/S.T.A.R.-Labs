import { z } from "zod";
import { getCatalog } from "./catalog.ts";

export const DEMO_VERSION = "starmap-illustrative-v1";
const bounded = (min: number, max: number) => z.number().finite().min(min).max(max);
const fixtureLabels = new Set(getCatalog().map((curve) => curve.label));
const fixtureByLabel = new Map(getCatalog().map((curve) => [curve.label, curve]));
export const snapshotStateSchema = z.object({
  lambdaQ: bounded(0, 2), alphaPhi: bounded(0, 0.8), alphaA: bounded(0, 0.8),
  betaQ: bounded(0, 1.2), lambdaScale: bounded(0.4, 2),
  topologyOn: z.boolean(), conformalOn: z.boolean(), freezeY: z.boolean(),
  windingU: bounded(0, 4).int(), windingV: bounded(0, 4).int(),
  beta: bounded(0, 1.2), gamma: bounded(0, 1), pressure: bounded(0, 0.45), z: bounded(0, 2.4),
  selectedLabel: z.string().max(40).refine((label) => fixtureLabels.has(label), "Unknown fixture").nullable(),
  mappingFamily: z.enum(["acsc", "mcj", "ptd", "ft", "rank-elev"]),
  provenance: z.enum(["all", "illustrative", "synthetic"]),
  showFilaments: z.boolean(), colorMode: z.enum(["rank", "entropy", "omega", "provenance"]), rankLift: z.boolean(),
}).strict().superRefine((state, context) => {
  if (state.selectedLabel && state.provenance !== "all" && fixtureByLabel.get(state.selectedLabel)?.provenance !== state.provenance) {
    context.addIssue({ code: "custom", path: ["selectedLabel"], message: "Fixture is excluded by the saved filter" });
  }
});
export const snapshotInputSchema = z.object({ demoVersion: z.literal(DEMO_VERSION), state: snapshotStateSchema }).strict();
export type SnapshotState = z.infer<typeof snapshotStateSchema>;
export type DemoSnapshot = { id: string; createdAt: string; demoVersion: string; state: SnapshotState; checksum: string };
export function captureSnapshotState(lab: object): SnapshotState {
  const values = lab as Record<string, unknown>;
  const state = Object.fromEntries(Object.keys(snapshotStateSchema.shape).map((key) => [key, values[key]]));
  const visible = getCatalog().filter((curve) => state.provenance === "all" || curve.provenance === state.provenance);
  if (!visible.some((curve) => curve.label === state.selectedLabel)) state.selectedLabel = visible[0]?.label ?? null;
  return snapshotStateSchema.parse(state);
}
