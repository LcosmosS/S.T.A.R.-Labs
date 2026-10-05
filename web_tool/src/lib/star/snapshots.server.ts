import { createHash, randomUUID } from "node:crypto";
import { DEMO_VERSION, snapshotInputSchema, type DemoSnapshot } from "./snapshots";

const headers = { "Cache-Control": "no-store", "Content-Type": "application/json" };
export function json(value: unknown, status = 200) { return new Response(JSON.stringify(value), { status, headers }); }
type SnapshotRow = { id: string; created_at: Date | string; demo_version: string; state: DemoSnapshot["state"]; checksum: string };
function snapshot(row: SnapshotRow): DemoSnapshot {
  return { id: row.id, createdAt: new Date(row.created_at).toISOString(), demoVersion: row.demo_version, state: row.state, checksum: row.checksum };
}
async function storage() {
  if (process.env.VERCEL && !process.env.DATABASE_URL?.trim()) throw new Error("Durable storage is not configured");
  const { dbSource, getSql } = await import("../db");
  return { sql: await getSql(), storage: dbSource === "neon" ? "neon" as const : "local" as const, durable: dbSource === "neon" };
}
export async function health() {
  try {
    const db = await storage();
    await db.sql.query("select id from starmap_demo_snapshots limit 0");
    await db.sql.query("select day from starmap_demo_budget limit 0");
    return json({ status: "ok", storage: db.storage, durable: db.durable, demoVersion: DEMO_VERSION });
  } catch { return json({ status: "unavailable", error: "Notebook storage is unavailable. The illustrative lab remains usable." }, 503); }
}
export async function listSnapshots() {
  try {
    const db = await storage();
    const rows = await db.sql.query<SnapshotRow>("select * from starmap_demo_snapshots order by created_at desc, id desc limit 20");
    return json({ snapshots: rows.map(snapshot), storage: db.storage, durable: db.durable });
  } catch { return json({ error: "Notebook storage is unavailable. Try again later." }, 503); }
}
export async function getSnapshot(id: string) {
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id)) return json({ error: "Invalid snapshot ID." }, 400);
  try {
    const { sql } = await storage();
    const rows = await sql.query<SnapshotRow>("select * from starmap_demo_snapshots where id = $1", [id]);
    return rows[0] ? json({ snapshot: snapshot(rows[0]) }) : json({ error: "Snapshot not found." }, 404);
  } catch { return json({ error: "Notebook storage is unavailable. Try again later." }, 503); }
}
export async function saveSnapshot(request: Request) {
  if (!request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) return json({ error: "Send a JSON demo configuration." }, 415);
  const reader = request.body?.getReader();
  if (!reader) return json({ error: "A demo configuration is required." }, 400);
  const chunks: Uint8Array[] = []; let size = 0;
  while (true) {
    const { done, value } = await reader.read(); if (done) break;
    size += value.byteLength;
    if (size > 4096) { await reader.cancel(); return json({ error: "Configuration exceeds 4 KB." }, 413); }
    chunks.push(value);
  }
  let input;
  try {
    const bytes = new Uint8Array(size); let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
    input = snapshotInputSchema.parse(JSON.parse(new TextDecoder().decode(bytes)));
  } catch { return json({ error: "Invalid demo configuration or unsupported version." }, 400); }
  const checksum = createHash("sha256").update(JSON.stringify(input)).digest("hex");
  try {
    const { sql } = await storage();
    const existing = await sql.query<SnapshotRow>("select * from starmap_demo_snapshots where checksum = $1", [checksum]);
    if (existing[0]) return json({ snapshot: snapshot(existing[0]) });
    // Atomic shared prototype budget; no visitor identifiers are stored.
    const rows = await sql.query<SnapshotRow>(`
      with admitted as (
        insert into starmap_demo_budget (day, used) values (current_date, 1)
        on conflict (day) do update set used = starmap_demo_budget.used + 1
        where starmap_demo_budget.used < 200 returning day
      )
      insert into starmap_demo_snapshots (id, demo_version, state, checksum)
      select $1, $2, $3::jsonb, $4 from admitted
      on conflict (checksum) do nothing returning *`,
      [randomUUID(), DEMO_VERSION, JSON.stringify(input.state), checksum]);
    if (rows[0]) return json({ snapshot: snapshot(rows[0]) }, 201);
    const raced = await sql.query<SnapshotRow>("select * from starmap_demo_snapshots where checksum = $1", [checksum]);
    return raced[0] ? json({ snapshot: snapshot(raced[0]) }) : json({ error: "Today's prototype save limit has been reached. Export your settings and try again tomorrow." }, 429);
  } catch { return json({ error: "Notebook storage is unavailable. Your settings have not been saved." }, 503); }
}
