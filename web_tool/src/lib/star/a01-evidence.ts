import metadata from "./a01-evidence-metadata.json" with { type: "json" };

/** Only immutable primary artifacts enter this model; synthetic fixtures stay separate. */
export interface EvidencePoint {
  readonly label: string;
  readonly isogeny_class: string;
  readonly conductor: number;
  /** Exact integer text: converting discriminants to a Number loses precision. */
  readonly delta: string;
  readonly rank: number;
  readonly torsion_order: number;
  readonly longitude: number;
  readonly latitude: number;
  readonly elevation: number;
}
export interface EvidenceSummary {
  readonly alpha: number;
  readonly analysis_rows: number;
  readonly decision: string;
  readonly experiment_id: string;
  readonly interpretation_limit: string;
  readonly isogeny_policy: string;
  readonly neighbor_k: number;
  readonly null_exceedances: number;
  readonly null_prng: string;
  readonly null_realizations: number;
  readonly null_seed: number;
  readonly observed_statistic: number;
  readonly p_value: number;
  readonly protocol_version: string;
  readonly source_rows: number;
  readonly undirected_edge_count: number;
}
export interface EvidenceData {
  readonly schemaVersion: 1;
  readonly experimentId: "EXP-MAP-A01";
  readonly runId: string;
  readonly points: readonly EvidencePoint[];
  readonly nullStatistics: readonly number[];
  readonly summary: EvidenceSummary;
}

/**
 * Freeze an acyclic JSON value and its unfrozen descendants in place.
 *
 * Metadata and validated payloads use this boundary so display consumers cannot
 * mutate shared evidence. Primitives pass through unchanged; an already frozen
 * object is not traversed again. The return type is shallow, though newly visited
 * object descendants are frozen at runtime.
 *
 * @param value - Parsed JSON or metadata without cyclic references.
 * @returns The same value, with each newly visited object frozen.
 */
function freeze<T>(value: T): Readonly<T> {
  if (value !== null && typeof value === "object" && !Object.isFrozen(value)) {
    for (const child of Object.values(value)) freeze(child);
    Object.freeze(value);
  }
  return value;
}

export const a01EvidenceMetadata = freeze(metadata);
const POINT_KEYS = ["conductor", "delta", "elevation", "isogeny_class", "label", "latitude", "longitude", "rank", "torsion_order"];
const SUMMARY_KEYS = ["alpha", "analysis_rows", "decision", "experiment_id", "interpretation_limit", "isogeny_policy", "neighbor_k", "null_exceedances", "null_prng", "null_realizations", "null_seed", "observed_statistic", "p_value", "protocol_version", "source_rows", "undirected_edge_count"];
/**
 * Narrow an unknown payload field to a non-null, non-array object.
 * This is a structural guard only; callers must validate its keys and values.
 *
 * @param value - Untrusted decoded JSON field.
 * @returns Whether the value can be checked as a string-keyed record.
 */
function object(value: unknown): value is Record<string, unknown> { return value !== null && typeof value === "object" && !Array.isArray(value); }
/**
 * Compare a record's complete enumerable key set with the expected schema keys.
 * Sorting copies the expected list, so validation does not reorder that schema.
 *
 * @param value - Record already accepted by the object guard.
 * @param keys - Required field names, with no optional or additional fields.
 * @returns Whether the sorted, comma-joined key lists match exactly.
 */
function exactKeys(value: Record<string, unknown>, keys: string[]) { return Object.keys(value).sort().join(",") === [...keys].sort().join(","); }
/**
 * Accept finite numeric JSON fields without coercing strings or nulls.
 *
 * @param value - Candidate numeric field.
 * @returns Whether the value is a number other than NaN or either infinity.
 */
function finite(value: unknown): value is number { return typeof value === "number" && Number.isFinite(value); }
/**
 * Require an exactly representable integer at or above an inclusive lower bound.
 *
 * @param value - Candidate count, rank, conductor, or rendering parameter.
 * @param min - Inclusive minimum; defaults to zero.
 * @returns Whether the value is finite, safe as an integer, and within the bound.
 */
function integer(value: unknown, min = 0): value is number { return finite(value) && Number.isSafeInteger(value) && value >= min; }

/**
 * Validate the decoded A01 schema and locked arithmetic-run bindings, then freeze it.
 *
 * Checks cover payload identity and counts, unique curve/isogeny identities,
 * precision-preserving discriminant text, coordinate formulas, pinned summary
 * fields, and the stored nulls' exceedance count and p-value. These checks do not
 * authenticate bytes: production callers must first use the hash-verifying parser.
 * Acceptance preserves the run's stated arithmetic-null interpretation limit and
 * does not establish physical support or independent replication.
 *
 * @param value - Untrusted decoded JSON payload.
 * @returns The same payload as deeply frozen, typed display evidence.
 * @throws When any schema, identity, arithmetic, or pinned-run check fails.
 */
