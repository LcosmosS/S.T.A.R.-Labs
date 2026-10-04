-- Public, append-only, nonpersonal illustrative configurations. No research results.
CREATE TABLE starmap_demo_snapshots (
  id uuid PRIMARY KEY,
  created_at timestamptz NOT NULL DEFAULT now(),
  demo_version text NOT NULL CHECK (demo_version = 'starmap-illustrative-v1'),
  state jsonb NOT NULL CHECK (jsonb_typeof(state) = 'object' AND octet_length(state::text) <= 4096),
  checksum text NOT NULL UNIQUE CHECK (checksum ~ '^[0-9a-f]{64}$')
);
CREATE INDEX starmap_demo_snapshots_recent ON starmap_demo_snapshots (created_at DESC);
CREATE TABLE starmap_demo_budget (day date PRIMARY KEY, used integer NOT NULL CHECK (used BETWEEN 1 AND 200));
