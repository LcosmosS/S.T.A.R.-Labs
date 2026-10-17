#!/usr/bin/env node
/** Production-browser checks for the read-only EXP-MAP-A01 evidence viewer.
 *
 * Every plotted value is compared with the preserved primary CSV, not a
 * second projection implementation. External services are replaced locally;
 * this test neither downloads sky imagery nor executes an experiment.
 */
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdir, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const origin = process.argv[2]?.replace(/\/$/, "");
if (!/^http:\/\/127\.0\.0\.1:808[01]$/.test(origin ?? "")) {
  console.error("Usage: node scripts/a01-browser-smoke.mjs http://127.0.0.1:8081 (or :8080); optional CHROMIUM_EXECUTABLE_PATH / CHROMIUM");
  process.exit(2);
}

const runId = "20261016T041335361140Z-e60fd05117fc";
const primaryDirectory = new URL(`../../release_packages/EXP-MAP-A01-primary-execution-v0.1/${runId}/`, import.meta.url);
const [sourceBytes, nullBytes, summaryBytes, manifestBytes, metadataBytes, payloadBytes] = await Promise.all([
  readFile(new URL("observed_projection.csv", primaryDirectory)),
  readFile(new URL("null_statistics.csv", primaryDirectory)),
  readFile(new URL("summary.json", primaryDirectory)),
  readFile(new URL("manifest.json", primaryDirectory)),
  readFile(new URL("../src/lib/star/a01-evidence-metadata.json", import.meta.url)),
  readFile(new URL("../public/evidence/a01-primary-v1.json", import.meta.url)),
]);
/**
 * Hash the exact file bytes for comparison with the reviewed viewer metadata.
 * @param {import("node:crypto").BinaryLike} bytes - Preserved or generated file contents.
 * @returns {string} Lowercase hexadecimal SHA-256 digest; no text normalization is applied.
 */
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const metadata = JSON.parse(metadataBytes);
const summary = JSON.parse(summaryBytes);
const payload = JSON.parse(payloadBytes);
const payloadPath = metadata.payload.url;
assert.equal(payloadPath, "/evidence/a01-primary-v1.json");
assert.equal(payloadBytes.length, metadata.payload.sizeBytes, "Reviewed output byte count");
assert.equal(sha256(payloadBytes), metadata.payload.sha256, "Reviewed output SHA-256");
for (const [name, bytes] of [["observed_projection.csv", sourceBytes], ["null_statistics.csv", nullBytes], ["summary.json", summaryBytes], ["manifest.json", manifestBytes]]) {
  const recorded = metadata.sources.find((item) => item.name === name);
  assert.ok(recorded, `Immutable ${name} is recorded in viewer provenance`);
  assert.equal(bytes.length, recorded.sizeBytes, `Immutable ${name} size`);
  assert.equal(sha256(bytes), recorded.sha256, `Immutable ${name} SHA-256`);
}
/**
 * Read the simple, unquoted primary CSV format into records of original strings.
 * @param {Buffer} bytes - Saved CSV bytes with a header and equal-width data rows.
 * @returns {Record<string, string>[]} Source-order records, retaining exact integer text.
 * @throws {assert.AssertionError} When a row has a different cell count from the header.
 */
