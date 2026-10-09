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
