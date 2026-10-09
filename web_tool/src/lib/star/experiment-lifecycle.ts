/** Pure read-only lifecycle presentation. Canonical Status is authoritative;
 * neither filed protocols nor CI checks imply experiment activation.
 */
export function isPreregisteredStatus(status: string): boolean {
  return /^preregistered(?:$|_)/.test(status.toLowerCase().trim());
}

type ExperimentRow = { Experiment_ID: string; Status: string };
type TheoryRow = { id: string; record: { Status: string }; protocolPath: string };
export type PreregisteredEntry = {
  id: string;
  namespace: "REPO-CSV-v0.2" | "THEORY-SEARCH-v0.1";
  kind: "Controlled experiment protocol" | "Theory/obstruction protocol";
  status: string;
  protocolPath?: string;
};

export function getPreregisteredEntries(snapshot: {
  experiments: readonly ExperimentRow[];
  preregistrations: readonly TheoryRow[];
}): PreregisteredEntry[] {
  const experiments = snapshot.experiments
    .filter((row) => isPreregisteredStatus(row.Status))
    .map((row) => ({
      id: row.Experiment_ID,
      namespace: "REPO-CSV-v0.2" as const,
      kind: "Controlled experiment protocol" as const,
      status: row.Status,
    }));
  const theory = snapshot.preregistrations
    .filter((row) => isPreregisteredStatus(row.record.Status))
    .map((row) => ({
      id: row.id,
      namespace: "THEORY-SEARCH-v0.1" as const,
      kind: "Theory/obstruction protocol" as const,
      status: row.record.Status,
      protocolPath: row.protocolPath,
    }));
  return [...experiments, ...theory].sort((a, b) => a.id.localeCompare(b.id));
}