export function validateEvidenceData(value: unknown): EvidenceData {
  if (!object(value) || !exactKeys(value, ["schemaVersion", "experimentId", "runId", "points", "nullStatistics", "summary"]) || value.schemaVersion !== 1 || value.experimentId !== a01EvidenceMetadata.experimentId || value.runId !== a01EvidenceMetadata.runId || !Array.isArray(value.points) || value.points.length !== a01EvidenceMetadata.analysisRows || !Array.isArray(value.nullStatistics) || value.nullStatistics.length !== a01EvidenceMetadata.nullRealizations || !object(value.summary)) throw new Error("Invalid A01 evidence payload identity or row counts");
  const labels = new Set<string>();
  const classes = new Set<string>();
  for (const point of value.points) {
    if (!object(point) || !exactKeys(point, POINT_KEYS) || typeof point.label !== "string" || typeof point.isogeny_class !== "string" || !/^[1-9]\d*[a-z]+$/.test(point.isogeny_class) || point.label !== `${point.isogeny_class}1` || !integer(point.conductor, 11) || point.conductor > 9999 || Number(point.label.match(/^\d+/)?.[0]) !== point.conductor || typeof point.delta !== "string" || !/^-?[1-9]\d*$/.test(point.delta) || !integer(point.rank) || !integer(point.torsion_order, 1) || !finite(point.longitude) || !finite(point.latitude) || !finite(point.elevation) || point.elevation !== 200 * point.rank) throw new Error("Invalid A01 evidence point");
    if (labels.has(point.label) || classes.has(point.isogeny_class)) throw new Error("Duplicate A01 evidence identity");
    labels.add(point.label); classes.add(point.isogeny_class);
    const delta = BigInt(point.delta);
    const magnitude = Number(delta < 0n ? -delta : delta);
    if (!Number.isFinite(magnitude) || Math.abs(point.longitude - 360 * Math.log(magnitude) / Math.log(1e30)) > 1e-10 || Math.abs(point.latitude - 180 * Math.log(point.conductor) / Math.log(1e9)) > 1e-10) throw new Error("A01 arithmetic coordinate formula mismatch");
  }
  const summary = value.summary;
  if (!exactKeys(summary, SUMMARY_KEYS) || summary.alpha !== a01EvidenceMetadata.alpha || summary.analysis_rows !== a01EvidenceMetadata.analysisRows || summary.decision !== "reject_null" || summary.experiment_id !== a01EvidenceMetadata.experimentId || summary.interpretation_limit !== "This endpoint tests local rank/elevation coherence against the locked rank-permutation null only; it does not establish ACSC or physical support." || summary.isogeny_policy !== "curve_number_equals_1_per_isogeny_class" || summary.neighbor_k !== 10 || summary.null_exceedances !== a01EvidenceMetadata.nullExceedances || summary.null_prng !== a01EvidenceMetadata.pinnedParameters.prng || summary.null_realizations !== a01EvidenceMetadata.nullRealizations || summary.null_seed !== a01EvidenceMetadata.pinnedParameters.seed || summary.observed_statistic !== a01EvidenceMetadata.observedStatistic || summary.p_value !== a01EvidenceMetadata.pValue || summary.protocol_version !== a01EvidenceMetadata.protocolVersion || summary.source_rows !== a01EvidenceMetadata.sourceRows || summary.undirected_edge_count !== 221930) throw new Error("A01 summary differs from the pinned execution");
  if (value.nullStatistics.some((statistic: unknown) => !finite(statistic) || statistic > 0)) throw new Error("Invalid A01 null statistic");
  const exceedances = value.nullStatistics.filter((statistic: number) => statistic >= a01EvidenceMetadata.observedStatistic).length;
  if (exceedances !== a01EvidenceMetadata.nullExceedances || (1 + exceedances) / (value.nullStatistics.length + 1) !== summary.p_value) throw new Error("A01 null distribution disagrees with the locked summary");
  return freeze(value) as unknown as EvidenceData;
}

/**
 * Verify the immutable payload's length and SHA-256 before decoding or validating it.
 *
 * UTF-8 decoding is fatal on invalid sequences. A matching hash is a byte-integrity
 * gate; the subsequent shape checks preserve the locked run's display contract,
 * without executing the experiment or extending its scientific interpretation.
 *
 * @param bytes - Original response bytes, without parsing or reserialization.
 * @returns Deeply frozen evidence only after all byte and payload checks pass.
 * @throws If length, browser SHA-256 support, digest, UTF-8, JSON, or validation fails.
 */
