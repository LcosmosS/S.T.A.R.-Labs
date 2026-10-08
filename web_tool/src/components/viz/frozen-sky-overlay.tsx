import { useEffect, useRef, useState } from "react";
import { MAX_SKY_SOURCES, SKY_SCOPE_IDS, verifyLocalFrozenSkyTable, type FrozenSkyTable } from "@/lib/star/sky-overlay-input";

/** Version-pinned CDS build. Scripts, HiPS tiles and catalog selections are
 * third-party network requests; frozen coordinate CSV remains in the browser. */
const ALADIN_URL = "https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.1/aladin.js";
const SURVEYS = [
  { id: "P/DSS2/color", label: "DSS2 color" },
  { id: "P/SDSS9/color", label: "SDSS DR9 color" },
  { id: "CDS/P/unWISE/color-W2-W1W2-W1", label: "unWISE W1/W2" },
] as const;
type CatalogAPI = { addSources: (sources: unknown[]) => void; removeAll: () => void };
type ViewerAPI = { addCatalog: (catalog: CatalogAPI) => void; setImageSurvey: (survey: string) => void };
type AladinAPI = {
  init: Promise<unknown>;
  aladin: (selector: string, options: Record<string, unknown>) => ViewerAPI;
  catalog: (options: Record<string, unknown>) => CatalogAPI;
  source: (ra: number, dec: number, data: Record<string, string>) => unknown;
};
declare global { interface Window { A?: AladinAPI } }
let loadPromise: Promise<AladinAPI> | undefined;

function loadAladin(): Promise<AladinAPI> {
  if (typeof window === "undefined") return Promise.reject(new Error("Aladin is browser-only"));
  if (window.A) return window.A.init.then(() => window.A as AladinAPI);
  if (!loadPromise) {
    loadPromise = new Promise<AladinAPI>((resolve, reject) => {
      const script = document.createElement("script");
      script.src = ALADIN_URL; script.async = true; script.crossOrigin = "anonymous";
      script.onload = () => {
        if (!window.A) reject(new Error("CDS Aladin Lite did not initialize"));
        else window.A.init.then(() => resolve(window.A as AladinAPI), reject);
      };
      script.onerror = () => reject(new Error("Unable to load pinned Aladin Lite; check external network access"));
      document.head.appendChild(script);
    }).catch((reason) => { loadPromise = undefined; throw reason; });
  }
  return loadPromise;
}