const parseCsv = (bytes) => {
  const [header, ...lines] = bytes.toString("utf8").trimEnd().split(/\r?\n/);
  const columns = header.split(",");
  return lines.map((line, index) => {
    const cells = line.split(",");
    assert.equal(cells.length, columns.length, `Primary CSV row ${index + 2} column count`);
    return Object.fromEntries(columns.map((column, i) => [column, cells[i]]));
  });
};
const source = parseCsv(sourceBytes);
const byLabel = new Map(source.map((point) => [point.label, point]));
const nulls = parseCsv(nullBytes).map((row) => Number(row.statistic));
assert.equal(source.length, 38042);
assert.equal(byLabel.size, source.length, "Preserved labels are unique");
assert.deepEqual(payload.points, source.map((point) => ({
  label: point.label, isogeny_class: point.isogeny_class,
  conductor: Number(point.conductor), delta: point.delta,
  rank: Number(point.rank), torsion_order: Number(point.torsion_order),
  longitude: Number(point.longitude), latitude: Number(point.latitude), elevation: Number(point.elevation),
})), "Every static point retains the primary CSV values and source order");
assert.equal(nulls.length, 999);
assert.deepEqual(payload.nullStatistics, nulls, "Static null values retain primary output order");
assert.deepEqual(payload.summary, summary, "Static summary equals preserved primary summary");
assert.equal(summary.observed_statistic, -114.40183841751903);
assert.equal(summary.null_exceedances, 0);
assert.equal(summary.p_value, 0.001);
assert.equal(summary.alpha, 0.01);
const rankCounts = new Map();
for (const point of source) rankCounts.set(Number(point.rank), (rankCounts.get(Number(point.rank)) ?? 0) + 1);
const screenshots = fileURLToPath(new URL("../screenshots/", import.meta.url));
await mkdir(screenshots, { recursive: true });

const aladinSpy = `window.A={init:Promise.resolve(),aladin:()=>({addCatalog:()=>{},setImageSurvey:()=>{}}),catalog:()=>({addSources:()=>{},removeAll:()=>{}}),source:(ra,dec,data)=>({ra,dec,data})};`;
const browser = await chromium.launch({
  headless: true,
  ...(process.env.CHROMIUM_EXECUTABLE_PATH || process.env.CHROMIUM
    ? { executablePath: process.env.CHROMIUM_EXECUTABLE_PATH || process.env.CHROMIUM }
    : {}),
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
});

/**
 * Create an isolated browser page with local substitutes for every off-origin request.
 * Optionally replace the evidence response to exercise explicit failure states, and
 * collect page errors, console errors, and payload requests for later assertions.
 * @param {{width: number, height: number}} viewport - Browser dimensions for this case.
 * @param {{status?: number, body: string | Buffer}} [replacement] - Evidence response override.
 * @returns {Promise<object>} Context, page, and mutable error/request collections; the caller closes the context.
 */
async function newOfflinePage(viewport, replacement) {
  const context = await browser.newContext({ viewport, reducedMotion: "reduce" });
  const page = await context.newPage();
  const errors = [];
  const payloadRequests = [];
  page.on("pageerror", (error) => errors.push(String(error)));
  page.on("console", (event) => {
    if (event.type() !== "error") return;
    // A missing asset produces an expected browser resource warning. Its
    // caught loader failure must still produce the explicit fail-closed UI.
    if (replacement?.status === 404 && event.location().url === origin + payloadPath) return;
    errors.push(event.text());
  });
  await context.route("**/*", async (route) => {
    const request = route.request();
    const url = new URL(request.url());
    if (url.origin === origin) {
      if (url.pathname === payloadPath) {
        payloadRequests.push({ url: request.url(), method: request.method() });
        if (replacement) {
          await route.fulfill({ status: replacement.status ?? 200, contentType: "application/json", body: replacement.body });
          return;
        }
      }
      await route.continue();
      return;
    }
    // Nothing off-origin reaches a network. Aladin is unrelated to arithmetic
    // evidence and receives the same deterministic local spy as sky smoke.
    const resourceType = request.resourceType();
    const isAladin = url.hostname === "aladin.cds.unistra.fr" && url.pathname.endsWith("/aladin.js");
    await route.fulfill({
      status: 200,
      headers: { "access-control-allow-origin": "*" },
      contentType: resourceType === "stylesheet" ? "text/css" : resourceType === "image" ? "image/svg+xml" : "application/javascript",
      body: isAladin ? aladinSpy : resourceType === "image" ? '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>' : "",
    });
  });
  return { context, page, errors, payloadRequests };
}

/**
 * Navigate to a local route and wait for the projection controls to hydrate.
 * @param {import("playwright").Page} page - Offline page returned by newOfflinePage.
 * @param {string} [path="/projection"] - Route expected to contain the projection mode controls.
 * @returns {Promise<void>} Resolves once the Synthetic Demo control and hydration marker exist.
 * @throws {Error} On navigation/readiness timeout or a non-200 response.
 */