export async function verifyAndParseEvidencePayload(bytes: ArrayBuffer): Promise<EvidenceData> {
  if (bytes.byteLength !== a01EvidenceMetadata.payload.sizeBytes) throw new Error("A01 evidence byte length mismatch; immutable payload unavailable");
  if (!globalThis.crypto?.subtle) throw new Error("SHA-256 verification is unavailable in this browser context");
  const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);
  const hex = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  if (hex !== a01EvidenceMetadata.payload.sha256) throw new Error("A01 evidence SHA-256 mismatch; immutable payload rejected");
  return validateEvidenceData(JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes)));
}

/**
 * Fetch the pinned static A01 payload and pass its original bytes through verification.
 *
 * @param options - Optional cancellation signal forwarded unchanged to fetch.
 * @returns The verified, frozen payload; no fallback or synthetic evidence is used.
 * @throws For HTTP failures, fetch/cancellation failures, or failed byte/payload checks.
 */
export async function loadA01Evidence({ signal }: { signal?: AbortSignal } = {}): Promise<EvidenceData> {
  const response = await fetch(a01EvidenceMetadata.payload.url, { signal });
  if (!response.ok) throw new Error(`A01 evidence is unavailable (HTTP ${response.status})`);
  return verifyAndParseEvidencePayload(await response.arrayBuffer());
}

/**
 * Select a rank subset for display without modifying points or locked run results.
 *
 * @param points - Validated evidence points in source order.
 * @param rank - A non-negative safe integer rank, or "all" to retain every point.
 * @returns The original array for "all", otherwise matching points in input order.
 * @throws If the rank is neither "all" nor a non-negative safe integer.
 */
export function filterEvidencePoints(points: readonly EvidencePoint[], rank: number | "all"): readonly EvidencePoint[] {
  if (rank === "all") return points;
  if (!integer(rank)) throw new Error("Rank filter must be a non-negative integer or all");
  return points.filter((point) => point.rank === rank);
}

/**
 * Limit rendered points by deterministic, evenly spaced input-order indices.
 *
 * Selection uses floor(index * length / cap), starting at the first point. It is
 * a display optimization, not a statistical sample or a new analysis population;
 * the full locked statistic and stored null distribution remain unchanged.
 *
 * @param points - Validated points, optionally filtered for the current view.
 * @param cap - Positive safe integer maximum number of points to render.
 * @returns The original array when within the cap, otherwise references to cap points.
 * @throws If cap is not a positive safe integer.
 */
export function sampleEvidencePoints(points: readonly EvidencePoint[], cap: number): readonly EvidencePoint[] {
  if (!integer(cap, 1)) throw new Error("Rendering cap must be a positive integer");
  if (points.length <= cap) return points;
  return Array.from({ length: cap }, (_, index) => points[Math.floor(index * points.length / cap)]);
}

export interface NullHistogramBin { readonly min: number; readonly max: number; readonly count: number; }
/**
 * Bin finite stored null statistics into equal-width intervals for display.
 *
 * Bins include their lower edge; the final bin also includes the maximum. A
 * constant input expands the range by 0.5 on each side to give nonzero width.
 * Every input value contributes one count, without changing the nulls or deriving
 * a replacement p-value for the locked run.
 *
 * @param values - Nonempty finite statistics, normally the full stored null array.
 * @param binCount - Safe integer from 1 through 200; defaults to 24.
 * @returns Display range and ordered bin boundaries/counts.
 * @throws For empty or non-finite input, or an invalid bin count.
 */
export function buildNullHistogram(values: readonly number[], binCount = 24): { min: number; max: number; bins: readonly NullHistogramBin[] } {
  if (!values.length || values.some((value) => !Number.isFinite(value)) || !integer(binCount, 1) || binCount > 200) throw new Error("Invalid null histogram input");
  const minimum = Math.min(...values);
  const maximum = Math.max(...values);
  const min = minimum === maximum ? minimum - 0.5 : minimum;
  const max = minimum === maximum ? maximum + 0.5 : maximum;
  const width = (max - min) / binCount;
  const bins = Array.from({ length: binCount }, (_, index) => ({ min: min + index * width, max: min + (index + 1) * width, count: 0 }));
  for (const value of values) bins[Math.min(binCount - 1, Math.floor((value - min) / width))].count += 1;
  return { min, max, bins };
}
