/** Local, byte-hash-verified sky positions, never an inference-ready galaxy join.
 * The dataset IDs below are already registered but NOT scientifically validated.
 * Frozen extracts are user-selected; their exact bytes must match a declared
 * SHA-256. Upstream provenance is a separate registry gate.
 */
export const SKY_SCOPE_IDS = ["DATA-SDSS18-200K", "DATA-MANGA-HI-ALL"] as const;
export type SkyScope = (typeof SKY_SCOPE_IDS)[number];
export type SkySource = { source_id: string; ra_deg: number; dec_deg: number };
export type FrozenSkyTable = {
  dataset_id: SkyScope;
  sha256: string;
  sources: SkySource[];
  file_name: string;
};
export const MAX_SKY_TABLE_BYTES = 1_000_000;
export const MAX_SKY_SOURCES = 2000;
const EXACT_COLUMNS = "source_id,ra_deg,dec_deg";
const SAFE_ID = /^[A-Za-z0-9_.:-]{1,96}$/;
const NUMBER = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/;

export function validateScope(scope: string): SkyScope {
  if (!SKY_SCOPE_IDS.some((s) => s === scope)) throw new Error("Unregistered dataset scope; a new scope needs separate canonical review");
  return scope as SkyScope;
}
export function validateSha256(value: string): string {
  const digest = value.trim().toLowerCase();
  if (!/^[0-9a-f]{64}$/.test(digest)) throw new Error("Expected SHA-256 must contain exactly 64 hexadecimal digits");
  return digest;
}
export function parseFrozenSkyCSV(text: string): SkySource[] {
  const lines = text.replace(/^\uFEFF/, "").split(/\r\n|\n|\r/);
  if (lines.at(-1) === "") lines.pop();
  if (lines.shift() !== EXACT_COLUMNS) throw new Error("Expected exactly source_id,ra_deg,dec_deg in that order");
  if (lines.length < 1 || lines.length > MAX_SKY_SOURCES) throw new Error("Frozen source count must be between 1 and 2,000");
  const seen = new Set<string>();
  return lines.map((line, index) => {
    const cells = line.split(",");
    if (cells.length !== 3) throw new Error(`Line ${index + 2}: expected three plain, unquoted CSV columns`);
    const [source_id, ra, dec] = cells;
    if (!source_id || !SAFE_ID.test(source_id)) throw new Error(`Line ${index + 2}: invalid source_id`);
    if (seen.has(source_id)) throw new Error(`Line ${index + 2}: duplicate source_id; refuse silent deduplication`);
    if (!ra || !dec || !NUMBER.test(ra) || !NUMBER.test(dec)) throw new Error(`Line ${index + 2}: invalid decimal-degree coordinates`);
    const ra_deg = Number(ra), dec_deg = Number(dec);
    if (!Number.isFinite(ra_deg) || !Number.isFinite(dec_deg) || ra_deg < 0 || ra_deg >= 360 || dec_deg < -90 || dec_deg > 90)
      throw new Error(`Line ${index + 2}: RA/Dec outside ICRS degree bounds`);
    seen.add(source_id);
    return { source_id, ra_deg, dec_deg };
  });
}
export async function verifyLocalFrozenSkyTable(file: File, expectedSha: string, scope: string): Promise<FrozenSkyTable> {
  const dataset_id = validateScope(scope);
  const declared = validateSha256(expectedSha);
  if (file.size < 1 || file.size > MAX_SKY_TABLE_BYTES) throw new Error("Frozen CSV must be nonempty and no larger than 1 MB");
  if (!file.name.toLowerCase().endsWith(".csv")) throw new Error("Only frozen UTF-8 .csv files are accepted");
  if (!globalThis.crypto?.subtle) throw new Error("Secure browser context with Web Crypto is required");
  const bytes = await file.arrayBuffer();
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  const actual = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  if (actual !== declared) throw new Error("SHA-256 mismatch; refusing to render any unverified coordinates");
  const text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  const sources = parseFrozenSkyCSV(text);
  return { dataset_id, sha256: actual, sources, file_name: file.name };
}


/** CI-admitted observational display releases. The site does not mint or approve
 * releases: the exact imported manifest must first pass sky:check on the build
 * commit. The browser independently checks the exact served coordinate bytes.
 * Neither gate constitutes independent scientific review or physical support.
 */
export type PublishedSkyRelease = {
  datasetId: string;
  qualifiedDatasetId: string;
  coordinatePath: string;
  coordinateSha256: string;
  selectedIdsSha256: string;
  coordinateRole: "sdss_position" | "hi_centroid" | "optical_counterpart";
  sourceSha256: string;
  reviewSha256: string;
  sourceRows: number;
  controlledSupportEligible?: boolean;
  physicalSupportEligible?: boolean;
};
export type PublishedSkyTable = {
  dataset_id: string;
  sha256: string;
  sources: SkySource[];
  coordinate_role: PublishedSkyRelease["coordinateRole"];
};
const RELEASE_SHA = /^[0-9a-f]{64}$/;
const RELEASE_ID = /^[A-Za-z0-9_.:-]{1,96}$/;
const RELEASE_PATH = "web_tool/public/sky/";

