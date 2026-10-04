import { SceneOptimizer, SceneOptimizerOptions } from "@babylonjs/core";
// preset tiers try progressively harder optimizations to reach the target FPS:
SceneOptimizer.OptimizeAsync(scene,
  SceneOptimizerOptions.HighDegradationAllowed(60),   // target 60 fps
  () => console.log("reached target"),
  () => console.log("could not reach target"));
