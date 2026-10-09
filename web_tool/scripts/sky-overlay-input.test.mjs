import test from "node:test";
import assert from "node:assert/strict";
import { parseFrozenSkyCSV, validateScope, validateSha256, MAX_SKY_SOURCES } from "../src/lib/star/sky-overlay-input.ts";

test("only pre-existing dataset scopes can be labeled registered", () => {
  assert.equal(validateScope("DATA-SDSS18-200K"), "DATA-SDSS18-200K");
  assert.equal(validateScope("DATA-MANGA-HI-ALL"), "DATA-MANGA-HI-ALL");
  assert.throws(() => validateScope("DATA-VIZIER-ALFALFA100"), /Unregistered/);
});
test("hash must be complete rather than a placeholder or Dropbox content hash", () => {
  assert.equal(validateSha256("A".repeat(64)), "a".repeat(64));
  assert.throws(() => validateSha256("abc"), /64 hexadecimal/);
});
test("exact three-column ICRS coordinates, poles and RA wrapping are accepted", () => {
  const pts = parseFrozenSkyCSV("source_id,ra_deg,dec_deg\r\nAGC:1,359.9999,-90\r\nAGC:2,0,90\r\n");
  assert.equal(pts.length, 2);
  assert.equal(pts[0].ra_deg, 359.9999);
});
test("reject source aliases, blanks, duplicate IDs, out-of-range and unquoted CSV ambiguity", () => {
  for (const csv of [
    "ra,dec,id\nX,1,1\n",
    "source_id,ra_deg,dec_deg\nX,0,0\nX,1,1\n",
    "source_id,ra_deg,dec_deg\nX,360,0\n",
    "source_id,ra_deg,dec_deg\nX,10,-90.1\n",
    "source_id,ra_deg,dec_deg\nX,NaN,1\n",
    "source_id,ra_deg,dec_deg\nX,1,\n",
    "source_id,ra_deg,dec_deg\n\"X\",1,2\n",
    "source_id,ra_deg,dec_deg\n<script>,1,2\n",
  ]) assert.throws(() => parseFrozenSkyCSV(csv));
});
test("fail closed on overlarge tables", () => {
  const text = "source_id,ra_deg,dec_deg\n" + Array.from({length: MAX_SKY_SOURCES+1}, (_,i)=>`X${i},1,2`).join("\n");
  assert.throws(() => parseFrozenSkyCSV(text), /between 1 and 2,000/);
});