export function parsePublishedSkyReleases(manifest: unknown): PublishedSkyRelease[] {
  if (typeof manifest !== "object" || manifest === null || Array.isArray(manifest))
    throw new Error("Invalid CI release manifest");
  const data = manifest as Record<string, unknown>;
  if (data.schemaVersion !== "star-sky-overlay-releases-v1" || !Array.isArray(data.sources) || data.sources.length > 32)
    throw new Error("Invalid CI release manifest version or source count");
  const seen = new Set<string>();
  return data.sources.map((untrusted: unknown) => {
    if (typeof untrusted !== "object" || untrusted === null || Array.isArray(untrusted))
      throw new Error("Invalid sky release entry");
    const r = untrusted as Record<string, unknown>;
    const id = r.datasetId;
    if (typeof id !== "string" || !RELEASE_ID.test(id) || seen.has(id) ||
        r.qualifiedDatasetId !== "REPO-CSV-v0.2:" + id)
      throw new Error("Unregistered, duplicated or unqualified sky release");
    seen.add(id);
    for (const k of ["coordinateSha256", "selectedIdsSha256", "sourceSha256", "reviewSha256"])
      if (typeof r[k] !== "string" || !RELEASE_SHA.test(r[k] as string))
        throw new Error("Invalid CI release checksum");
    const p = r.coordinatePath;
    if (typeof p !== "string" || !p.startsWith(RELEASE_PATH) ||
        p.includes("\\") || p.includes("//") ||
        p.slice(RELEASE_PATH.length).split("/").some(v => !v || v === "." || v === ".." || !/^[A-Za-z0-9_.-]+$/.test(v)))
      throw new Error("Unsafe CI release coordinate path");
    if (!["sdss_position", "hi_centroid", "optical_counterpart"].includes(r.coordinateRole as string) ||
        typeof r.sourceRows !== "number" || !Number.isInteger(r.sourceRows) || r.sourceRows < 1 ||
        r.controlledSupportEligible === true || r.physicalSupportEligible === true)
      throw new Error("Unsupported sky release coordinate role, count or promotion");
    return r as PublishedSkyRelease;
  });
}

async function shaHex(bytes: BufferSource): Promise<string> {
  if (!globalThis.crypto?.subtle) throw new Error("Web Crypto requires a secure browser context");
  return Array.from(new Uint8Array(await globalThis.crypto.subtle.digest("SHA-256", bytes)),
    b => b.toString(16).padStart(2, "0")).join("");
}

export async function verifyPublishedSkyBytes(release: PublishedSkyRelease, input: Uint8Array): Promise<PublishedSkyTable> {
  if (input.byteLength < 1 || input.byteLength > MAX_SKY_TABLE_BYTES)
    throw new Error("CI coordinate release is empty or exceeds the 1 MB limit");
  // Reject malformed or substituted bytes before parsing or showing any markers.
  const bytes = new Uint8Array(input);
  const actual = await shaHex(bytes);
  if (actual !== release.coordinateSha256) throw new Error("Published sky coordinate SHA-256 mismatch");
  const text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  const sources = parseFrozenSkyCSV(text);
  const ids = new TextEncoder().encode(sources.map(s => s.source_id).join("\n") + "\n");
  if (await shaHex(ids) !== release.selectedIdsSha256)
    throw new Error("Published sky selected-ID chain mismatch");
  return { dataset_id: release.datasetId, sha256: actual, sources, coordinate_role: release.coordinateRole };
}

export async function fetchPublishedSkyTable(
  release: PublishedSkyRelease, fetcher: typeof fetch = fetch,
): Promise<PublishedSkyTable> {
  // Exactly the path approved by CI, with same-origin/no-redirect transport.
  const relative = release.coordinatePath.slice(RELEASE_PATH.length);
  if (!relative || !/^[A-Za-z0-9_.\/-]+$/.test(relative) ||
      relative.split("/").some(v => !v || v === "." || v === ".."))
    throw new Error("Unsafe published sky path");
  const response = await fetcher("/sky/" + relative, {
    cache: "no-store", credentials: "omit", mode: "same-origin", redirect: "error",
  });
  if (!response.ok || response.redirected || response.type === "opaque")
    throw new Error("CI sky release is unavailable or redirected");
  const declaredLength = response.headers.get("content-length");
  if (declaredLength !== null && (Number(declaredLength) > MAX_SKY_TABLE_BYTES || !/^\d+$/.test(declaredLength)))
    throw new Error("CI sky release exceeds size limit");
  if (!response.body) throw new Error("CI sky release has no readable body");
  const reader = response.body.getReader();
  const parts: Uint8Array[] = [];
  let size = 0;
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > MAX_SKY_TABLE_BYTES) throw new Error("CI sky release exceeds size limit");
      parts.push(value);
    }
  } finally { reader.releaseLock(); }
  const bytes = new Uint8Array(size);
  let offset = 0;
  for (const part of parts) { bytes.set(part, offset); offset += part.byteLength; }
  return verifyPublishedSkyBytes(release, bytes);
}
