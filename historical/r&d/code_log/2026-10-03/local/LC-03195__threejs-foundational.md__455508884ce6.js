const timer = new THREE.Timer();
let accumulator = 0; const FIXED = 1/60;
function animate() {
  timer.update();
  let delta = Math.min(timer.getDelta(), 0.25);
  accumulator += delta;
  while (accumulator >= FIXED) { fixedUpdate(FIXED); accumulator -= FIXED; } // physics/AI
  updateVisuals(delta);
  renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);
