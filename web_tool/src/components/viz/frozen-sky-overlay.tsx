import { useEffect, useRef, useState } from "react";
import { fetchPublishedSkyTable, parsePublishedSkyReleases, type PublishedSkyTable } from "@/lib/star/sky-overlay-input";
import publishedManifest from "../../../content/sky-overlay-releases.v1.json";

/** Version-pinned CDS build. HiPS/CDS requests are third-party network traffic.
 * Dataset coordinates are served read-only from the CI-verified release, never
 * from an arbitrary user-declared SHA-256 or from illustrative arithmetic data. */
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


const RELEASES = parsePublishedSkyReleases(publishedManifest);

export function FrozenSkyOverlay() {
  const [selectedId, setSelectedId] = useState<string>(RELEASES[0]?.datasetId ?? "");
  const [verified, setVerified] = useState<PublishedSkyTable | null>(null);
  const [status, setStatus] = useState<string>(
    RELEASES.length === 0
      ? "No CI-admitted observational sky releases. No astronomical markers are available for projection."
      : "Choose a CI-admitted dataset to fetch and verify its exact published coordinate bytes."
  );
  const [busy, setBusy] = useState(false);
  const [survey, setSurvey] = useState<string>(SURVEYS[0].id);
  const [visible, setVisible] = useState(true);
  const frame = useRef<HTMLDivElement>(null);
  const section = useRef<HTMLElement>(null);
  const revision = useRef(0);
  useEffect(() => { section.current?.setAttribute("data-sky-hydrated", "true"); }, []);
  const viewer = useRef<ViewerAPI | null>(null);
  const overlay = useRef<CatalogAPI | null>(null);

  function reset() {
    revision.current++;
    setVerified(null);
    viewer.current = null; overlay.current = null;
    if (frame.current) frame.current.replaceChildren();
  }
  async function loadSelected() {
    reset();
    const current = revision.current;
    const release = RELEASES.find(item => item.datasetId === selectedId);
    if (!release) { setStatus("Dataset is not admitted by the CI release manifest"); return; }
    setBusy(true);
    setStatus("Fetching the immutable reviewed coordinate release and checking SHA-256…");
    try {
      const accepted = await fetchPublishedSkyTable(release);
      if (current !== revision.current) return;
      setVerified(accepted);
      setStatus("CI-gated release coordinates and selected IDs verified against committed hashes. Display only; not independent scientific support.");
    } catch (error) {
      if (current === revision.current)
        setStatus(error instanceof Error ? error.message : "Published sky dataset verification failed");
    } finally { if (current === revision.current) setBusy(false); }
  }

  useEffect(() => {
    if (!verified || !frame.current) return;
    let disposed = false;
    loadAladin().then((A) => {
      if (disposed || !frame.current) return;
      const first = verified.sources[0];
      frame.current.replaceChildren();
      const map = A.aladin("#star-aladin-sky-viewport", {
        survey, target: String(first.ra_deg) + " " + String(first.dec_deg), fov: 1.5,
        cooFrame: "ICRS", showReticle: true, showCooGrid: true,
        showLayersControl: true, showShareControl: false,
      });
      const cat = A.catalog({ name: "CI release: " + verified.dataset_id, color: "#f59e0b", sourceSize: 8, onClick: "showTable" });
      map.addCatalog(cat);
      cat.addSources(verified.sources.map(p => A.source(p.ra_deg, p.dec_deg, { source_id: p.source_id })));
      viewer.current = map; overlay.current = cat;
    }).catch(error => { if (!disposed) setStatus(error instanceof Error ? error.message : "Aladin failed to load"); });
    return () => { disposed = true; viewer.current = null; overlay.current = null; };
  }, [verified]);

  useEffect(() => { try { viewer.current?.setImageSurvey(survey); } catch { setStatus("This external HiPS image survey is unavailable; choose DSS2."); } }, [survey]);
  useEffect(() => {
    if (!overlay.current || !verified) return;
    overlay.current.removeAll();
    if (visible) {
      const A = window.A;
      if (A) overlay.current.addSources(verified.sources.map(p => A.source(p.ra_deg, p.dec_deg, { source_id: p.source_id })));
    }
  }, [visible, verified]);

  return <section ref={section} aria-label="CI-reviewed observational sky catalogue" className="space-y-4 rounded-xl border border-border bg-surface p-5">
    <div>
      <h2 className="font-display text-xl tracking-tight">Observed sky · Aladin Lite</h2>
      <p className="mt-2 max-w-3xl text-sm leading-relaxed text-muted">
        Display-only astronomical coordinates are released through a repository CI gate. Select an approved
        dataset; the browser fetches its read-only coordinate extract and independently verifies its committed
        SHA-256 and ordered source IDs. There is no user-entered checksum or arbitrary local file upload.
        A verified display release does not establish an arithmetic correspondence, crossmatch, or physical result.
      </p>
    </div>
    <div className="grid gap-3 sm:grid-cols-2">
      <label className="text-xs text-muted">CI-admitted observational dataset
        <select aria-label="CI-admitted sky dataset" value={selectedId}
          disabled={busy || RELEASES.length === 0}
          onChange={e => { reset(); setSelectedId(e.target.value); setStatus("Choose Load after selecting an admitted dataset."); }}
          className="mt-1 block h-11 w-full rounded-md border border-border bg-elevated px-3 text-sm text-fg disabled:opacity-50">
          {RELEASES.length === 0 ? <option value="">No approved sky releases</option> :
            RELEASES.map(release => <option key={release.datasetId} value={release.datasetId}>{release.datasetId} · {release.coordinateRole}</option>)}
        </select>
      </label>
      <div className="flex items-end">
        <button type="button" onClick={() => void loadSelected()} disabled={busy || !selectedId || RELEASES.length === 0}
          className="h-11 rounded-md bg-primary px-4 text-sm font-medium text-primary-fg disabled:opacity-40">
          {busy ? "Verifying published dataset…" : "Load CI-verified sky dataset"}
        </button>
      </div>
    </div>
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
      <p className="text-xs text-muted">
        The browser retrieves only the CI-released same-origin coordinate extract. CDS Aladin and HiPS imagery
        may make independent third-party network requests. CI verifies recorded provenance and bytes, but cannot
        itself establish publisher authority or independent reviewer identity.
      </p>
    </> : null}
    <p className="text-xs text-subtle">
      No released catalogue is silently inferred from historical CSVs or source-provenance status alone.
      The admission manifest must name a reviewed transformation, exact coordinate role and full file hashes;
      a modified or missing coordinate file is rejected without plotting any positions.
      The 160 arithmetic illustration points are never astronomical coordinates.
    </p>
  </section>;
}