async function open(page, path = "/projection") {
  const response = await page.goto(origin + path, { waitUntil: "domcontentloaded", timeout: 45000 });
  assert.equal(response?.status(), 200, `${path} production HTTP status`);
  await page.getByRole("button", { name: "Synthetic Demo", exact: true }).waitFor();
  await page.locator('[data-a01-hydrated="true"]').waitFor({ timeout: 20000 });
}

/**
 * Select A01 Evidence and assert saved-result labels and scientific limitations.
 * @param {import("playwright").Page} page - Hydrated projection page.
 * @returns {Promise<import("playwright").Locator>} Loaded evidence panel after the synthetic plot is hidden.
 * @throws {Error} If the evidence plot fails to appear or required boundaries/results are absent.
 */
async function evidence(page) {
  await page.getByRole("button", { name: "A01 Evidence", exact: true }).click();
  await page.getByTestId("a01-arithmetic-plot").waitFor({ timeout: 30000 });
  const panel = page.getByTestId("a01-evidence-viewer");
  const text = await panel.innerText();
  assert.match(text, /arithmetic/i);
  assert.match(text, /NULL-MAP-001/);
  assert.match(text, /-114\.40183841751903/);
  assert.match(text, /0\s*(?:\/|of)\s*999/);
  assert.match(text, /0\.001/);
  assert.match(text, /0\.01/);
  assert.match(text, /replicat/i);
  assert.match(text, /physical support/i);
  assert.match(text, /(?:not|no|never)[^.\n]*(?:sky|astronomical|observed)/i);
  assert.equal(await page.getByTestId("synthetic-demo").isVisible().catch(() => false), false, "Evidence mode hides synthetic fixture plot");
  return panel;
}

/**
 * Assert that the document fits the viewport, allowing one pixel of browser rounding.
 * Local chart scrolling is permitted; horizontal overflow of the whole page is not.
 * @param {import("playwright").Page} page - Page whose document dimensions are inspected.
 * @returns {Promise<void>} Resolves when the page width assertion passes.
 */
async function assertNoOverflow(page) {
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1), false, "No horizontal page overflow");
}

/**
 * Check that an SVG mark has finite geometry wholly inside its owning viewBox.
 * @param {import("playwright").Locator} mark - SVG mark supporting getBBox.
 * @param {string} label - Description included in assertion failures.
 * @returns {Promise<void>} Resolves when the mark is not clipped by the SVG domain.
 */
async function assertSvgMarkVisible(mark, label) {
  const geometry = await mark.evaluate((node) => {
    const svg = node.ownerSVGElement;
    const box = node.getBBox();
    const view = svg.viewBox.baseVal;
    return { x: box.x, y: box.y, width: box.width, height: box.height, viewX: view.x, viewY: view.y, viewWidth: view.width, viewHeight: view.height };
  });
  assert.ok(Object.values(geometry).every(Number.isFinite), `${label} has finite display coordinates`);
  assert.ok(geometry.x >= geometry.viewX && geometry.y >= geometry.viewY && geometry.x + geometry.width <= geometry.viewX + geometry.viewWidth && geometry.y + geometry.height <= geometry.viewY + geometry.viewHeight, `${label} is inside the SVG, not clipped outside its domain`);
}

/**
 * Scroll a chart mark into view and verify its bounds fit the chart's local viewport.
 * @param {import("playwright").Locator} mark - SVG mark inside a horizontal scroll container.
 * @param {string} label - Description included in assertion failures.
 * @returns {Promise<void>} Resolves when a mobile user can reach the whole mark horizontally.
 */
async function assertHorizontallyReachable(mark, label) {
  await mark.scrollIntoViewIfNeeded();
  const [markBox, clipBox] = await Promise.all([
    mark.boundingBox(),
    mark.evaluate((node) => {
      const clip = node.ownerSVGElement.parentElement.getBoundingClientRect();
      return { x: clip.x, width: clip.width };
    }),
  ]);
  assert.ok(markBox && clipBox, `${label} has visible browser bounds`);
  assert.ok(markBox.x >= clipBox.x - 1 && markBox.x + markBox.width <= clipBox.x + clipBox.width + 1, `${label} is reachable inside its local horizontal scroll region`);
}

