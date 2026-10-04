import { WebGPUEngine, Engine } from "@babylonjs/core";
async function createEngine(canvas) {
  if (await WebGPUEngine.IsSupportedAsync) {
    const e = new WebGPUEngine(canvas, { antialias: true });
    await e.initAsync();            // REQUIRED before creating a Scene
    return e;
  }
  return new Engine(canvas, true, { powerPreference: "high-performance" });   // WebGL2 fallback
}
