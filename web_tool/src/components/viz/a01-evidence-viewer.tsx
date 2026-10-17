import { memo, useEffect, useMemo, useState } from "react";
import {
  a01EvidenceMetadata as metadata,
  filterEvidencePoints,
  loadA01Evidence,
  sampleEvidencePoints,
  type EvidenceData,
  type EvidencePoint,
} from "@/lib/star/a01-evidence";
import styles from "./a01-evidence-viewer.module.css";

const RENDER_CAP = 4_000;
const number = (value: number) => value.toLocaleString("en-US");

/** Read-only visual specification: the saved arithmetic base coordinates are
 * plotted on linear, equally spaced degree axes, with elevation in the selected
 * record. Rendering samples never enter the saved, full-cohort inference. The
 * 999 saved null values share a T axis with the observed statistic; a separately
 * labeled detail view expands only the null range. No endpoint is executed here. */
export function A01EvidenceViewer() {
  const [data, setData] = useState<EvidenceData | null>(null);
  const [error, setError] = useState("");
  const [rank, setRank] = useState<number | "all">("all");
  const [query, setQuery] = useState("");
  const [selectedLabel, setSelectedLabel] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    void loadA01Evidence({ signal: controller.signal })
      .then((loaded) => {
        if (controller.signal.aborted) return;
        setData(loaded);
        setSelectedLabel(loaded.points[0]?.label ?? "");
      })
      .catch((reason: unknown) => {
        if (!controller.signal.aborted)
          setError(
            reason instanceof Error
              ? reason.message
              : "Evidence verification failed",
          );
      });
    return () => controller.abort();
  }, []);

  const filtered = useMemo(
    () => (data ? filterEvidencePoints(data.points, rank) : []),
    [data, rank],
  );
  const sampled = useMemo(
    () => sampleEvidencePoints(filtered, RENDER_CAP),
    [filtered],
  );
  const choices = useMemo(() => {
    const term = query.trim().toLowerCase();
    return term
      ? filtered.filter((point) => point.label.toLowerCase().includes(term))
      : filtered;
  }, [filtered, query]);
  const ranks = useMemo(
    () =>
      data
        ? [...new Set(data.points.map((point) => point.rank))].sort(
            (a, b) => a - b,
          )
        : [],
    [data],
  );
  const selected = useMemo(
    () => filtered.find((point) => point.label === selectedLabel),
    [filtered, selectedLabel],
  );
  const choiceOptions = useMemo(
    () =>
      choices.map((point) => (
        <option key={point.label} value={point.label}>
          {point.label} · rank {point.rank} · N {point.conductor}
        </option>
      )),
    [choices],
  );

  function changeRank(value: string) {
    const next = value === "all" ? "all" : Number(value);
    setRank(next);
    setQuery("");
    const nextPoints = data ? filterEvidencePoints(data.points, next) : [];
    if (!nextPoints.some((point) => point.label === selectedLabel))
      setSelectedLabel(nextPoints[0]?.label ?? "");
  }

  return (
    <section
      className={styles.viewer}
      aria-label="EXP-MAP-A01 primary execution evidence"
      data-testid="a01-evidence-viewer"
    >
      <header className={styles.introduction}>
        <p className={styles.eyebrow}>
          Read-only primary execution · EXP-MAP-A01
        </p>
        <h2>A01 arithmetic projection evidence</h2>
        <p>
          Inspect the saved primary execution against the locked arithmetic
          rank-permutation <strong>NULL-MAP-001</strong>. These are arithmetic
          coordinates of elliptic curves, not observed sky locations.
        </p>
        <p className={styles.boundary}>
          No independent replication. No ACSC physical support. No controlled or
          physical support eligibility promotion.
        </p>
      </header>

      {error ? (
        <div role="alert" className={styles.failure}>
          <h3>A01 evidence unavailable</h3>
          <p>{error}</p>
          <p>
            The immutable data could not be verified. No evidence points or
            inference are displayed.
          </p>
        </div>
      ) : !data ? (
        <p role="status" aria-live="polite">
          Loading and verifying immutable A01 evidence…
        </p>
      ) : (
        <>
          <section
            className={styles.result}
            aria-label="Locked full-cohort result"
          >
            <h3>Locked full-cohort result</h3>
            <dl className={styles.metrics}>
              <div>
                <dt>Observed statistic T</dt>
                <dd data-testid="a01-observed-statistic">
                  {String(data.summary.observed_statistic)}
                </dd>
              </div>
              <div>
                <dt>Null exceedances</dt>
                <dd>
                  {data.summary.null_exceedances}/
                  {data.summary.null_realizations}
                </dd>
              </div>
              <div>
                <dt>One-sided p</dt>
                <dd>{String(data.summary.p_value)}</dd>
              </div>
              <div>
                <dt>Locked alpha</dt>
                <dd>{String(data.summary.alpha)}</dd>
              </div>
            </dl>
            <p>
              {number(data.summary.analysis_rows)} isogeny-class representatives
              from {number(data.summary.source_rows)} source rows; k ={" "}
              {data.summary.neighbor_k},{" "}
              {number(data.summary.undirected_edge_count)} undirected edges.
              Larger T is more extreme. The plus-one Monte Carlo value is p = (0
              + 1)/(999 + 1) = 0.001, below alpha = 0.01.
            </p>
            <p>
              <strong>
                Rejects only the locked arithmetic rank-permutation
                NULL-MAP-001.
              </strong>
            </p>
            <p>
              These saved statistics always use the complete locked analysis
              cohort. Display filters, selection, and rendering samples do not
              recalculate them.
            </p>
          </section>

          <section
            className={styles.projection}
            aria-label="Saved arithmetic coordinates"
          >
            <div className={styles.sectionHeader}>
              <h3>Saved arithmetic coordinates</h3>
              <p>
                Linear longitude and latitude from the locked logarithmic
                arithmetic map; equal spacing per degree. Elevation is rank ×
                200 and appears in the selected record. No geographic wrapping,
                sky crossmatch, or coordinate recomputation.
              </p>
              <p>
                The saved longitude range extends above 360°. The fixed axes
                (0–480° longitude, 0–180° latitude) cover all saved values
                without clipping.
              </p>
            </div>
            <div className={styles.controls}>
              <label>
                Rank filter
                <select
                  aria-label="Rank filter"
                  value={rank}
                  onChange={(event) => changeRank(event.target.value)}
                >
                  <option value="all">All ranks</option>
                  {ranks.map((value) => (
                    <option key={value} value={value}>
                      Rank {value}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Find curve label
                <input
                  aria-label="Find curve label"
                  type="search"
                  value={query}
                  placeholder="For example, 11a1"
                  onChange={(event) => setQuery(event.target.value)}
                />
              </label>
            </div>
            <p
              className={styles.rendering}
              data-testid="a01-rendering-count"
              data-rendered-count={sampled.length}
              data-filtered-count={filtered.length}
            >
              Showing {number(sampled.length)} of {number(filtered.length)}{" "}
              rank-filtered representatives
              {filtered.length > RENDER_CAP
                ? ` (deterministic rendering cap ${number(RENDER_CAP)})`
                : " (all filtered points)"}
              . This is a rendering optimization only, not an analysis sample. A
              selected curve is additionally marked at its saved coordinates.
            </p>
            <div className={styles.chartScroll}>
              <ArithmeticPlot
                points={sampled}
                selected={selected}
                onSelect={setSelectedLabel}
              />
            </div>
            <p className={styles.chartNote}>
              Click a plotted point or use the searchable curve selector below.
              All filtered representatives remain selectable, including those
              outside the rendering cap. Charts scroll horizontally on narrow
              screens.
            </p>

            <div className={styles.selectionGrid}>
              <label className={styles.curveSelector}>
                Select evidence curve
                <select
                  aria-label="Select evidence curve"
                  size={5}
                  value={
                    choices.some((point) => point.label === selectedLabel)
                      ? selectedLabel
                      : ""
                  }
                  onChange={(event) => setSelectedLabel(event.target.value)}
                >
                  {choices.length === 0 ? (
                    <option value="" disabled>
                      No matching curve labels
                    </option>
                  ) : (
                    <>{choiceOptions}</>
                  )}
                </select>
                <span>
                  {number(choices.length)} matching labels in the rank-filtered
                  cohort. Use keyboard arrows to select.
                </span>
              </label>
              {selected ? (
                <SelectedRecord point={selected} />
              ) : (
                <p>No representative is selected.</p>
              )}
            </div>
          </section>

          <NullDistribution
            values={data.nullStatistics}
            observed={data.summary.observed_statistic}
          />
          <Provenance />
        </>
      )}
    </section>
  );
}

const PLOT = {
  width: 800,
  height: 370,
  left: 66,
  top: 24,
  plotWidth: 716,
  plotHeight: 268.5,
};
const xPosition = (value: number) => PLOT.left + (value / 480) * PLOT.plotWidth;
const yPosition = (value: number) =>
  PLOT.top + ((180 - value) / 180) * PLOT.plotHeight;

const ArithmeticPlot = memo(function ArithmeticPlot({
  points,
  selected,
  onSelect,
}: {
  points: readonly EvidencePoint[];
  selected?: EvidencePoint;
  onSelect: (label: string) => void;
}) {
  return (
    <svg
      className={styles.coordinatePlot}
      viewBox={`0 0 ${PLOT.width} ${PLOT.height}`}
      role="group"
      aria-label="Saved arithmetic longitude versus latitude, in degrees; not observed sky locations"
      data-testid="a01-arithmetic-plot"
      data-longitude-min={0}
      data-longitude-max={480}
      data-latitude-min={0}
      data-latitude-max={180}
    >
      <title>EXP-MAP-A01 saved arithmetic base coordinates</title>
      <desc>
        Longitude ranges from 0 to 480 degrees, preserving values above 360
        without wrapping or clipping. Latitude ranges from 0 to 180 degrees.
        Both axes use the same linear degree spacing. Point selection is also
        available through the curve selector.
      </desc>
      {[0, 120, 240, 360, 480].map((value) => (
        <g key={`x${value}`}>
          <line
            className={styles.gridLine}
            x1={xPosition(value)}
            x2={xPosition(value)}
            y1={PLOT.top}
            y2={PLOT.top + PLOT.plotHeight}
          />
          <text
            x={xPosition(value)}
            y={PLOT.top + PLOT.plotHeight + 27}
            textAnchor="middle"
          >
            {value}
          </text>
        </g>
      ))}
      {[0, 60, 120, 180].map((value) => (
        <g key={`y${value}`}>
          <line
            className={styles.gridLine}
            x1={PLOT.left}
            x2={PLOT.left + PLOT.plotWidth}
            y1={yPosition(value)}
            y2={yPosition(value)}
          />
          <text x={PLOT.left - 12} y={yPosition(value) + 5} textAnchor="end">
            {value}
          </text>
        </g>
      ))}
      <path
        className={styles.axis}
        d={`M${PLOT.left},${PLOT.top}v${PLOT.plotHeight}h${PLOT.plotWidth}`}
      />
      <g className={styles.points}>
        {points.map((point) => (
          <circle
            key={point.label}
            cx={xPosition(point.longitude)}
            cy={yPosition(point.latitude)}
            r={2.6}
            data-sampled-point="true"
            data-label={point.label}
            data-x={point.longitude}
            data-y={point.latitude}
            data-z={point.elevation}
            onClick={() => onSelect(point.label)}
            aria-label={`Select arithmetic curve ${point.label}`}
          >
            <title>
              {point.label} · rank {point.rank} · longitude {point.longitude} ·
              latitude {point.latitude} · elevation {point.elevation}
            </title>
          </circle>
        ))}
      </g>
      {selected ? (
        <circle
          className={styles.selectedMarker}
          cx={xPosition(selected.longitude)}
          cy={yPosition(selected.latitude)}
          r={7}
          data-testid="a01-selected-marker"
          data-label={selected.label}
          data-x={selected.longitude}
          data-y={selected.latitude}
          data-z={selected.elevation}
          aria-label={`Selected curve ${selected.label}`}
        >
          <title>Selected: {selected.label}</title>
        </circle>
      ) : null}
      <text x={PLOT.left + PLOT.plotWidth / 2} y={355} textAnchor="middle">
        Arithmetic longitude (degrees)
      </text>
      <text
        transform={`translate(18 ${PLOT.top + PLOT.plotHeight / 2}) rotate(-90)`}
        textAnchor="middle"
      >
        Arithmetic latitude (degrees)
      </text>
    </svg>
  );
});

function SelectedRecord({ point }: { point: EvidencePoint }) {
  return (
    <section
      className={styles.selectedRecord}
      aria-label="Selected arithmetic representative"
      data-testid="a01-selected-curve"
      data-label={point.label}
      data-conductor={point.conductor}
      data-delta={point.delta}
      data-rank={point.rank}
      data-isogeny-class={point.isogeny_class}
      data-torsion-order={point.torsion_order}
      data-longitude={point.longitude}
      data-latitude={point.latitude}
      data-elevation={point.elevation}
    >
      <h4>{point.label}</h4>
      <dl>
        <RecordValue label="Isogeny class" value={point.isogeny_class} />
        <RecordValue label="Conductor N" value={String(point.conductor)} />
        <RecordValue
          label="Discriminant Δ (exact integer)"
          value={point.delta}
        />
        <RecordValue label="Rank" value={String(point.rank)} />
        <RecordValue
          label="Torsion order"
          value={String(point.torsion_order)}
        />
        <RecordValue
          label="Arithmetic longitude (degrees)"
          value={String(point.longitude)}
        />
        <RecordValue
          label="Arithmetic latitude (degrees)"
          value={String(point.latitude)}
        />
        <RecordValue
          label="Arithmetic elevation (rank × 200)"
          value={String(point.elevation)}
        />
      </dl>
      <p>
        Source row: <code>observed_projection.csv</code>, label{" "}
        <code>{point.label}</code>. Values are saved primary-run outputs.
        Coordinates are displayed with JavaScript round-trip precision; the
        discriminant retains its exact integer string.
      </p>
    </section>
  );
}

function RecordValue({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}

function histogram(
  values: readonly number[],
  low: number,
  high: number,
  count: number,
) {
  const bins = Array.from({ length: count }, (_, index) => ({
    min: low + ((high - low) * index) / count,
    max: low + ((high - low) * (index + 1)) / count,
    count: 0,
  }));
  for (const value of values) {
    const index = Math.min(
      count - 1,
      Math.max(0, Math.floor(((value - low) / (high - low)) * count)),
    );
    bins[index].count++;
  }
  return bins;
}

const NullDistribution = memo(function NullDistribution({
  values,
  observed,
}: {
  values: readonly number[];
  observed: number;
}) {
  const nullMin = Math.min(...values);
  const nullMax = Math.max(...values);
  const fullPadding = (observed - nullMin) * 0.04;
  const detailPadding = (nullMax - nullMin) * 0.05;
  return (
    <section
      className={styles.nullSection}
      aria-label="Saved locked null distribution"
      data-testid="a01-null-distribution"
    >
      <h3>Saved locked null distribution</h3>
      <p>
        All {number(values.length)} saved rank-permutation realizations. T is
        negative mean absolute elevation difference across the locked arithmetic
        k = 10 neighbor graph. Greater or equal T is the preregistered one-sided
        exceedance direction.
      </p>
      <h4>Complete T axis, including the observed statistic</h4>
      <div className={styles.chartScroll}>
        <HistogramChart
          values={values}
          low={nullMin - fullPadding}
          high={observed + fullPadding}
          observed={observed}
        />
      </div>
      <h4>Null-only detail · narrower T axis</h4>
      <p>
        The observed T is outside this detail panel; its position is shown on
        the complete axis above. Bin counts start at zero in both panels.
      </p>
      <div className={styles.chartScroll}>
        <HistogramChart
          values={values}
          low={nullMin - detailPadding}
          high={nullMax + detailPadding}
          detail
        />
      </div>
      <p className={styles.chartNote}>
        0 of 999 null statistics are greater than or equal to observed T =
        -114.40183841751903. The finite permutation p-value is 0.001, not zero.
        This arithmetic null rejection does not test a cosmological
        correspondence.
      </p>
    </section>
  );
});

function HistogramChart({
  values,
  low,
  high,
  observed,
  detail = false,
}: {
  values: readonly number[];
  low: number;
  high: number;
  observed?: number;
  detail?: boolean;
}) {
  const bins = histogram(values, low, high, 24);
  const maxCount = Math.max(...bins.map((bin) => bin.count));
  const yMax = Math.ceil(maxCount / 20) * 20;
  const left = 70,
    top = 52,
    width = 690,
    height = 218,
    baseline = top + height;
  const x = (value: number) => left + ((value - low) / (high - low)) * width;
  const y = (value: number) => baseline - (value / yMax) * height;
  return (
    <svg
      viewBox="0 0 800 354"
      className={styles.histogram}
      role="img"
      aria-label={
        detail
          ? "Null-only histogram of 999 saved statistics, narrower T axis"
          : "Histogram of all 999 saved null statistics with observed T on the same complete axis"
      }
      data-testid={detail ? "a01-null-detail-histogram" : "a01-null-histogram"}
      data-denominator={values.length}
      data-axis-min={low}
      data-axis-max={high}
    >
      <title>
        {detail
          ? "Null-only detail, observed statistic outside panel"
          : "Saved null statistics and observed T, shared linear T axis"}
      </title>
      <desc>
        Histogram counts start at zero. There are 24 equal-width bins. Total
        null realizations: {values.length}.
      </desc>
      {[0, yMax / 2, yMax].map((value) => (
        <g key={value}>
          <line
            className={styles.gridLine}
            x1={left}
            x2={left + width}
            y1={y(value)}
            y2={y(value)}
          />
          <text x={left - 12} y={y(value) + 5} textAnchor="end">
            {value}
          </text>
        </g>
      ))}
      {bins.map((bin, index) => (
        <rect
          key={index}
          className={styles.histogramBar}
          x={x(bin.min) + 1}
          y={y(bin.count)}
          width={width / bins.length - 2}
          height={baseline - y(bin.count)}
          data-count={bin.count}
          data-min={bin.min}
          data-max={bin.max}
        >
          <title>
            {bin.min.toFixed(6)} to {bin.max.toFixed(6)}: {bin.count} of{" "}
            {values.length} saved null statistics
          </title>
        </rect>
      ))}
      <path className={styles.axis} d={`M${left},${top}v${height}h${width}`} />
      {Array.from(
        { length: 5 },
        (_, index) => low + ((high - low) * index) / 4,
      ).map((value) => (
        <text key={value} x={x(value)} y={baseline + 28} textAnchor="middle">
          {value.toFixed(2)}
        </text>
      ))}
      {observed !== undefined ? (
        <g className={styles.observed}>
          <line
            x1={x(observed)}
            x2={x(observed)}
            y1={top}
            y2={baseline}
            data-testid="a01-observed-marker"
            data-statistic={observed}
          />
          <text x={x(observed)} y={22} textAnchor="end">
            Observed T = {String(observed)}
          </text>
          <text x={x(observed)} y={43} textAnchor="end">
            0 / 999 exceedances
          </text>
        </g>
      ) : null}
      <text x={left + width / 2} y={337} textAnchor="middle">
        T · negative mean absolute elevation difference
      </text>
      <text
        transform={`translate(20 ${top + height / 2}) rotate(-90)`}
        textAnchor="middle"
      >
        Count (of 999)
      </text>
    </svg>
  );
}

function Provenance() {
  return (
    <section className={styles.provenance} aria-label="A01 artifact provenance">
      <h3>Immutable artifacts and provenance</h3>
      <p>
        Run <code>{metadata.runId}</code> · protocol{" "}
        <code>{metadata.protocolVersion}</code> · dataset{" "}
        <code>{metadata.datasetId}</code> · provenance <code>PROV-004</code>.
      </p>
      <p>
        Browser verification passed: the static viewer payload matches its
        committed SHA-256 before parsing. The generated data preserves the saved
        coordinates, exact discriminant strings, all representatives, and all
        999 null statistics.
      </p>
      <dl className={styles.provenanceSummary}>
        <RecordValue
          label="Viewer payload SHA-256"
          value={metadata.payload.sha256}
        />
        <RecordValue
          label="Preservation commit (merged PR #104)"
          value={metadata.preservationCommit}
        />
        <RecordValue
          label="Primary execution commit"
          value={metadata.executionCommit}
        />
        <RecordValue
          label="Arithmetic source SHA-256"
          value={metadata.sourceSha256}
        />
        <RecordValue
          label="Pinned upstream ecdata commit"
          value={metadata.sourceCommit}
        />
      </dl>
      <p className={styles.links}>
        <a href={metadata.links.pullRequest}>Merged preservation PR #104</a>
        <a href={metadata.links.package}>Pinned primary package</a>
        <a href={metadata.links.protocol}>Locked preregistration</a>
        <a href={metadata.links.upstream}>Pinned upstream ecdata source</a>
        <a href={metadata.payload.url} download>
          Static viewer data
        </a>
      </p>
      <details>
        <summary>Source artifact hashes and pinned parameters</summary>
        <div className={styles.sourceList}>
          {metadata.sources.map((source) => (
            <div key={source.name}>
              <a href={source.url}>{source.name}</a>
              <p>
                {number(source.sizeBytes)} bytes · SHA-256{" "}
                <code>{source.sha256}</code>
              </p>
            </div>
          ))}
        </div>
        <dl className={styles.parameters}>
          <RecordValue
            label="Neighbor k"
            value={String(metadata.pinnedParameters.neighborK)}
          />
          <RecordValue
            label="Rank scale"
            value={String(metadata.pinnedParameters.rankScale)}
          />
          <RecordValue
            label="Null seed"
            value={String(metadata.pinnedParameters.seed)}
          />
          <RecordValue
            label="Null realizations"
            value={String(metadata.pinnedParameters.realizations)}
          />
          <RecordValue
            label="Null PRNG"
            value={metadata.pinnedParameters.prng}
          />
          <RecordValue
            label="P-value formula"
            value={metadata.pinnedParameters.pValueFormula}
          />
        </dl>
        <p>
          The map uses natural logarithms with locked normalization Δmax = 10³⁰
          and Nmax = 10⁹, longitude scale 360°, latitude scale 180°, rank scale
          200, and clipping disabled. No controls alter these pinned parameters.
        </p>
      </details>
      <p className={styles.boundary}>
        Interpretation is limited to the locked arithmetic rank-permutation
        NULL-MAP-001. Independent replication, ACSC physical support, and
        support eligibility promotion remain absent. This viewer does not
        execute an experiment or modify registry flags.
      </p>
    </section>
  );
}