/**
 * Read rendered sample identities, saved coordinates, and SVG positions from the DOM.
 * Selection overlays are excluded so the result measures only the rendering sample.
 * @param {import("playwright").Page} page - Page with an A01 arithmetic plot.
 * @returns {Promise<object[]>} Source values and screen positions for each sampled circle.
 */
async function plottedPoints(page) {
  return page.getByTestId("a01-arithmetic-plot").locator('[data-sampled-point="true"]').evaluateAll((nodes) => nodes.map((node) => ({
    label: node.getAttribute("data-label"),
    x: Number(node.getAttribute("data-x")),
    y: Number(node.getAttribute("data-y")),
    z: Number(node.getAttribute("data-z")),
    screenX: Number(node.getAttribute("cx")),
    screenY: Number(node.getAttribute("cy")),
  })));
}

/**
 * Compare sampled marks against the preserved CSV and check equal linear axis spacing.
 * This checks display fidelity only; it does not rerun A01 or establish physical support.
 * @param {object[]} points - DOM records returned by plottedPoints.
 * @param {number} [rank] - Optional cohort rank that every sampled representative must match.
 * @returns {void} Returns after identity, exact coordinate, and scale assertions pass.
 * @throws {assert.AssertionError} On duplicate/unknown labels, changed coordinates, or nonlinear scaling.
 */
function assertPrimaryCoordinates(points, rank) {
  assert.equal(new Set(points.map((point) => point.label)).size, points.length, "Rendering sample never duplicates representatives");
  for (const point of points) {
    const original = byLabel.get(point.label);
    assert.ok(original, `${point.label} exists in immutable primary CSV`);
    assert.equal(point.x, Number(original.longitude), `${point.label} preserved arithmetic longitude`);
    assert.equal(point.y, Number(original.latitude), `${point.label} preserved arithmetic latitude`);
    assert.equal(point.z, Number(original.elevation), `${point.label} preserved arithmetic elevation`);
    if (rank !== undefined) assert.equal(Number(original.rank), rank, "Rank filter applies before rendering sample");
  }
  if (points.length > 1) {
    const base = points[0];
    const otherX = points.find((point) => point.x !== base.x);
    const otherY = points.find((point) => point.y !== base.y);
    assert.ok(otherX && otherY, "Cohort spans both arithmetic axes");
    const xScale = (otherX.screenX - base.screenX) / (otherX.x - base.x);
    const yScale = (otherY.screenY - base.screenY) / (otherY.y - base.y);
    assert.ok(xScale > 0 && yScale < 0, "Arithmetic axes have the expected directions");
    assert.ok(Math.abs(xScale + yScale) < 1e-9, "Both arithmetic axes preserve equal display spacing per degree");
    for (const point of points) {
      assert.ok(Math.abs(point.screenX - (base.screenX + (point.x - base.x) * xScale)) < 1e-8, "Plotted longitude remains linear, without a geographic transform");
      assert.ok(Math.abs(point.screenY - (base.screenY + (point.y - base.y) * yScale)) < 1e-8, "Plotted latitude remains linear, without a geographic transform");
    }
  }
}

/**
 * Wait for and verify full filtered counts separately from the capped rendering count.
 * @param {import("playwright").Page} page - Evidence page after a rank selection.
 * @param {number} filtered - Expected number of representatives in the complete cohort.
 * @param {number} rendered - Expected number of sampled points actually plotted.
 * @returns {Promise<void>} Resolves when both counts and the display-cap explanation agree.
 */
