const STEP = 1/60; let acc = 0;
function frame(dt){ acc += Math.min(dt, 0.25);        // clamp to avoid spiral-of-death after tab-out
  while (acc >= STEP){ physicsStep(STEP); acc -= STEP; }
  const alpha = acc / STEP; render(alpha);            // interpolate between last two states
}
