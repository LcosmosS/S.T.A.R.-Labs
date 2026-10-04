import { readdirSync } from "node:fs";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
function tests(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? tests(path) : /\.test\.(mjs|ts)$/.test(path) ? [path] : [];
  });
}
const run = spawnSync(process.execPath, ["--experimental-strip-types", "--test", ...tests("scripts"), ...tests("src/lib")], { stdio: "inherit" });
process.exit(run.status ?? 1);
