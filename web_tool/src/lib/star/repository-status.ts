type ExecutionGates = {
  experimentExecutionEligible: boolean;
  datasetExecutionEligible: boolean;
};

/** Read only the current flags, not historical free-text audit assessments. */
export function executionSummary(gates: ExecutionGates): string {
  return gates.experimentExecutionEligible && gates.datasetExecutionEligible
    ? "Execution eligibility is recorded for the experiment and dataset. A source-locked runner preflight is still required for each controlled run."
    : "Controlled execution is blocked by the recorded experiment or dataset eligibility gate.";
}

type SkyIdentity = {
  datasetId: string;
  sourceSha256: string;
  coordinateSha256: string;
  selectedIdsSha256: string;
  coordinateRole: string;
};

/** An older candidate becomes admitted only for the identical reviewed bytes/role. */
export function matchingSkyRelease<T extends SkyIdentity>(candidate: SkyIdentity, releases: readonly T[]): T | undefined {
  return releases.find(release =>
    release.datasetId === candidate.datasetId &&
    release.sourceSha256 === candidate.sourceSha256 &&
    release.coordinateSha256 === candidate.coordinateSha256 &&
    release.selectedIdsSha256 === candidate.selectedIdsSha256 &&
    release.coordinateRole === candidate.coordinateRole);
}

export function unresolvedPlaceholders(datasets: readonly { Dataset_ID: string; Status: string; Provenance_Status: string }[]): string[] {
  const reserved = new Set(["DATA-PROVENANCE-ALL", "DATA-PHYS-CONSTRAINTS", "DATA-ECC-THEORY"]);
  return datasets.filter(row => reserved.has(row.Dataset_ID) && row.Status === "planned" && row.Provenance_Status === "unknown")
    .map(row => row.Dataset_ID);
}
