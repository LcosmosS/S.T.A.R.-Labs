import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { Check, Copy, Download, LoaderCircle, NotebookPen, RefreshCw, Save } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { MAPPING_META } from "@/lib/star/physics";
import { useLab } from "@/lib/star/store";
import {
  captureSnapshotState,
  DEMO_VERSION,
  type DemoSnapshot,
  type SnapshotState,
} from "@/lib/star/snapshots";

export const Route = createFileRoute("/notebook")({
  validateSearch: (search: Record<string, unknown>): { snapshot?: string } => ({
    snapshot: typeof search.snapshot === "string" ? search.snapshot.slice(0, 128) : undefined,
  }),
  component: NotebookPage,
});

type SnapshotList = { snapshots: DemoSnapshot[]; storage: "neon" | "local"; durable: boolean };

async function requestJson<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(path, options);
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body?.error === "string" ? body.error : `Request failed (${response.status}).`;
    throw new Error(detail);
  }
  if (!body) throw new Error("The server returned an unreadable response. Please retry.");
  return body as T;
}

function messageFrom(error: unknown) {
  return error instanceof Error ? error.message : "The request could not complete. Please retry.";
}

function StateSummary({ state }: { state: SnapshotState }) {
  const fields = [
    ["Projection", MAPPING_META[state.mappingFamily].short],
    ["Catalog filter", state.provenance],
    ["Selected fixture", state.selectedLabel ?? "None"],
    ["Color by", state.colorMode],
    ["Redshift z", state.z.toFixed(2)],
    ["Topology / conformal", `${state.topologyOn ? "On" : "Off"} / ${state.conformalOn ? "On" : "Off"}`],
    ["λQ / βQ", `${state.lambdaQ.toFixed(2)} / ${state.betaQ.toFixed(2)}`],
    ["Winding u / v", `${state.windingU} / ${state.windingV}`],
  ];
  return (
    <dl className="grid gap-x-6 gap-y-4 sm:grid-cols-2">
      {fields.map(([label, value]) => (
        <div key={label} className="min-w-0">
          <dt className="font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">{label}</dt>
          <dd className="mt-1 break-words text-sm text-fg">{value}</dd>
        </div>
      ))}
    </dl>
  );
}