async function assertCount(page, filtered, rendered) {
  const count = page.getByTestId("a01-rendering-count");
  await page.waitForFunction(({ filtered, rendered }) => {
    const element = document.querySelector('[data-testid="a01-rendering-count"]');
    return element?.getAttribute("data-filtered-count") === String(filtered) && element?.getAttribute("data-rendered-count") === String(rendered);
  }, { filtered, rendered });
  assert.equal(Number(await count.getAttribute("data-filtered-count")), filtered, "Full filtered cohort count");
  assert.equal(Number(await count.getAttribute("data-rendered-count")), rendered, "Rendering cap count");
  assert.match(await count.innerText(), /render|display/i, "Cap described as rendering optimization");
}

const verdicts = [];
try {
  for (const viewport of [{ width: 1280, height: 900 }, { width: 390, height: 844 }]) {
    const { page, context, errors, payloadRequests } = await newOfflinePage(viewport);
    try {
      await open(page);
      const demo = page.getByTestId("synthetic-demo");
      await demo.waitFor();
      assert.equal(await demo.getAttribute("data-fixture-count"), "160", "Default Synthetic Demo retains all 160 original fixtures");
      assert.equal(await page.getByTestId("a01-arithmetic-plot").count(), 0, "No evidence plot in default Synthetic Demo");
      assert.equal(payloadRequests.length, 0, "Evidence payload loads only upon mode selection");
      await assertNoOverflow(page);

      const panel = await evidence(page);
      await assertCount(page, source.length, 4000);
      const initial = await plottedPoints(page);
      assert.equal(initial.length, 4000, "Default deterministic rendering cap");
      assertPrimaryCoordinates(initial);
      const distribution = page.getByTestId("a01-null-distribution");
      for (const name of ["a01-null-histogram", "a01-null-detail-histogram"]) {
        const histogram = page.getByTestId(name);
        assert.equal(await histogram.getAttribute("data-denominator"), "999");
        const bins = await histogram.locator("[data-count]").evaluateAll((nodes) => nodes.map((node) => ({
          count: Number(node.getAttribute("data-count")),
          min: Number(node.getAttribute("data-min")),
          max: Number(node.getAttribute("data-max")),
        })));
        assert.equal(bins.length, 24, "A genuine equal-width null histogram is rendered");
        assert.equal(bins.reduce((sum, bin) => sum + bin.count, 0), 999, "Histogram includes all 999 preserved null realizations");
        for (let i = 0; i < bins.length; i++) {
          const bin = bins[i];
          const expected = nulls.filter((value) => value >= bin.min && (i === bins.length - 1 ? value <= bin.max : value < bin.max)).length;
          assert.equal(bin.count, expected, `${name} bin ${i + 1} matches primary null values`);
        }
      }
      assert.equal(Number(await distribution.locator("[data-statistic]").getAttribute("data-statistic")), summary.observed_statistic, "Observed-statistic marker uses primary statistic");
      await assertSvgMarkVisible(distribution.locator("[data-statistic]"), "Observed statistic beyond the null range");
      if (viewport.width < 640) {
        await assertHorizontallyReachable(distribution.locator("[data-statistic]"), "Mobile observed-statistic marker");
        await page.getByTestId("a01-null-histogram").locator("..").screenshot({ path: `${screenshots}/a01-null-observed-${viewport.width}.png`, animations: "disabled" });
      }
      await assertNoOverflow(page);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({ path: `${screenshots}/a01-evidence-${viewport.width}.png`, animations: "disabled", fullPage: true });

      // Every rank can be selected; a low-count rank must plot its entire
      // cohort, while a common rank still uses the identical rendering cap.
      for (const [rank, count] of rankCounts) {
        await page.getByLabel("Rank filter", { exact: true }).selectOption(String(rank));
        await assertCount(page, count, Math.min(count, 4000));
        const filtered = await plottedPoints(page);
        assert.equal(filtered.length, Math.min(count, 4000));
        assertPrimaryCoordinates(filtered, rank);
        assert.equal(await page.getByTestId("a01-observed-statistic").innerText(), String(summary.observed_statistic), "Rank filtering cannot change the locked full-cohort observed statistic");
      }
      await page.getByLabel("Rank filter", { exact: true }).selectOption("all");
      assert.deepEqual(await plottedPoints(page), initial, "Returning to all ranks reproduces the same deterministic sample");

      const renderedLabels = new Set(initial.map((point) => point.label));
      const outsideSample = source.find((point) => !renderedLabels.has(point.label) && (BigInt(point.delta) < 0n ? -BigInt(point.delta) : BigInt(point.delta)) > BigInt(Number.MAX_SAFE_INTEGER));
      assert.ok(outsideSample, "Primary cohort has selectable representatives outside rendering sample");
      const selector = page.getByLabel("Select evidence curve", { exact: true });
      assert.equal(await selector.locator("option").count(), source.length, "Selection includes the entire filtered cohort, not only sampled points");
      await page.getByLabel("Find curve label", { exact: true }).fill(outsideSample.label);
      await selector.selectOption(outsideSample.label);
      const details = page.getByTestId("a01-selected-curve");
      await details.getByRole("heading", { name: outsideSample.label, exact: true }).waitFor();
      const detailText = await details.innerText();
      for (const field of ["label", "isogeny_class", "conductor", "delta", "rank", "torsion_order"]) {
        assert.ok(detailText.includes(outsideSample[field]), `Selected primary ${field} displayed`);
      }
      for (const [field, attribute] of [["label", "label"], ["isogeny_class", "isogeny-class"], ["conductor", "conductor"], ["delta", "delta"], ["rank", "rank"], ["torsion_order", "torsion-order"], ["longitude", "longitude"], ["latitude", "latitude"], ["elevation", "elevation"]]) {
        const expected = ["label", "isogeny_class", "delta"].includes(field) ? outsideSample[field] : String(Number(outsideSample[field]));
        assert.equal(await details.getAttribute(`data-${attribute}`), expected, `Selected primary ${field} exact value`);
      }
      const marker = page.getByTestId("a01-selected-marker");
      assert.equal(await marker.getAttribute("data-label"), outsideSample.label, "Non-sampled selection is visibly marked");
      assert.equal(Number(await marker.getAttribute("data-x")), Number(outsideSample.longitude));
      assert.equal(Number(await marker.getAttribute("data-y")), Number(outsideSample.latitude));
      assert.equal(Number(await marker.getAttribute("data-z")), Number(outsideSample.elevation));
      await assertSvgMarkVisible(marker, "Non-sampled selected representative");
      // Arithmetic 'longitude' is not geographic longitude and legitimately
      // exceeds 360. Selecting the extreme guards against wrapping/clipping.
      const maximumLongitude = source.reduce((maximum, point) => Number(point.longitude) > Number(maximum.longitude) ? point : maximum);
      assert.ok(Number(maximumLongitude.longitude) > 360, "Preserved arithmetic domain extends beyond a geographic longitude range");
      await page.getByLabel("Find curve label", { exact: true }).fill(maximumLongitude.label);
      await selector.selectOption(maximumLongitude.label);
      await details.getByRole("heading", { name: maximumLongitude.label, exact: true }).waitFor();
      assert.equal(Number(await marker.getAttribute("data-x")), Number(maximumLongitude.longitude));
      await assertSvgMarkVisible(marker, "Arithmetic coordinate above 360 degrees");
      if (viewport.width < 640) await assertHorizontallyReachable(marker, "Mobile arithmetic coordinate above 360 degrees");
      await page.getByLabel("Find curve label", { exact: true }).fill(outsideSample.label);
      await selector.selectOption(outsideSample.label);
      await details.getByRole("heading", { name: outsideSample.label, exact: true }).waitFor();
      assert.match(await panel.innerText(), /PROV-004/);
      assert.match(await panel.innerText(), /259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968/);
      assert.match(await panel.innerText(), new RegExp(runId));
      for (const name of ["observed_projection.csv", "null_statistics.csv", "summary.json", "manifest.json"]) {
        const links = panel.locator(`a[href*="/${runId}/${name}"]`);
        assert.ok(await links.count() > 0, `Immutable ${name} provenance link is available`);
      }
      await panel.locator("details > summary").click();
      await assertNoOverflow(page);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({ path: `${screenshots}/a01-selection-${viewport.width}.png`, animations: "disabled", fullPage: true });

      await page.getByRole("button", { name: "Synthetic Demo", exact: true }).click();
      assert.equal(await page.getByTestId("synthetic-demo").getAttribute("data-fixture-count"), "160");
      assert.equal(await page.getByTestId("a01-arithmetic-plot").count(), 0, "Evidence points never become demo fixtures");
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({ path: `${screenshots}/a01-synthetic-demo-${viewport.width}.png`, animations: "disabled" });
      await evidence(page);
      assert.deepEqual(await plottedPoints(page), initial, "Mode round-trip preserves deterministic sample");
      assert.ok(payloadRequests.length > 0);
      assert.ok(payloadRequests.every((request) => request.url === origin + payloadPath && request.method === "GET"), "Evidence loading performs same-origin GET requests only");
      assert.deepEqual(errors, [], "No uncaught errors or console errors on desktop/mobile");
      verdicts.push({ viewport, primaryRows: source.length, rendered: initial.length, ranks: rankCounts.size, nullRealizations: nulls.length, outsideSampleSelection: outsideSample.label, ok: true });
    } finally {
      await context.close();
    }
  }

  // A syntactically valid, same-length alteration is the SHA verification
  // case: byte-count checks alone cannot reject it. Truncation and missing
  // bytes exercise independent failure paths. No fallback plot is admitted.
  const tampered = Buffer.from(payloadBytes);
  const labelOffset = tampered.indexOf(Buffer.from('"11a1"'));
  assert.ok(labelOffset >= 0, "Known primary label is present in static payload");
  tampered[labelOffset + 2] = 50; // 11a1 -> 12a1; valid JSON, unchanged byte length.
  assert.equal(tampered.length, payloadBytes.length);
  assert.notEqual(sha256(tampered), metadata.payload.sha256);
  for (const replacement of [
    { name: "tampered", body: tampered, expected: /SHA-256|hash|digest/i },
    { name: "truncated", body: payloadBytes.subarray(0, payloadBytes.length - 30), expected: /byte|size|length|truncat/i },
    { name: "missing", status: 404, body: "Missing evidence asset", expected: /404|HTTP|fetch|load/i },
  ]) {
    const { page, context, errors, payloadRequests } = await newOfflinePage({ width: 1280, height: 900 }, replacement);
    try {
      await open(page);
      await page.getByRole("button", { name: "A01 Evidence", exact: true }).click();
      const alert = page.getByRole("alert").filter({ hasText: /A01 evidence unavailable/i });
      await alert.waitFor({ timeout: 30000 });
      assert.match(await alert.innerText(), replacement.expected, `${replacement.name} diagnostic identifies the failure`);
      assert.equal(await page.getByTestId("a01-arithmetic-plot").count(), 0, `${replacement.name} payload cannot create an evidence plot`);
      assert.equal(await page.getByTestId("a01-null-distribution").count(), 0, `${replacement.name} payload cannot create a null histogram`);
      assert.equal(await page.getByTestId("synthetic-demo").isVisible().catch(() => false), false, "Failed evidence load does not silently substitute a synthetic plot");
      // React development StrictMode replays a mounted effect once (the first
      // fetch is aborted). Production must make exactly one failing request.
      const maximumRequests = origin.endsWith(":8080") ? 2 : 1;
      assert.ok(payloadRequests.length >= 1 && payloadRequests.length <= maximumRequests, "Failure is explicit without an unbounded retry loop");
      assert.deepEqual(errors, [], "Fail-closed error is handled without uncaught runtime errors");
      await assertNoOverflow(page);
      verdicts.push({ rejectedPayload: replacement.name, ok: true });
    } finally {
      await context.close();
    }
  }
  console.log(JSON.stringify({ ok: true, origin, outputSha256: metadata.payload.sha256, primaryProjectionSha256: sha256(sourceBytes), primaryNullSha256: sha256(nullBytes), checks: verdicts }, null, 2));
} finally {
  await browser.close();
}