export function FrozenSkyOverlay() {
  const [scope, setScope] = useState<string>(SKY_SCOPE_IDS[0]);
  const [expectedSha, setExpectedSha] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [verified, setVerified] = useState<FrozenSkyTable | null>(null);
  const [status, setStatus] = useState<string>("No coordinate table loaded. No simulated sky positions are displayed.");
  const [busy, setBusy] = useState(false);
  const [survey, setSurvey] = useState<string>(SURVEYS[0].id);
  const [visible, setVisible] = useState(true);
  const frame = useRef<HTMLDivElement>(null);
  const section = useRef<HTMLElement>(null);
  useEffect(() => { section.current?.setAttribute("data-sky-hydrated", "true"); }, []);
  const viewer = useRef<ViewerAPI | null>(null);
  const overlay = useRef<CatalogAPI | null>(null);

  function reset() { setVerified(null); viewer.current = null; overlay.current = null; if (frame.current) frame.current.replaceChildren(); }
  async function verifyFile() {
    reset(); setBusy(true); setStatus("Verifying exact bytes and coordinate schema…");
    try {
      if (!file) throw new Error("Choose a frozen local CSV first");
      const accepted = await verifyLocalFrozenSkyTable(file, expectedSha, scope);
      setVerified(accepted);
      setStatus(`SHA-256 verified locally for ${accepted.sources.length} user-supplied sources. This does not verify upstream astronomy provenance.`);
    } catch (error) { setStatus(error instanceof Error ? error.message : "Unknown validation failure"); }
    finally { setBusy(false); }
  }

  useEffect(() => {
    if (!verified || !frame.current) return;
    let disposed = false;
    loadAladin().then((A) => {
      if (disposed || !frame.current) return;
      const first = verified.sources[0];
      frame.current.replaceChildren();
      const map = A.aladin("#star-aladin-sky-viewport", {
        survey, target: `${first.ra_deg} ${first.dec_deg}`, fov: 1.5,
        cooFrame: "ICRS", showReticle: true, showCooGrid: true,
        showLayersControl: true, showShareControl: false,
      });
      const cat = A.catalog({ name: `Local SHA-256 checked: ${verified.dataset_id}`, color: "#f59e0b", sourceSize: 8, onClick: "showTable" });
      map.addCatalog(cat);
      cat.addSources(verified.sources.map((point) => A.source(point.ra_deg, point.dec_deg, { source_id: point.source_id })));
      viewer.current = map; overlay.current = cat;
    }).catch((error) => { if (!disposed) setStatus(error instanceof Error ? error.message : "Aladin failed to load"); });
    return () => { disposed = true; viewer.current = null; overlay.current = null; };
  }, [verified]);

  useEffect(() => { try { viewer.current?.setImageSurvey(survey); } catch { setStatus("This external HiPS image survey is unavailable; choose DSS2."); } }, [survey]);
  useEffect(() => { if (!overlay.current || !verified) return; overlay.current.removeAll(); if (visible) {
    const A = window.A; if (A) overlay.current.addSources(verified.sources.map(p => A.source(p.ra_deg, p.dec_deg, { source_id: p.source_id })));
  } }, [visible, verified]);

  return <section ref={section} aria-label="Verified local sky catalogue" className="space-y-4 rounded-xl border border-border bg-surface p-5">
    <div>
      <h2 className="font-display text-xl tracking-tight">Observed sky · Aladin Lite</h2>
      <p className="mt-2 max-w-3xl text-sm leading-relaxed text-muted">
        Separate from the conjectural elliptic-curve projection. Select a user-controlled, frozen ICRS J2000
        coordinate extract and enter its recorded SHA-256. The registered dataset identifiers are <strong>planned scopes</strong>,
        not verified source lineages. No crossmatch, inference, or ACSC evidence is produced.
      </p>
    </div>
    <div className="grid gap-3 sm:grid-cols-2">
      <label className="text-xs text-muted">Registered dataset scope
        <select aria-label="Registered dataset scope" value={scope} onChange={e => { reset(); setScope(e.target.value); }}
          className="mt-1 block h-11 w-full rounded-md border border-border bg-elevated px-3 text-sm text-fg">
          {SKY_SCOPE_IDS.map(id => <option key={id} value={id}>{id} (provenance pending)</option>)}
        </select>
      </label>
      <label className="text-xs text-muted">Frozen UTF-8 CSV (source_id,ra_deg,dec_deg; up to {MAX_SKY_SOURCES.toLocaleString()} rows)
        <input aria-label="Frozen local coordinate CSV" className="mt-1 block w-full text-sm text-fg" type="file" accept=".csv,text/csv"
          onChange={e => { reset(); setFile(e.currentTarget.files?.[0] ?? null); }} />
      </label>
      <label className="text-xs text-muted sm:col-span-2">Recorded SHA-256 of exact CSV bytes
        <input aria-label="Expected SHA-256" spellCheck={false} autoComplete="off" value={expectedSha} onChange={e => { reset(); setExpectedSha(e.target.value); }}
          placeholder="64 hexadecimal digits from the frozen-source manifest"
          className="mt-1 h-11 w-full rounded-md border border-border bg-elevated px-3 font-mono text-xs text-fg" />
      </label>
    </div>
    <button type="button" onClick={() => void verifyFile()} disabled={busy || !file}
      className="h-11 rounded-md bg-primary px-4 text-sm font-medium text-primary-fg disabled:opacity-40">
      {busy ? "Checking local file…" : "Verify bytes and display on sky"}
    </button>
    <p role="status" aria-live="polite" className="text-xs text-muted">{status}</p>
    {verified ? <>
      <div className="flex flex-wrap items-end gap-3">
        <label className="text-xs text-muted">Survey imagery
          <select aria-label="Background sky survey" className="mt-1 block h-11 rounded-md border border-border bg-elevated px-3 text-sm text-fg"
            value={survey} onChange={e => setSurvey(e.target.value)}>
            {SURVEYS.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
          </select>
        </label>
        <label className="flex h-11 items-center gap-2 text-xs text-muted">
          <input aria-label="Show verified coordinate overlay" type="checkbox" checked={visible} onChange={e => setVisible(e.target.checked)} />
          Show coordinate overlay
        </label>
        <span className="font-mono text-xs text-muted">{verified.sources.length} positions · {verified.sha256.slice(0,12)}…</span>
      </div>
      <div id="star-aladin-sky-viewport" ref={frame} className="h-[360px] w-full overflow-hidden rounded-lg border border-border sm:h-[480px]" aria-label="Aladin Lite ICRS sky viewer" />
      <p className="text-xs text-muted">The source CSV is never sent to S.T.A.R. Labs. Display uses CDS Aladin/HiPS network requests; coordinates and selected fields can be sent to the external map service as part of normal map use. The file hash certifies local bytes only, not identification or scientific eligibility.</p>
    </> : null}
    <p className="text-xs text-subtle">Expected exact header: <code>source_id,ra_deg,dec_deg</code>. Plain decimal degrees, ICRS/J2000, unique safe IDs, no rounding, missing values, clipping, reordering or silent deduplication. No markers appear unless every row and the exact SHA-256 pass. This viewer never displays the 160 arithmetic illustration points as sky coordinates.</p>
  </section>;
}
