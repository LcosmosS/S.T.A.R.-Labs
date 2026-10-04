import { Engine, Scene, Vector3 } from "@babylonjs/core";
const engine = new Engine(canvas, true, { preserveDrawingBuffer: false, stencil: true, powerPreference: "high-performance" });
const scene = new Scene(engine);
engine.runRenderLoop(() => scene.render());
window.addEventListener("resize", () => engine.resize());
