// Input (held keys → actions once per frame)
let steer = 0; // -1..+1, player-visible
if (keys.has('KeyA') || keys.has('ArrowLeft'))  steer += 1;  // LEFT
if (keys.has('KeyD') || keys.has('ArrowRight')) steer -= 1;  // RIGHT
// Optional: steer = clamp(steer + gamepadX, -1, 1) with same sign convention

// Integrate (speedFactor ~ 0..1 from |speed|)
const reverse = speed >= 0 ? 1 : -1; // wheel-left still feels left in reverse
yaw += steer * turnRate * speedFactor * reverse * dt;

// Move along heading
const fx = -Math.sin(yaw), fz = -Math.cos(yaw);
position.x += fx * speed * dt;
position.z += fz * speed * dt;