function NotebookPage() {
  const lab = useLab();
  const { snapshot: sharedId } = Route.useSearch();
  const [snapshots, setSnapshots] = useState<DemoSnapshot[]>([]);
  const [selected, setSelected] = useState<DemoSnapshot | null>(null);
  const [storage, setStorage] = useState<Pick<SnapshotList, "storage" | "durable"> | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [shareUrl, setShareUrl] = useState("");
  const shareInput = useRef<HTMLInputElement>(null);
  const current = captureSnapshotState(lab);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError("");
    requestJson<SnapshotList>("/api/snapshots", { signal: controller.signal })
      .then((data) => {
        setSnapshots(data.snapshots);
        setStorage({ storage: data.storage, durable: data.durable });
      })
      .catch((err: unknown) => {
        if (!controller.signal.aborted) {
          setStorage(null);
          setError(messageFrom(err));
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [refresh]);

  useEffect(() => {
    if (!sharedId) return;
    const controller = new AbortController();
    setSelected(null);
    setNotice("Loading the shared snapshot…");
    requestJson<{ snapshot: DemoSnapshot }>(`/api/snapshots/${encodeURIComponent(sharedId)}`, {
      signal: controller.signal,
    })
      .then(({ snapshot }) => {
        setSelected(snapshot);
        setNotice("Shared snapshot loaded. Review its settings, then restore it to the Deck.");
      })
      .catch((err: unknown) => {
        if (!controller.signal.aborted) {
          setNotice("");
          setError(messageFrom(err));
        }
      });
    return () => controller.abort();
  }, [sharedId]);

  useEffect(() => {
    if (!selected) {
      setShareUrl("");
      return;
    }
    const url = new URL("/notebook", window.location.origin);
    url.searchParams.set("snapshot", selected.id);
    setShareUrl(url.toString());
  }, [selected]);

  async function saveSnapshot() {
    setSaving(true);
    setError("");
    setNotice("");
    try {
      const { snapshot } = await requestJson<{ snapshot: DemoSnapshot }>("/api/snapshots", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ demoVersion: DEMO_VERSION, state: captureSnapshotState(useLab.getState()) }),
      });
      setSelected(snapshot);
      setSnapshots((items) => [snapshot, ...items.filter((item) => item.id !== snapshot.id)].slice(0, 20));
      setNotice("Configuration saved. Review or share this snapshot below.");
    } catch (err) {
      setError(messageFrom(err));
    } finally {
      setSaving(false);
    }
  }

  function restoreSnapshot() {
    if (!selected) return;
    setError("");
    try {
      useLab.getState().set(captureSnapshotState(selected.state));
      setNotice("Snapshot restored. Open the Deck to explore these settings.");
    } catch (err) {
      setError(messageFrom(err));
    }
  }

  function exportConfiguration() {
    setError("");
    try {
      const contents = {
        demoVersion: DEMO_VERSION,
        evidenceStatus: "illustrative-only",
        state: captureSnapshotState(useLab.getState()),
      };
      const url = URL.createObjectURL(new Blob([JSON.stringify(contents, null, 2) + "\n"], { type: "application/json" }));
      const link = document.createElement("a");
      link.href = url;
      link.download = "starmap-demo-configuration.json";
      link.click();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
      setNotice("Current demo configuration exported as JSON.");
    } catch (err) {
      setError(messageFrom(err));
    }
  }

  async function copyShareLink() {
    if (!shareUrl) return;
    setError("");
    try {
      if (!navigator.clipboard?.writeText) {
        shareInput.current?.focus();
        shareInput.current?.select();
        setNotice("Share link selected. Copy it using your device’s copy command.");
        return;
      }
      await navigator.clipboard.writeText(shareUrl);
      setNotice("Share link copied.");
    } catch {
      shareInput.current?.focus();
      shareInput.current?.select();
      setNotice("Clipboard access was unavailable. The selected share link can be copied manually.");
    }
  }

  return (
    <div className="space-y-8">
      <header className="max-w-2xl">
        <Badge tone="steel"><NotebookPen className="mr-1.5 size-3" /> Demo notebook</Badge>
        <h1 className="mt-3 font-display text-4xl tracking-tight">Keep a configuration. Share an exploration.</h1>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          Save the Deck’s current projection, filters, and model controls. Each public snapshot can be restored on
          another device. Snapshots contain only bounded demo settings, with no names, notes, or personal data.
        </p>
      </header>

      <div className="rounded-lg border border-warn/25 bg-warn/5 p-4 text-sm leading-relaxed text-muted">
        <span className="font-medium text-warn">Illustrative configurations only.</span>{" "}
        Saving or restoring a snapshot does not run a preregistered experiment, create scientific evidence, or
        change an execution gate. The browser uses the same fixed demonstration catalog for every snapshot.
      </div>

      <div className="flex flex-wrap items-center gap-x-3 gap-y-2 text-xs text-muted">
        <Badge tone={storage?.durable ? "ok" : "default"}>
          {loading ? "Connecting" : storage?.durable ? "Neon connected" : storage ? "Local preview" : "Storage unavailable"}
        </Badge>
        <span>
          {storage?.durable
            ? "Public, append-only storage. Saved links persist across sessions."
            : storage
              ? "Local preview storage may reset. Export JSON to keep a copy."
              : "Export remains available while shared storage is unavailable."}
        </span>
        <span className="font-mono text-[10px] text-subtle">{DEMO_VERSION}</span>
      </div>

      <div aria-live="polite" aria-atomic="true">
        {error ? <p role="alert" className="rounded-lg bg-danger/10 p-4 text-sm text-danger">{error}</p> : null}
        {notice ? <p className="mt-2 flex items-start gap-2 text-sm text-steel"><Check className="mt-0.5 size-4 shrink-0" />{notice}</p> : null}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section aria-labelledby="current-settings" className="rounded-xl bg-surface p-5 shadow-[var(--shadow-border)] sm:p-6">
          <div className="mb-5 flex items-center justify-between gap-3">
            <h2 id="current-settings" className="font-display text-2xl tracking-tight">Current configuration</h2>
            <Link to="/" className="text-xs text-steel underline-offset-4 hover:underline">Edit on Deck</Link>
          </div>
          <StateSummary state={current} />
          <div className="mt-6 flex flex-wrap gap-2">
            <Button type="button" onClick={saveSnapshot} disabled={saving || loading || !storage}>
              {saving ? <LoaderCircle className="animate-spin" /> : <Save />}
              {saving ? "Saving…" : "Save snapshot"}
            </Button>
            <Button type="button" variant="secondary" onClick={exportConfiguration}><Download /> Export JSON</Button>
          </div>
          <p className="mt-3 text-xs leading-relaxed text-muted">
            Saved configurations are public and cannot be edited or deleted through this prototype.
            Export includes every demo control; the summary above shows the main settings.
          </p>
        </section>

        <section aria-labelledby="selected-snapshot" className="min-w-0 rounded-xl bg-surface p-5 shadow-[var(--shadow-border)] sm:p-6">
          <h2 id="selected-snapshot" className="font-display text-2xl tracking-tight">Review a snapshot</h2>
          {selected ? (
            <>
              <p className="mt-2 break-all font-mono text-[11px] text-muted">{selected.id}</p>
              <p className="mb-5 mt-1 text-xs text-subtle">Saved {new Date(selected.createdAt).toLocaleString()} · {selected.demoVersion}</p>
              <StateSummary state={selected.state} />
              <div className="mt-6 flex flex-wrap gap-2">
                <Button type="button" onClick={restoreSnapshot}>Restore settings</Button>
                <Button asChild variant="secondary"><Link to="/">Open Deck</Link></Button>
              </div>
              <label htmlFor="snapshot-share-link" className="mt-5 block font-mono text-[10px] uppercase tracking-[0.14em] text-subtle">Public share link</label>
              <div className="mt-2 flex min-w-0 flex-col gap-2 sm:flex-row">
                <input
                  ref={shareInput}
                  id="snapshot-share-link"
                  readOnly
                  value={shareUrl}
                  onFocus={(event) => event.currentTarget.select()}
                  className="h-11 min-w-0 flex-1 rounded-md border border-border bg-elevated px-3 text-xs text-fg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/70"
                />
                <Button type="button" variant="outline" onClick={copyShareLink} disabled={!shareUrl}><Copy /> Copy</Button>
              </div>
              <p className="mt-3 break-all font-mono text-[10px] leading-relaxed text-subtle">Configuration checksum: {selected.checksum}</p>
            </>
          ) : (
            <div className="mt-6 rounded-lg border border-dashed border-border p-6 text-sm leading-relaxed text-muted">
              Save your current settings or choose a recent snapshot below. Review its controls before restoring.
            </div>
          )}
        </section>
      </div>

      <section aria-labelledby="recent-snapshots">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 id="recent-snapshots" className="font-display text-2xl tracking-tight">Recent public snapshots</h2>
            <p className="mt-1 text-xs text-muted">The 20 most recent configurations from this prototype.</p>
          </div>
          <Button type="button" variant="outline" onClick={() => setRefresh((value) => value + 1)} disabled={loading}>
            <RefreshCw className={loading ? "animate-spin" : undefined} /> Refresh
          </Button>
        </div>
        {loading ? (
          <p className="py-6 text-sm text-muted">Loading snapshots…</p>
        ) : snapshots.length ? (
          <ul className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
            {snapshots.map((snapshot) => (
              <li key={snapshot.id}>
                <button
                  type="button"
                  aria-pressed={selected?.id === snapshot.id}
                  onClick={() => { setSelected(snapshot); setError(""); setNotice("Snapshot selected. Review its settings above."); }}
                  className={`h-full w-full rounded-lg border p-4 text-left transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/70 ${selected?.id === snapshot.id ? "border-steel bg-elevated" : "border-border bg-surface hover:bg-elevated"}`}
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="text-sm font-medium text-fg">{MAPPING_META[snapshot.state.mappingFamily].short}</span>
                    <Badge>{snapshot.state.provenance}</Badge>
                  </div>
                  <p className="mt-2 text-xs text-muted">{snapshot.state.selectedLabel ?? "No selected fixture"} · z = {snapshot.state.z.toFixed(2)}</p>
                  <p className="mt-2 text-xs text-subtle">{new Date(snapshot.createdAt).toLocaleString()}</p>
                  <p className="mt-2 break-all font-mono text-[10px] text-subtle">{snapshot.id}</p>
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p className="rounded-lg bg-surface p-5 text-sm leading-relaxed text-muted">
            {storage ? "No snapshots yet. Save the first configuration from the Deck." : "Shared snapshots are currently unavailable. Refresh to retry."}
          </p>
        )}
      </section>
    </div>
  );
}
